"""
Supply functionality for process and analysis of data from transcriptomics.

This module 'interaction' is part of the 'transcriptomics' package within
the 'exercise' package.

Author:

    T. Cameron Waller, Ph.D.
    tcameronwaller@gmail.com
    Rochester, Minnesota 55902
    United States of America

License:

    This file is part of the project package directory 'exercise'
    (https://github.com/tcameronwaller/exercise/).

    Project 'exercise' supports data analysis with team in endocrinology.
    Copyright (C) 2024 Thomas Cameron Waller

    The code within project 'exercise' is free software: you can redistribute
    it and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the GNU
    General Public License, or (at your option) any later version.

    The code within project 'exercise' is distributed in the hope that it will
    be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
    Public License for more details.

    You should have received a copy of the GNU General Public License along
    with project 'exercise'. If not, see <http://www.gnu.org/licenses/>.
"""


###############################################################################
# Notes

# consider changing the name of this module to "select_changes"


###############################################################################
# Installation and importation

# Standard
import sys
#print(sys.path)
import os
import math
import statistics
import pickle
import copy
import random
import itertools
import time

# Relevant
import numpy
import scipy.stats
import pandas
pandas.options.mode.chained_assignment = None # default = "warn"
pandas.set_option('future.no_silent_downcasting', True) # set option to suppress warnings

# Custom
import partner.utility as putly
import partner.extraction as pextr
import partner.organization as porg
import partner.scale as pscl
import partner.description as pdesc
#import partner.regression as preg
import partner.plot as pplot
import partner.parallelization as prall
import exercise.transcriptomics.organize_signal as exrosig

###############################################################################
# Functionality



def extract_sample_sets_by_two_categories_two_levels(
    categories_levels=None,
    column_sample_identifier=None,
    table=None,
    report=None,
):
    """
    Extract sets of samples from a table by combinations of level values of
    categorical variables.

    arguments:
        categories_levels (dict<list<str>>): names of two categorical variables
            and level values of each
        column_sample_identifier (str): name of column in tables for
            identifiers that correspond to samples and their signals
        table (object): Pandas data-frame table of properties or attributes of
            samples
        report (bool): whether to print reports

    raises:

    returns:
        (list<dict<str>>): records of information about each set of samples
            that includes the categories and their levels which define these
            sets

    """

    # Copy information in table.
    table = table.copy(deep=True)
    # Organize indices in table.
    table.reset_index(
        level=None,
        inplace=True,
        drop=False, # remove index; do not move to regular columns
    )

    # Create combinations of level values of categorical variables.
    categories_levels_flat = list()
    for category in categories_levels.keys():
        category_levels_flat = list()
        for level in categories_levels[category]:
            category_levels_flat.append(str(str(category) + ";" + str(level)))
            pass
        categories_levels_flat.append(category_levels_flat)
        pass
    combinations = list(itertools.product(
        categories_levels_flat[0],
        categories_levels_flat[1],
        repeat=1
    ))

    # Extract and collect sets of samples corresponding to combinations of
    # level values of categorical variables.
    records_sets = list()
    for combination in combinations:
        category_first = str(combination[0]).split(";")[0]
        level_first = str(combination[0]).split(";")[1]
        category_second = str(combination[1]).split(";")[0]
        level_second = str(combination[1]).split(";")[1]
        table_set = table.loc[(
            (table[category_first] == level_first) &
            (table[category_second] == level_second)
        ), :].copy(deep=True)
        samples_set = copy.deepcopy(
            table_set[column_sample_identifier].to_list()
        )
        record_set = dict()
        record_set["name"] = str(
            category_first + ":" + level_first + ";" +
            category_second + ":" + level_second
        )
        record_set[category_first] = level_first
        record_set[category_second] = level_second
        record_set["categories"] = [category_first, category_second,]
        record_set["samples"] = samples_set
        records_sets.append(record_set)
        pass

    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.interaction.py")
        function = "extract_table_sample_sets_by_two_categories_two_levels()"
        print("function: " + function)
        #putly.print_terminal_partition(level=4)
        #print(list(categories_levels_flat))
        #print(combinations)
        putly.print_terminal_partition(level=4)
        for record in records_sets:
            count_samples = int(len(record["samples"]))
            #categories = list(filter(
            #    lambda key: (str(key) not in ["samples",]),
            #    list(record.keys())
            #))
            for category in record["categories"]:
                print(str(category + ": " + str(record[category])))
                pass
            print(str("count samples: " + str(count_samples)))
            putly.print_terminal_partition(level=5)
            pass
        putly.print_terminal_partition(level=4)
    # Return information.
    return records_sets


def extract_gene_signal_sets_by_two_categories_two_levels(
    identifier_gene=None,
    column_gene_identifier=None,
    sets_samples=None,
    table=None,
    report=None,
):
    """
    Extract and describe by basic statistics sets of signals corresponding to
    sets of samples.

    arguments:
        identifier_gene (str): identifier of a gene
        column_gene_identifier (str): name of column in tables for
            identifiers that correspond to genes and their signals
        sets_samples (list<dict<str>>): records of information about each set
            of samples that includes the categories and their levels which
            define these sets
        table (object): Pandas data-frame table of values of signal intensity
            for genes across rows and samples across columns
        report (bool): whether to print reports

    raises:

    returns:
        (list<dict<str>>): records of information about each set of samples and
            signals that includes the categories and their levels which define
            these sets


    """

    # Copy information in table.
    table = table.copy(deep=True)
    # Copy other information.
    sets_samples = copy.deepcopy(sets_samples)

    # Organize indices in table.
    table.reset_index(
        level=None,
        inplace=True,
        drop=False, # remove index; do not move to regular columns
    )
    # Extract signals for specific gene.
    table_gene = table.loc[(
        (table[column_gene_identifier] == identifier_gene)
    ), :].copy(deep=True)
    # Organize indices in table.
    table_gene.set_index(
        [column_gene_identifier],
        append=False,
        drop=True,
        inplace=True,
    )
    series_gene = table_gene.iloc[0, :]

    # Extract and describe by basic statistics sets of signals corresponding to
    # sets of samples.
    records_sets = list()
    for set in sets_samples:
        # Extract and organize information from series.
        values_raw = series_gene[set["samples"]].dropna().to_numpy(
            dtype="float64",
            na_value=numpy.nan,
            copy=True,
        )
        values_nonmissing = numpy.copy(values_raw[~numpy.isnan(values_raw)])
        record_set = copy.deepcopy(set)
        record_set["signals"] = values_nonmissing
        # Determine mean, median, standard deviation, and standard error of
        # values in array.
        record_set["mean"] = numpy.nanmean(values_nonmissing)
        record_set["standard_error"] = scipy.stats.sem(
            values_nonmissing,
            ddof=1, # divisor is (n - 1) for sample standard deviation
            nan_policy="omit", # ignore missing values in calculation
        )
        record_set["standard_deviation"] = numpy.nanstd(
            values_nonmissing,
            ddof=1, # divisor is (n - 1) for sample standard deviation
        )
        record_set["median"] = numpy.nanmedian(values_nonmissing)
        record_set["interquartile"] = scipy.stats.iqr(
            values_nonmissing,
            rng=(25, 75),
            nan_policy="omit", # ignore missing values in calculation.
        )
        record_set["minimum"] = numpy.nanmin(values_nonmissing)
        record_set["maximum"] = numpy.nanmax(values_nonmissing)
        pail_95 = pdesc.calculate_confidence_interval_range(
            confidence=0.95,
            standard_error=record_set["standard_error"],
            estimate=record_set["mean"],
        )
        record_set["range_95_low"] = pail_95["minimum"]
        record_set["range_95_high"] = pail_95["maximum"]
        # Collect information.
        records_sets.append(record_set)
        pass

    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.interaction.py")
        function = "extract_gene_signal_sets_by_two_categories_two_levels()"
        print("function: " + function)
    # Return information.
    return records_sets



def define_sequence_columns_table_interaction(
    columns_gene=None,
    names_sets=None,
):
    """
    Defines names of columns in sequence by which to filter and sort columns in
    a table.

    This list represents the columns that are novel derivations of the original
    columns.

    arguments:
        columns_gene (list<str>): names of columns in gene table to transfer
        names_sets (list<str>): names for sets of samples and their signals

    raises:

    returns:
        (list<str>): names of columns in sequence by which to filter and sort
            columns in table

    """

    # Copy other information.
    columns_gene = copy.deepcopy(columns_gene)
    names_sets = copy.deepcopy(names_sets)

    # Determine names of columns for statistics.
    statistics = [
        "mean",
        "error",
        #"median",
        #"interquartile",
    ]
    columns_sets_statistics = list()
    for name_set in names_sets:
        for statistic in statistics:
            columns_sets_statistics.append(str(name_set + "_" + statistic))
            pass
        pass

    # Specify sequence of columns within table.
    columns_sequence = copy.deepcopy(columns_gene)
    columns_sequence.extend(columns_sets_statistics)
    columns_sequence.append("p_value_interaction")
    columns_sequence.append("q_value_interaction")
    # Return information.
    return columns_sequence




def create_table_interaction_by_two_categories_two_levels(
    name_instance=None,
    identifiers_gene=None,
    column_category_first=None,
    column_category_second=None,
    column_sample_identifier=None,
    column_gene_identifier=None,
    columns_gene=None,
    column_interaction_pvalue=None,
    column_interaction_qvalue=None,
    levels_category_first=None,
    levels_category_second=None,
    z_score=None,
    method_signal_aggregation=None,
    table_sample=None,
    table_gene=None,
    table_signal=None,
    table_interaction=None,
    report=None,
):
    """
    Create table to summarize the interaction in multiple gene's signals
    between samples with two level values each of two categorical variables.

    gene mean_set_1 mean_set_2 mean_set_3 mean_set_4 p_value_interaction
    ...  ...        ...        ...        ...        ...
    ...  ...        ...        ...        ...        ...
    ...  ...        ...        ...        ...        ...
    ...  ...        ...        ...        ...        ...
    ...  ...        ...        ...        ...        ...

    arguments:
        name_instance (str): name for instance set of genes parameters for
            summary
        identifiers_gene (list<str>): identifiers of genes
        column_category_first (str): name of column in sample table for first
            categorical variable
        column_category_second (str): name of column in sample table for second
            categorical variable
        column_sample_identifier (str): name of column in tables for
            identifiers that correspond to samples and their signals
        column_gene_identifier (str): name of column in tables for
            identifiers that correspond to genes and their signals
        columns_gene (list<str>): names of columns in gene table to transfer
        column_interaction_pvalue (str): name of column in interaction table
            for p-value corresponding to interaction between levels of the
            first and second categorical variables
        column_interaction_qvalue (str): name of column in interaction table
            for q-value corresponding to interaction between levels of the
            first and second categorical variables
        levels_category_first (list<str>): levels, names, or values of first
            categorical variable
        levels_category_second (list<str>): levels, names, or values of second
            categorical variable
        z_score (bool): whether to transform to z-scores to standardize
            distribution of values of signal intensity for each gene across
            samples
        method_signal_aggregation (str): method for the aggregation of values
            of signal for each gene across samples in each group or set; either
            'mean' or 'median'
        table_sample (object): Pandas data-frame table of properties or
            attributes of samples
        table_gene (object): Pandas data-frame table of properties or
            attributes of genes
        table_signal (object): Pandas data-frame table of values of signal
            intensity for genes across rows and samples across columns
        table_interaction (object): Pandas data-frame table of statistics
            describing interaction in a single gene's signals between sets of
            samples corresponding to the same level values of categorical
            variables
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data-frame table

    """

    # Copy information in table.
    table_sample = table_sample.copy(deep=True)
    table_gene = table_gene.copy(deep=True)
    table_signal = table_signal.copy(deep=True)
    table_interaction = table_interaction.copy(deep=True)
    # Copy other information.
    columns_gene = copy.deepcopy(columns_gene)


    # Extract identifiers of samples in sets corresponding to all unique
    # combinations of level values of categorical variables.
    categories_levels = dict()
    categories_levels[column_category_first] = levels_category_first
    categories_levels[column_category_second] = levels_category_second
    sets_samples = extract_sample_sets_by_two_categories_two_levels(
        categories_levels=categories_levels,
        column_sample_identifier=column_sample_identifier,
        table=table_sample,
        report=report,
    )
    # Collect unique identifiers of samples in all sets.
    samples_all = list()
    for set in sets_samples:
        samples_all.extend(copy.deepcopy(set["samples"]))
        pass
    samples_all_unique = putly.collect_unique_elements(
        elements=samples_all,
    )

    # Prepare information in table of values of signal intensity for genes
    # across samples.
    # Filter rows in signal table to keep only relevant genes.
    table_signal = table_signal.loc[
        table_signal.index.isin(identifiers_gene), :
    ].copy(deep=True)
    # Filter columns in signal table to keep only relevant samples.
    # Signal table must have column "identifier_gene" set as index.
    #table_signal = table_signal.loc[
    #    :, table_signal.columns.isin(samples_all_unique)
    #].copy(deep=True)
    table_signal = table_signal.filter(
        items=samples_all_unique,
        axis="columns",
    )
    # Determine whether to transform to z-scores to standardize distribution of
    # values of signal intensity for each gene across samples.
    if z_score:
        # Calculate the standard z-score of signal intensity values for each
        # gene across samples.
        table_signal = pscl.transform_standard_z_score_by_table_rows(
            table=table_signal,
            report=report,
        )

    # Collect records of information, which will become rows in table.
    records = list()
    # Iterate on genes.
    for identifier_gene in identifiers_gene:
        # Collect information.
        record = dict()
        record["gene_identifier"] = identifier_gene
        # Extract information about gene.
        for column_gene in columns_gene:
            record[column_gene] = str(
                table_gene.at[identifier_gene, column_gene]
            )
            pass
        # Extract p-value of interaction.
        record["p_value_interaction"] = str(
            table_interaction.at[identifier_gene, column_interaction_pvalue]
        )
        record["q_value_interaction"] = str(
            table_interaction.at[identifier_gene, column_interaction_qvalue]
        )
        # Extract values of signal intensity from sets of samples corresponding
        # to all unique combinations of level values of categorical variables.
        sets_signals = extract_gene_signal_sets_by_two_categories_two_levels(
            identifier_gene=identifier_gene,
            column_gene_identifier=column_gene_identifier,
            sets_samples=sets_samples,
            table=table_signal,
            report=False,
        )
        # Collect information.
        names_sets = list()
        # Iterate on sets.
        for set_signal in sets_signals:
            # Determine name for set of samples and signals.
            #category_first = set_signal["categories"][0]
            #category_second = set_signal["categories"][1]
            #level_first = set_signal[category_first]
            #level_second = set_signal[category_second]
            name_set = set_signal["name"]
            names_sets.append(name_set)
            # Collect information.
            record[str(name_set + "_mean")] = set_signal["mean"]
            record[str(name_set + "_error")] = set_signal["standard_error"]
            record[str(name_set + "_median")] = set_signal["median"]
            record[str(name_set + "_interquartile")] = (
                set_signal["interquartile"]
            )

            pass
        # Collect information.
        records.append(record)
        pass

    # Organize information in a table.
    table = pandas.DataFrame(data=records)
    # Filter and sort columns within table.
    columns_sequence = define_sequence_columns_table_interaction(
        columns_gene=columns_gene,
        names_sets=names_sets,
    )
    columns_sequence.insert(0, "gene_identifier")
    table = porg.filter_sort_table_columns(
        table=table,
        columns_sequence=columns_sequence,
        report=report,
    )

    print(table)


    # TODO: TCW; 2 October 2024
    # 1. include parameters for translation abbreviations of the category names
    # 2. write the table to file.
    # 3. create heatmap



    pass





###############################################################################
# Procedure



##########
# Control procedure within branch for parallelization.





##########
# Call main procedure.


def execute_procedure(
    path_directory_dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        path_directory_dock (str): path to dock directory for procedure's
            source and product directories and files

    raises:

    returns:

    """

    ##########
    # Parameters.
    project="exercise"
    routine="transcriptomics"
    procedure="interaction"
    report = True

    ##########
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.interaction.py")
        print("function: execute_procedure()")
        putly.print_terminal_partition(level=5)
        print("system: local")
        print("project: " + str(project))
        print("routine: " + str(routine))
        print("procedure: " + str(procedure))
        putly.print_terminal_partition(level=5)
        pass

    # TODO: TCW; 1 October 2024
    # Begin with demonstration use case...

    # Define path to file for table of information about samples.
    file_sample = "table_sample.pickle"
    path_file_source_sample = os.path.join(
        path_directory_dock,
        "out_exercise",
        "transcriptomics",
        "organize_signal",
        "parts",
        "adipose",
        "adipose_5_visit-first_interaction-age-sex",
        "data",
        file_sample,
    )
    # Define path to files for tables of information about genes and signals.
    file_gene = "table_gene_adipose.pickle"
    file_signal = "table_signal_adipose.pickle"
    path_file_source_gene = os.path.join(
        path_directory_dock,
        "out_exercise",
        "transcriptomics",
        "organize_signal",
        "whole",
        "preparation",
        file_gene,
    )
    path_file_source_signal = os.path.join(
        path_directory_dock,
        "out_exercise",
        "transcriptomics",
        "organize_signal",
        "whole",
        "preparation",
        file_signal,
    )
    # Define path to file for table of interaction statistics.
    file_interaction = "table_adipose_5_visit-first_interaction-age-sex.pickle"
    path_file_source_interaction = os.path.join(
        path_directory_dock,
        "out_exercise",
        "transcriptomics",
        "select_gene_sets",
        "data",
        "pickle",
        file_interaction,
    )


    #path_file_source_sample (str): path to file for source table of
    #    information about samples and their properties or attributes
    #path_file_source_gene (str): path to file for source table of
    #    information about genes and their properties or attributes
    #path_file_source_signal (str): path to file for source table of
    #    values of signal for genes across samples
    #path_file_source_interaction (str): path to file for source table of
    #    statistics describing interaction in a gene's signals between
    #    samples with the same level values of the categorical variables
    #path_file_product (str): path to file for product table

    # TODO: TCW; 2 October 2024
    # TODO: need to write the interaction tables to 'pickle' format.

    # Read source files.
    table_sample = pandas.read_pickle(
        path_file_source_sample,
    )
    table_gene = pandas.read_pickle(
        path_file_source_gene,
    )
    table_signal = pandas.read_pickle(
        path_file_source_signal,
    )
    table_interaction = pandas.read_pickle(
        path_file_source_interaction,
    )

    ##########
    # Filter rows in sample table by inclusion and by tissue.
    # This step is unnecessary when using the specific version of the sample
    # table after stratification for analysis.
    if False:
        tissue = "adipose"
        table_sample["inclusion"] = table_sample["inclusion"].astype("str")
        table_sample = table_sample.loc[
            (table_sample["inclusion"] == "1"), :
        ].copy(deep=True)
        table_sample = table_sample.loc[
            (table_sample["tissue"] == tissue), :
        ].copy(deep=True)

    ##########
    # Create table to summarize interactions between sets of samples.
    table_summary = create_table_interaction_by_two_categories_two_levels(
        name_instance="test_adipose_5_visit-first_interaction-age-sex",
        identifiers_gene=[
            "ENSG00000101405",
            "ENSG00000100344",
            "ENSG00000146674",
            "ENSG00000164530",
            "ENSG00000183785",
            "ENSG00000196169",
            "ENSG00000183671",
            "ENSG00000176387",
            "ENSG00000196208",
            "ENSG00000099337",
            "ENSG00000114737",
        ],
        column_category_first="cohort_age_text",
        column_category_second="sex_text",
        column_sample_identifier="identifier_signal",
        column_gene_identifier="identifier_gene",
        columns_gene=["gene_name", "gene_type", "gene_chromosome",],
        column_interaction_pvalue="p_value_fill",
        column_interaction_qvalue="q_value_fill",
        levels_category_first=["elder", "younger",],
        levels_category_second=["male", "female",],
        z_score=True,
        method_signal_aggregation="mean", # "mean" or "median"
        table_sample=table_sample,
        table_gene=table_gene,
        table_signal=table_signal,
        table_interaction=table_interaction,
        report=report,
    )


    pass


###############################################################################
# End
