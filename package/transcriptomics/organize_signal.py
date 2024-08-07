"""
Supply functionality for process and analysis of data from transcriptomics.

This module 'organize_sample' is part of the 'transcriptomics' package within
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

###############################################################################
# Functionality


##########
# 1. Initialize directories for read of source and write of product files.


def preinitialize_directories(
    project=None,
    routine=None,
    procedure=None,
    path_directory_dock=None,
    restore=None,
    report=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        project (str): name of project
        routine (str): name of routine, either 'transcriptomics' or
            'proteomics'
        procedure (str): name of procedure, a set or step in the routine
            process
        path_directory_dock (str): path to dock directory for procedure's
            source and product directories and files
        restore (bool): whether to remove previous versions of data
        report (bool): whether to print reports

    raises:

    returns:
        (dict<str>): collection of paths to directories for procedure's files

    """

    # Collect paths.
    paths = dict()
    # Define paths to directories.
    paths["dock"] = path_directory_dock
    paths["out_project"] = os.path.join(
        paths["dock"], str("out_" + project),
    )
    paths["out_routine"] = os.path.join(
        paths["out_project"], str(routine),
    )
    paths["out_procedure"] = os.path.join(
        paths["out_routine"], str(procedure),
    )
    # Initialize directories in main branch.
    paths_initialization = [
        #paths["out_project"],
        #paths["out_routine"],
        paths["out_procedure"],
    ]
    # Remove previous directories and files to avoid version or batch
    # confusion.
    if restore:
        for path in paths_initialization:
            putly.remove_directory(path=path) # caution
            pass
    # Create directories.
    for path in paths_initialization:
        putly.create_directories(
            path=path,
        )
        pass
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organize_signal.py")
        print("function: preinitialize_directories()")
        putly.print_terminal_partition(level=5)
        print("path to dock directory for procedure's files: ")
        print(path_directory_dock)
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return paths


def initialize_directories(
    project=None,
    routine=None,
    procedure=None,
    tissue=None,
    name_set=None,
    path_directory_dock=None,
    restore=None,
    report=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        project (str): name of project
        routine (str): name of routine, either 'transcriptomics' or
            'proteomics'
        procedure (str): name of procedure, a set or step in the routine
            process
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        name_set (str): name for instance of rules for selection
        path_directory_dock (str): path to dock directory for procedure's
            source and product directories and files
        restore (bool): whether to remove previous versions of data
        report (bool): whether to print reports

    raises:

    returns:
        (dict<str>): collection of paths to directories for procedure's files

    """

    # Collect paths.
    paths = dict()
    # Define paths to directories.
    paths["dock"] = path_directory_dock
    paths["in_data"] = os.path.join(
        paths["dock"], "in_data", str(project), str(routine),
    )
    paths["in_parameters"] = os.path.join(
        paths["dock"], "in_parameters", str(project), str(routine),
    )
    paths["in_parameters_private"] = os.path.join(
        paths["dock"], "in_parameters_private", str(project), str(routine),
    )
    paths["out_project"] = os.path.join(
        paths["dock"], str("out_" + project),
    )
    paths["out_routine"] = os.path.join(
        paths["out_project"], str(routine),
    )
    paths["out_procedure"] = os.path.join(
        paths["out_routine"], str(procedure),
    )
    paths["out_tissue"] = os.path.join(
        paths["out_procedure"], str(tissue),
    )
    paths["out_set"] = os.path.join(
        paths["out_tissue"], str(name_set),
    )
    #paths["out_test"] = os.path.join(
    #    paths["out_set"], "test",
    #)
    paths["out_data"] = os.path.join(
        paths["out_set"], "data",
    )
    #paths["out_plot"] = os.path.join(
    #    paths["out_set"], "plot",
    #)
    # Initialize directories in main branch.
    paths_initialization = [
        #paths["out_project"],
        #paths["out_routine"],
        #paths["out_procedure"], # omit to avoid conflict in parallel branches
        #paths["out_tissue"], # omit to avoid conflict in parallel branches
        paths["out_set"],
        paths["out_data"],
    ]
    # Remove previous directories and files to avoid version or batch
    # confusion.
    if restore:
        for path in paths_initialization:
            putly.remove_directory(path=path) # caution
            pass
    # Create directories.
    for path in paths_initialization:
        putly.create_directories(
            path=path,
        )
        pass
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organize_signal.py")
        print("function: initialize_directories()")
        putly.print_terminal_partition(level=5)
        print("path to dock directory for procedure's files: ")
        print(path_directory_dock)
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return paths


##########
# 2. Read source information from file.


def define_column_types_table_sample():
    """
    Defines the variable types of columns within table for attributes of
    samples.

    Review: TCW; 24 June 2024

    arguments:

    raises:

    returns:
        (dict<str>): variable types of columns within table

    """

    # Specify variable types of columns within table.
    types_columns = dict()
    types_columns["inclusion"] = "int32"
    types_columns["identifier"] = "string"
    types_columns["path_file"] = "string"
    types_columns["sample_plate"] = "string"
    types_columns["plate"] = "string"
    types_columns["sample"] = "string"
    types_columns["sample_plate"] = "string"
    types_columns["condition_code"] = "string"
    types_columns["tissue"] = "string"
    types_columns["condition"] = "string"
    types_columns["subject"] = "string"
    types_columns["note_condition"] = "string"
    #types_columns["sex"] = "string"
    #types_columns["age"] = "int32"
    #types_columns["body_mass"] = "float32"
    #types_columns["body_mass_index"] = "float32"
    # Return information.
    return types_columns


def define_column_types_table_sample_attribute():
    """
    Defines the variable types of columns within table for attributes of
    samples.

    Review: TCW; 30 July 2024

    arguments:

    raises:

    returns:
        (dict<str>): variable types of columns within table

    """

    # Specify variable types of columns within table.
    types_columns = dict()
    types_columns["Name"] = "string"
    types_columns["Visit"] = "string"
    types_columns["Date"] = "string"
    types_columns["Age Group"] = "string"
    types_columns["Sex"] = "string"
    types_columns["Intervention"] = "string"
    types_columns["Age"] = "int32"
    types_columns["BMI (kg/m2)"] = "float32"
    types_columns["Total % Fat"] = "float32"
    types_columns["Total Fat Mass"] = "float32"
    types_columns["Lean Mass"] = "float32"
    # ...
    # Return information.
    return types_columns


def define_column_types_table_main():
    """
    Defines the variable types of columns within table for values of intensity.

    Review: TCW; 24 June 2024

    arguments:

    raises:

    returns:
        (dict<str>): variable types of columns within table

    """

    # Specify variable types in columns within table.
    types_columns = dict()
    types_columns["identifier_gene"] = "string"
    types_columns["gene_id"] = "string"
    types_columns["gene_name"] = "string"
    types_columns["exon_number"] = "string"
    types_columns["gene_type"] = "string"
    types_columns["chromosome"] = "string"
    # Return information.
    return types_columns


def read_source(
    paths=None,
    tissue=None,
    report=None,
):
    """
    Reads and organizes source information from file.

    Notice that Pandas does not accommodate missing values within series of
    integer variable types.

    arguments:
        paths : (dict<str>): collection of paths to directories for procedure's
            files
        tissue (str): name of tissue, either 'adipose' or 'muscle', which
            distinguishes study design and sets of samples
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of source information read from file

    """

    # Define paths to parent directories.
    #paths["in_data"]
    #paths["in_parameters"]

    # Define paths to child files.
    print(paths["out_routine"])
    path_file_table_sample = os.path.join(
        paths["out_routine"], "organize_sample", "data",
        "table_sample.pickle",
    )
    if (tissue == "adipose"):
        path_file_table_main = os.path.join(
            paths["in_data"], "quantification_2024-07-14",
            "organization", "quantification_rna_reads_gene_adipose.tsv",
        )
    elif (tissue == "muscle"):
        path_file_table_main = os.path.join(
            paths["in_data"], "quantification_2024-07-14",
            "organization", "quantification_rna_reads_gene_muscle.tsv",
        )
        pass

    # Collect information.
    pail = dict()
    # Read information from file.

    # Table of samples and their attributes.
    pail["table_sample"] = pandas.read_pickle(
        path_file_table_sample,
    )

    # Table of values of intensity across samples and proteins.
    types_columns = define_column_types_table_main()
    pail["table_main"] = pandas.read_csv(
        path_file_table_main,
        sep="\t",
        header=0,
        dtype=types_columns,
        na_values=[
            "nan", "na", "NAN", "NA", "<nan>", "<na>", "<NAN>", "<NA>",
        ],
        encoding="utf-8",
    )
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: read_source()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=5)
        print("sample table: ")
        print(pail["table_sample"])
        putly.print_terminal_partition(level=5)
        count_rows = (pail["table_main"].shape[0])
        count_columns = (pail["table_main"].shape[1])
        print("main table: ")
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        print(pail["table_main"])
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return pail


##########
# 3. Select set of samples for specific analyses.


def select_sets_identifier_table_sample(
    table_sample=None,
    name_set=None,
    tissue=None,
    cohort_selection=None,
    factor_availability=None,
    report=None,
):
    """
    Selects sets of samples relevant to specific analyses.

    This function preserves the original sequence of samples from the source
    table in its extraction of identifiers. It is important to preserve the
    definitive sequence of samples from the table of their attributes as this
    sequence will determine the sort sequence of values in the table of
    signals, which must correspond exactly to the table of samples.

    arguments:
        table_sample (object): Pandas data-frame table of information about
            samples that correspond to signals within accompanying main table
        name_set (str): name for instance of rules for selection
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        cohort_selection (dict<list<str>>): filters on rows in table for
            selection of samples relevant to cohort for analysis
        factor_availability (dict<list<str>>): features and their values
            corresponding to factors of interest in the analysis
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of information

    """

    # Copy information in table.
    table_sample = table_sample.copy(deep=True)
    # Copy other information.
    cohort_selection = copy.deepcopy(cohort_selection)
    factor_availability = copy.deepcopy(factor_availability)

    # Translate names of columns.
    translations = dict()
    translations["identifier_signal"] = "identifier"
    table_sample.rename(
        columns=translations,
        inplace=True,
    )

    # Filter rows in table for selection of relevant samples.
    # Filter by inclusion indicator.
    table_inclusion = table_sample.loc[
        (table_sample["inclusion"] == 1), :
    ].copy(deep=True)
    # Separate information about sets of samples for difference experimental
    # conditions or groups.
    table_tissue = table_inclusion.loc[
        (table_inclusion["tissue"] == tissue), :
    ].copy(deep=True)
    #table_factor = table_tissue.loc[
    #    (
    #        (table_tissue["condition"] == "control") |
    #        (table_tissue["condition"] == "intervention_1")
    #    ), :
    #].copy(deep=True)

    # Filter rows in table by rules for selection of a specific set.
    # Iterate on features and values for selection of samples in cohort.
    table_cohort = table_inclusion.copy(deep=True)
    for feature in cohort_selection.keys():
        table_cohort = table_cohort.loc[(
            table_cohort[feature].isin(cohort_selection[feature])
        ), :].copy(deep=True)
    # Iterate on factors and values for selection of samples on the basis
    # of availability.
    table_factor = table_cohort.copy(deep=True)
    for factor in factor_availability.keys():
        table_factor = table_factor.loc[(
            table_factor[factor].isin(factor_availability[factor])
        ), :].copy(deep=True)
    table_selection = table_factor.copy(deep=True)
    # Separate samples for unique values of factor.
    # This operation would necessarily assume that there were two and only two
    # unique values of a single factor.
    # table_control =
    # table_case =

    # Extract identifiers of samples in separate groups.
    samples_inclusion = copy.deepcopy(
        table_inclusion["identifier"].to_list()
    )
    samples_tissue = copy.deepcopy(
        table_tissue["identifier"].to_list()
    )
    samples_selection = copy.deepcopy(
        table_selection["identifier"].to_list()
    )

    # Organize indices in tables.
    tables = [
        table_inclusion,
        table_tissue,
        table_selection,
    ]
    for table in tables:
        table.reset_index(
            level=None,
            inplace=True,
            drop=True, # remove index; do not move to regular columns
        )
        table.set_index(
            ["identifier"],
            append=False,
            drop=True,
            inplace=True,
        )
        pass

    # Collect information.
    pail = dict()
    pail["table_inclusion"] = table_inclusion
    pail["table_tissue"] = table_tissue
    pail["table_selection"] = table_selection
    pail["samples_inclusion"] = samples_inclusion
    pail["samples_tissue"] = samples_tissue
    pail["samples_selection"] = samples_selection

    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: select_sets_identifier_table_sample()")
        print("name_set: " + str(name_set))
        print("tissue: " + tissue)
        print("features for cohort selection:")
        print(str(cohort_selection.keys()))
        print("factors for availability of specific values:")
        print(str(factor_availability.keys()))
        putly.print_terminal_partition(level=5)
        print("sample table, filtered by inclusion and tissue:")
        print(table_tissue.iloc[0:10, 0:])
        putly.print_terminal_partition(level=5)
        print("sample table, filtered by set selection rules:")
        print(table_selection.iloc[0:10, 0:])
        #putly.print_terminal_partition(level=5)
        #print("description of first categorical factor:")
        #print("first factor: " + str(factor_availability.keys()[0]))
        #table_selection[list(factor_availability.keys())[0]].describe(
        #    include=["category",]
        #)
        putly.print_terminal_partition(level=4)
        print(
            "counts of samples with each unique categorical value of each " +
            "factor:"
        )
        for factor in factor_availability.keys():
            print("factor: " + factor)
            print(
                table_selection[factor].value_counts(
                    dropna=False,
                )
            )
            putly.print_terminal_partition(level=4)
            pass
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return pail


##########
# 4. Organize information from source.


def define_column_sequence_table_main_gene():
    """
    Defines the columns in sequence within table.

    arguments:

    raises:

    returns:
        (list<str>): variable types of columns within table

    """

    # Specify sequence of columns within table.
    columns_sequence = [
        "identifier_gene",
        "gene_identifier",
        "gene_name",
        #"gene_exon_number",
        "gene_type",
        "gene_chromosome",
        #"Unnamed: 160",
    ]
    # Return information.
    return columns_sequence


def organize_table_main(
    table_main=None,
    columns_gene=None,
    samples=None,
    tissue=None,
    report=None,
):
    """
    Organizes information in tables about samples and measurement signals.

    arguments:
        table_main (object): Pandas data-frame table of values of signal
            intensity for sample observations across columns and for gene
            features across rows, with a few additional columns for attributes
            of gene features
        columns_gene (list<str>): names of columns corresponding to
            information about genes
        samples (list<str>): identifiers of samples corresponding to names of
            columns for measurement values of signal intensity across features
        tissue (str): name of tissue, either 'adipose' or 'muscle', which
            distinguishes study design and sets of samples
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of information

    """

    # Copy information in table.
    table_main = table_main.copy(deep=True)
    # Copy other information.
    columns_gene = copy.deepcopy(columns_gene)
    samples = copy.deepcopy(samples)

    # Translate names of columns.
    translations = dict()
    translations["gene_id"] = "gene_identifier"
    translations["exon_number"] = "gene_exon_number"
    translations["chromosome"] = "gene_chromosome"
    table_main.rename(
        columns=translations,
        inplace=True,
    )
    # Replace values of zero for signal intensity with missing values.
    # Only replace values within table's columns for samples.
    # This implementation is more concise than iteration across specific
    # columns.
    # This operation is inaccurate for quantification of RNA sequence read
    # data. In this case, it might even be more reasonable to replace missing
    # values with values of zero.
    #table_main[samples] = table_main[samples].replace(
    #    to_replace=0,
    #    value=pandas.NA,
    #)
    # Replace values less than zero with missing values.
    table_main[samples][table_main[samples] < 0] = pandas.NA

    # Filter and sort columns within table.
    columns_sequence = copy.deepcopy(columns_gene)
    columns_sequence.extend(samples)
    table_main = porg.filter_sort_table_columns(
        table=table_main,
        columns_sequence=columns_sequence,
        report=report,
    )

    # Collect information.
    pail = dict()
    pail["table_main"] = table_main
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: organize_table_main()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=5)
        print("main table: ")
        print(table_main.iloc[0:10, 0:])
        putly.print_terminal_partition(level=5)
        print("description of categorical gene type:")
        print(table_main["gene_type"].describe(include=["category",]))
        putly.print_terminal_partition(level=5)
        print(
            "counts of genes with each unique categorical value of "
            + "gene type:")
        print(table_main["gene_type"].value_counts(dropna=False))
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return pail


##########
# 5. Filter columns and rows in main table.


def define_keep_types_gene():
    """
    Defines the categorical types of genes for which to keep rows in the main
    table.

    Reference:
    https://www.gencodegenes.org/pages/biotypes.html

    arguments:

    raises:

    returns:
        (list<str>): types of gene to keep

    """

    # Specify categorical types.
    types_gene = [
        "protein_coding",
        "lncRNA",
        #"processed_pseudogene",
        #"unprocessed_pseudogene",
        "misc_RNA",
        "snRNA",
        "miRNA",
        "TEC",
        #"transcribed_unprocessed_pseudogene"
        "snoRNA",
        #"transcribed_processed_pseudogene",
        #"rRNA_pseudogene",
        #"IG_V_pseudogene",
        #"transcribed_unitary_pseudogene",
        "IG_V_gene",
        "TR_V_gene",
        #"unitary_pseudogene",
        "TR_J_gene",
        "rRNA",
        "scaRNA",
        "IG_D_gene",
        #"TR_V_pseudogene",
        "Mt_tRNA",
        #"artifact",
        "IG_J_gene",
        "IG_C_gene",
        #"IG_C_pseudogene",
        "ribozyme",
        "TR_C_gene",
        "sRNA",
        "TR_D_gene",
        #"pseudogene",
        "vault_RNA",
        #"TR_J_pseudogene",
        #"IG_J_pseudogene",
        "Mt_rRNA",
        #"translated_processed_pseudogene",
        "scRNA",
        #"IG_pseudogene",
    ]
    # Return information.
    return types_gene


def determine_keep_series_by_identity(
    row_identifier=None,
    row_type=None,
    identifier_prefix=None,
    types_gene=None,
):
    """
    Determines whether to keep a row from a table.

    arguments:
        row_identifier (str): current row's identifier of gene
        row_type (str): current row's type of gene
        identifier_prefix (str): prefix in identifier of gene to keep
        types_gene (list<str>): types of gene to keep

    raises:

    returns:
        (int): logical binary representation of whether to keep current row

    """

    # Determine whether to keep current row from table.
    #(any(row_type == type_gene for type_gene in types_gene))
    if (
        (pandas.notna(row_identifier)) and
        (len(str(row_identifier)) > 0) and
        (str(identifier_prefix) in str(row_identifier)) and
        (str(row_type) in types_gene)
    ):
        indicator = 1
    else:
        indicator = 0
        pass
    # Return information.
    return indicator


def filter_table_main_rows_signal(
    table_main=None,
    samples_all=None,
    samples_control=None,
    samples_intervention=None,
    filter_rows_signal_by_condition=None,
    threshold_signal_low=None,
    threshold_signal_high=None,
    proportion_signal_all=None,
    proportion_signal_control=None,
    proportion_signal_intervention=None,
    tissue=None,
    report=None,
):
    """
    Filters information in table for gene features across rows.

    This function filters rows for gene features by different thresholds on the
    proportion of a gene's signal intensities that must have non-missing,
    within-threshold, valid values across sets of samples in either the control
    or intervention experimental conditions or both. The reason for using these
    different thresholds is to allow genes to have signals that are detectable
    in only one experimental condition or the other. An example would be an
    experimental intervention that activates or deactivates transcriptional
    expression of specific genes.

    arguments:
        table_main (object): Pandas data-frame table of values of signal
            intensity for sample observations across columns and for gene
            features across rows, with a few additional columns for attributes
            of gene features
        samples_all (list<str>): identifiers of samples in both control and
            intervention experimental conditions corresponding to names of
            columns for measurement values of signal intensity across features
        samples_control (list<str>): identifiers of samples in control
            experimental condition corresponding to names of columns for
            measurement values of signal intensity across features
        samples_intervention (list<str>): identifiers of samples in
            intervention experimental condition corresponding to names of
            columns for measurement values of signal intensity across features
        filter_rows_signal_by_condition (bool): whether to filter rows by
            signal with separate consideration of columns for different
            experimental conditions
        threshold_signal_low (float): threshold below which
            (value <= threshold) all values are considered invalid and missing
        threshold_signal_high (float): threshold above which
            (value > threshold) all values are considered invalid and missing
        proportion_signal_all (float): proportion of signal intensities
            across all samples in any experimental condition that must have
            non-missing, within-threshold, valid values in order to keep the
            row for each gene feature
        proportion_signal_control (float): proportion of signal intensities
            across samples in control experimental condition that must have
            non-missing, within-threshold, valid values in order to keep the
            row for each gene feature
        proportion_signal_intervention (float): proportion of values of signal
            intensities across samples in intervention experimental condition
            that must have non-missing, within-threshold, valid values in
            order to keep the row for each gene feature
        tissue (str): name of tissue, either 'adipose' or 'muscle', which
            distinguishes study design and sets of samples
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data-frame table of values of intensity across
            samples in columns and proteins in rows

    """

    # Copy information in table.
    table_filter = table_main.copy(deep=True)
    # Copy other information.
    samples_all = copy.deepcopy(samples_all)
    samples_control = copy.deepcopy(samples_control)
    samples_intervention = copy.deepcopy(samples_intervention)

    # Collect names of temporary columns.
    names_columns_temporary = list()

    ##########
    # Filter rows in table on basis of signal validity.

    # Filter rows in table by signal validity across all samples.
    # porg.test_extract_organize_values_from_series()
    table_filter["match_keep_signal_all"] = table_filter.apply(
        lambda row:
            porg.determine_series_signal_validity_threshold(
                series=row,
                keys_signal=samples_all,
                threshold_low=threshold_signal_low,
                threshold_high=threshold_signal_high,
                proportion=proportion_signal_all,
                report=False,
            ),
        axis="columns", # apply function to each row
    )
    table_filter = table_filter.loc[
        (table_filter["match_keep_signal_all"] == 1), :
    ]
    names_columns_temporary.append("match_keep_signal_all")

    # Filter rows in table by signal validity across samples in control or
    # intervention experimental conditions, respectively.
    if filter_rows_signal_by_condition:
        table_filter["match_keep_signal_control"] = table_filter.apply(
            lambda row:
                porg.determine_series_signal_validity_threshold(
                    series=row,
                    keys_signal=samples_control,
                    threshold_low=threshold_signal_low,
                    threshold_high=threshold_signal_high,
                    proportion=proportion_signal_control,
                    report=False,
                ),
            axis="columns", # apply function to each row
        )
        table_filter["match_keep_signal_intervention"] = table_filter.apply(
            lambda row:
                porg.determine_series_signal_validity_threshold(
                    series=row,
                    keys_signal=samples_intervention,
                    threshold_low=threshold_signal_low,
                    threshold_high=threshold_signal_high,
                    proportion=proportion_signal_intervention,
                    report=False,
                ),
            axis="columns", # apply function to each row
        )
        table_filter = table_filter.loc[
            (
                (table_filter["match_keep_signal_control"] == 1) |
                (table_filter["match_keep_signal_intervention"] == 1)
            ), :
        ]
        names_columns_temporary.append("match_keep_signal_control")
        names_columns_temporary.append("match_keep_signal_intervention")
        pass

    # Remove unnecessary columns.
    table_filter.drop(
        labels=names_columns_temporary,
        axis="columns",
        inplace=True
    )

    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: filter_table_main_rows_signal()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return table_filter


def filter_table_main(
    table_main=None,
    columns_gene=None,
    samples_all=None,
    samples_control=None,
    samples_intervention=None,
    filter_rows_identity=None,
    filter_rows_signal=None,
    filter_rows_signal_by_condition=None,
    threshold_signal_low=None,
    threshold_signal_high=None,
    proportion_signal_all=None,
    proportion_signal_control=None,
    proportion_signal_intervention=None,
    tissue=None,
    report=None,
):
    """
    Filters information in table.

    This function filters rows for gene features by different thresholds on the
    proportion of a gene's signal intensities that must have non-missing,
    within-threshold, valid values across sets of samples in either the control
    or intervention experimental conditions or both. The reason for using these
    different thresholds is to allow genes to have signals that are detectable
    in only one experimental condition or the other. An example would be an
    experimental intervention that activates or deactivates transcriptional
    expression of specific genes.

    arguments:
        table_main (object): Pandas data-frame table of values of signal
            intensity for sample observations across columns and for gene
            features across rows, with a few additional columns for attributes
            of gene features
        columns_gene (list<str>): names of columns corresponding to
            information about genes
        samples_all (list<str>): identifiers of samples in both control and
            intervention experimental conditions corresponding to names of
            columns for measurement values of signal intensity across features
        samples_control (list<str>): identifiers of samples in control
            experimental condition corresponding to names of columns for
            measurement values of signal intensity across features
        samples_intervention (list<str>): identifiers of samples in
            intervention experimental condition corresponding to names of
            columns for measurement values of signal intensity across features
        filter_rows_identity (bool): whether to filter rows by identity
        filter_rows_signal (bool): whether to filter rows by signal
        filter_rows_signal_by_condition (bool): whether to filter rows by
            signal with separate consideration of columns for different
            experimental conditions
        threshold_signal_low (float): threshold below which
            (value <= threshold) all values are considered invalid and missing
        threshold_signal_high (float): threshold above which
            (value > threshold) all values are considered invalid and missing
        proportion_signal_all (float): proportion of signal intensities
            across all samples in any experimental condition that must have
            non-missing, within-threshold, valid values in order to keep the
            row for each gene feature
        proportion_signal_control (float): proportion of signal intensities
            across samples in control experimental condition that must have
            non-missing, within-threshold, valid values in order to keep the
            row for each gene feature
        proportion_signal_intervention (float): proportion of values of signal
            intensities across samples in intervention experimental condition
            that must have non-missing, within-threshold, valid values in
            order to keep the row for each gene feature
        tissue (str): name of tissue, either 'adipose' or 'muscle', which
            distinguishes study design and sets of samples
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data-frame table of values of intensity across
            samples in columns and proteins in rows

    """

    # Copy information in table.
    table_filter = table_main.copy(deep=True)
    # Copy other information.
    columns_gene = copy.deepcopy(columns_gene)
    samples_all = copy.deepcopy(samples_all)
    samples_control = copy.deepcopy(samples_control)
    samples_intervention = copy.deepcopy(samples_intervention)

    # Filter information in table.

    ##########
    # Filter rows within table on basis of gene feature identity.
    if filter_rows_identity:
        types_gene = define_keep_types_gene()
        table_filter["match_keep_identity"] = table_filter.apply(
            lambda row:
                determine_keep_series_by_identity(
                    row_identifier=row["identifier_gene"],
                    row_type=row["gene_type"],
                    identifier_prefix="ENSG",
                    types_gene=types_gene,
                ),
            axis="columns", # apply function to each row
        )
        table_filter = table_filter.loc[
            (table_filter["match_keep_identity"] == 1), :
        ]
        # Remove unnecessary columns.
        table_filter.drop(
            labels=["match_keep_identity",],
            axis="columns",
            inplace=True
        )
        pass

    ##########
    # Filter rows within table on basis of signal validity.
    if filter_rows_signal:
        table_filter = filter_table_main_rows_signal(
            table_main=table_filter,
            samples_all=samples_all,
            samples_control=samples_control,
            samples_intervention=samples_intervention,
            filter_rows_signal_by_condition=filter_rows_signal_by_condition,
            threshold_signal_low=threshold_signal_low,
            threshold_signal_high=threshold_signal_high,
            proportion_signal_all=proportion_signal_all,
            proportion_signal_control=proportion_signal_control,
            proportion_signal_intervention=proportion_signal_intervention,
            tissue=tissue,
            report=report,
        )
        pass

    ##########
    # Filter and sort columns within table.
    columns_sequence = copy.deepcopy(columns_gene)
    #columns_sequence.extend(samples_control)
    #columns_sequence.extend(samples_intervention)
    columns_sequence.extend(samples_all)
    table_filter = porg.filter_sort_table_columns(
        table=table_filter,
        columns_sequence=columns_sequence,
        report=report,
    )

    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: filter_table_main()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=5)
        print("source main table:")
        count_rows = (table_main.shape[0])
        count_columns = (table_main.shape[1])
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        print(table_main)
        putly.print_terminal_partition(level=5)
        print("product main table:")
        print(table_filter)
        putly.print_terminal_partition(level=5)
        count_rows = (table_filter.shape[0])
        count_columns = (table_filter.shape[1])
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        putly.print_terminal_partition(level=5)
        print("description of categorical gene type:")
        print(table_filter["gene_type"].describe(include=["category",]))
        putly.print_terminal_partition(level=5)
        print(
            "counts of genes with each unique categorical value of "
            + "gene type:")
        print(table_filter["gene_type"].value_counts(dropna=False))
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return table_filter


##########
# 6. Separate tables for information of distinct types.


def separate_table_main_columns(
    table_main=None,
    columns_gene=None,
    columns_signal=None,
    tissue=None,
    report=None,
):
    """
    Splits or separates information in table by columns.

    arguments:
        table_main (object): Pandas data-frame table of values of signal
            intensity for sample observations across columns and for gene
            features across rows, with a few additional columns for attributes
            of gene features
        columns_gene (list<str>): names of columns corresponding to
            information about genes
        columns_signal (list<str>): names of columns corresponding to
            identifiers of samples in both control and intervention
            experimental conditions for measurement values of signal intensity
            across features
        tissue (str): name of tissue, either 'adipose' or 'muscle', which
            distinguishes study design and sets of samples
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of information

    """

    # Copy information in table.
    table_split = table_main.copy(deep=True)
    # Copy other information.
    columns_gene = copy.deepcopy(columns_gene)
    columns_signal = copy.deepcopy(columns_signal)
    # Separate information into separate tables.
    #columns_gene.remove("identifier_gene")
    columns_signal.insert(0, "identifier_gene")
    table_gene = table_split.loc[
        :, table_split.columns.isin(columns_gene)
    ].copy(deep=True)
    table_signal = table_split.loc[
        :, table_split.columns.isin(columns_signal)
    ].copy(deep=True)
    # Translate names of columns.
    translations = dict()
    translations["identifier_gene"] = "identifier"
    table_gene.rename(
        columns=translations,
        inplace=True,
    )
    # Organize indices in table.
    table_gene.reset_index(
        level=None,
        inplace=True,
        drop=True, # remove index; do not move to regular columns
    )
    table_signal.reset_index(
        level=None,
        inplace=True,
        drop=True, # remove index; do not move to regular columns
    )
    table_gene.set_index(
        ["identifier"],
        append=False,
        drop=True,
        inplace=True,
    )
    table_signal.set_index(
        ["identifier_gene"],
        append=False,
        drop=True,
        inplace=True,
    )
    # Organize indices in table.
    table_gene.columns.rename(
        "attribute",
        inplace=True,
    ) # single-dimensional index
    table_signal.columns.rename(
        "sample",
        inplace=True,
    ) # single-dimensional index

    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: separate_table_main_columns()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=5)
        print("source main table:")
        count_rows = (table_split.shape[0])
        count_columns = (table_split.shape[1])
        print("count of rows in table: " + str(count_rows))
        print("count of columns in table: " + str(count_columns))
        print(table_main.iloc[0:10, 0:])
        putly.print_terminal_partition(level=5)
        count_rows = (table_gene.shape[0])
        count_columns = (table_gene.shape[1])
        print("table of information about genes:")
        print(table_gene.iloc[0:10, 0:])
        print("count of rows in table: " + str(count_rows))
        print("count of columns in table: " + str(count_columns))
        putly.print_terminal_partition(level=5)
        count_rows = (table_signal.shape[0])
        count_columns = (table_signal.shape[1])
        print("table of information about signals:")
        print(table_signal.iloc[0:10, 0:])
        print("count of rows in table: " + str(count_rows))
        print("count of columns in table: " + str(count_columns))
        putly.print_terminal_partition(level=5)
        pass
    # Collect information.
    pail = dict()
    pail["table_gene"] = table_gene
    pail["table_signal"] = table_signal
    # Return information.
    return pail


##########
# 7. Fill missing values of signal intensity.
# Functionality for this operation is in the "partner" package.


##########
# 8. Check the coherence of separate tables for analysis.


def check_coherence_table_sample_table_signal(
    table_sample=None,
    table_signal=None,
    tissue=None,
    report=None,
):
    """
    Checks the coherence, specifically identity and sequence of samples, of
    information in separate tables for sample attributes and gene signals
    across samples.

    arguments:
        table_sample (object): Pandas data-frame table of attributes for
            samples
        table_signal (object): Pandas data-frame table of values of signal
            intensity for sample observations across columns and for gene
            features across rows
        tissue (str): name of tissue, either 'adipose' or 'muscle', which
            distinguishes study design and sets of samples
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of information

    """

    # Copy information in table.
    table_sample = table_sample.copy(deep=True)
    table_sample_extract = table_sample.copy(deep=True)
    table_signal = table_signal.copy(deep=True)
    # Organize indices in table.
    table_sample_extract.reset_index(
        level=None,
        inplace=True,
        drop=False, # remove index; do not move to regular columns
    )
    # Extract identifiers of samples from each separate table.
    samples_sample = copy.deepcopy(
        table_sample_extract["identifier"].to_list()
    )
    samples_signal = copy.deepcopy(
        table_signal.columns.to_list()
    )
    # Confirm that both sets of samples are inclusive.
    inclusion = putly.compare_lists_by_mutual_inclusion(
        list_primary=samples_sample,
        list_secondary=samples_signal,
    )
    # Confirm that both sets of samples are identical across sequence.
    identity = putly.compare_lists_by_elemental_identity(
        list_primary=samples_sample,
        list_secondary=samples_signal,
    )
    # Confirm that both sets of samples are equal.
    equality = (samples_sample == samples_signal)
    # Perform tests of comparisons.
    test_primary = ["a", "b", "c", "d", "e", "f", "g",]
    test_secondary = ["a", "b", "c", "d", "g", "f", "e",]
    test_inclusion = putly.compare_lists_by_mutual_inclusion(
        list_primary=test_primary,
        list_secondary=test_secondary,
    )
    test_identity = putly.compare_lists_by_elemental_identity(
        list_primary=test_primary,
        list_secondary=test_secondary,
    )
    test_equality = (test_primary == test_secondary)
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organization.py")
        print("function: check_coherence_table_sample_table_signal()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=5)
        count_rows = (table_sample.shape[0])
        count_columns = (table_sample.shape[1])
        print("table of information about samples:")
        print(table_sample)
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        putly.print_terminal_partition(level=5)
        count_rows = (table_signal.shape[0])
        count_columns = (table_signal.shape[1])
        print("table of information about signals:")
        print(table_signal)
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        putly.print_terminal_partition(level=5)
        print("sample identifiers from rows of sample table:")
        print(samples_sample)
        putly.print_terminal_partition(level=5)
        print("sample identifiers from columns of signal table:")
        print(samples_signal)
        putly.print_terminal_partition(level=5)
        print("real comparisons of sample identifiers:")
        print("inclusion: " + str(inclusion))
        print("identity: " + str(identity))
        print("equality: " + str(equality))
        putly.print_terminal_partition(level=5)
        print("fake comparisons to check the tests themselves:")
        print("inclusion: " + str(test_inclusion))
        print("identity: " + str(test_identity))
        print("equality: " + str(test_equality))
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    pass


##########
# TODO: TCW; 18 July 2024
# For analysis (by regression, for example) it will make most sense to transpose the "signal" table
# to orient samples across rows (convenience in merging in sample attributes)
# and genes across columns (features, along with sample attributes as covariates).



##########
# Downstream analyses

# differential expression in DESeq2
# regression analyses in custom models

##########
# Downstream visualizations

# volcano plots of fold changes
# Venn diagrams of sets of differentially expressed genes (up or down)
# heatmaps of gene signals across persons
# pairwise correlation matrices with hierarchical clustering
#



###############################################################################
# Procedure


##########
# Control procedure within branch for parallelization.


def control_branch_procedure(
    name_set=None,
    tissue=None,
    cohort_selection=None,
    factor_availability=None,
    project=None,
    routine=None,
    procedure=None,
    path_directory_dock=None,
    report=None,
):
    """
    Control branch of procedure.

    arguments:
        name_set (str): name for instance of rules for selection
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        cohort_selection (dict<list<str>>): filters on rows in table for
            selection of samples relevant to cohort for analysis
        factor_availability (dict<list<str>>): features and their values
            corresponding to factors of interest in the analysis
        project (str): name of project
        routine (str): name of routine, either 'transcriptomics' or
            'proteomics'
        procedure (str): name of procedure, a set or step in the routine
            process
        path_directory_dock (str): path to dock directory for procedure's
            source and product directories and files
        report (bool): whether to print reports

    raises:

    returns:

    """

    ##########
    # 1. Initialize directories for read of source and write of product files.
    paths = initialize_directories(
        project=project,
        routine=routine,
        procedure=procedure,
        tissue=tissue,
        name_set=name_set,
        path_directory_dock=path_directory_dock,
        restore=True,
        report=report,
    )

    ##########
    # 2. Read source information from file.
    pail_source = read_source(
        tissue=tissue,
        paths=paths,
        report=report,
    )

    ##########
    # 3. Select set of samples relevant for analysis.
    pail_sample = select_sets_identifier_table_sample(
        table_sample=pail_source["table_sample"],
        name_set=name_set,
        tissue=tissue,
        cohort_selection=cohort_selection,
        factor_availability=factor_availability,
        report=report,
    )
    #pail_sample["samples_selection"]


    ##########
    # 4. Organize from source the information about signals.
    columns_gene = define_column_sequence_table_main_gene()
    pail_organization_main = organize_table_main(
        table_main=pail_source["table_main"],
        columns_gene=columns_gene,
        samples=pail_sample["samples_selection"],
        tissue=tissue,
        report=report,
    )

    ##########
    # 5. Filter columns and rows in main table.
    table_filter = filter_table_main(
        table_main=pail_organization_main["table_main"],
        columns_gene=columns_gene,
        samples_all=pail_sample["samples_selection"],
        samples_control=[],
        samples_intervention=[],
        filter_rows_identity=True,
        filter_rows_signal=True,
        filter_rows_signal_by_condition=False,
        threshold_signal_low=10, # DESeq2 recommendation for bulk RNAseq
        threshold_signal_high=None,
        proportion_signal_all=0.10, # proportion smaller condition to total
        proportion_signal_control=0.5,
        proportion_signal_intervention=0.5,
        tissue=tissue,
        report=report,
    )

    ##########
    # 6. Separate tables for information of distinct types.
    pail_separate = separate_table_main_columns(
        table_main=table_filter,
        columns_gene=columns_gene,
        columns_signal=pail_sample["samples_selection"],
        tissue=tissue,
        report=report,
    )

    ##########
    # 7. Fill missing values of signal intensity.
    table_signal = porg.fill_missing_values_table_by_row(
        table=pail_separate["table_signal"],
        columns=pail_sample["samples_selection"],
        method="zero",
        report=report,
    )


    ##########
    # 8. Check the coherence of separate tables for analysis.
    check_coherence_table_sample_table_signal(
        table_sample=pail_sample["table_selection"],
        table_signal=table_signal,
        tissue=tissue,
        report=report,
    )


    # TODO: TCW; 24 July 2024
    # TODO:
    # 1. - In future, add a pseudo-count of 1 to any zeros or missing values.
    #    - Silverman et al, 2020 (PubMed:33101615) is a good review of methods for handling zeros.
    # 2. - In future, apply a variety of scale-adjustment and normalization methods.
    #    - DESeq2 algorithm (PubMed:25516281), edgeR algorithm (PubMed:20196867), MRN algorithm (PubMed:26442135)
    #    - Evans, 2018 (PubMed:28334202)
    # 3. - In future, apply logarithmic transformation and evaluate distributions (histograms).
    # 4. - In future, evaluate coefficient of variance of each gene across control samples.

    ##########
    # Collect information.
    # Collections of files.
    pail_write_data = dict()
    pail_write_data[str("table_sample")] = (
        pail_sample["table_selection"]
    )
    pail_write_data[str("table_gene")] = (
        pail_separate["table_gene"]
    )
    pail_write_data[str("table_signal")] = (
        pail_separate["table_signal"]
    )

    ##########
    # Write product information to file.
    putly.write_tables_to_file(
        pail_write=pail_write_data,
        path_directory=paths["out_data"],
        reset_index=False,
        write_index=True,
        type="text",
    )
    putly.write_tables_to_file(
        pail_write=pail_write_data,
        path_directory=paths["out_data"],
        reset_index=False,
        write_index=True,
        type="pickle",
    )
    pass


##########
# Manage parallelization.


def control_parallel_instance(
    instance=None,
    parameters=None,
):
    """
    Control procedure to organize within tables the information about genetic
    correlations from LDSC.

    arguments:
        instance (dict): parameters specific to current instance
            name_set (str): name for instance of rules for selection
            tissue (str): name of tissue, either 'adipose' or 'muscle', which
                distinguishes study design and sets of samples
            cohort_selection (dict<list<str>>): filters on rows in table for
                selection of samples relevant to cohort for analysis
            factor_availability (dict<list<str>>): features and their values
                corresponding to factors of interest in the analysis
        parameters (dict): parameters common to all instances
            project (str): name of project
            routine (str): name of routine, either 'transcriptomics' or
                'proteomics'
            procedure (str): name of procedure, a set or step in the routine
                process
            path_directory_dock (str): path to dock directory for procedure's
                source and product directories and files
            report (bool): whether to print reports

    raises:

    returns:

    """

    ##########
    # Extract parameters.
    # Extract parameters specific to each instance.
    name_set = instance["name_set"]
    tissue = instance["tissue"]
    cohort_selection = instance["cohort_selection"]
    factor_availability = instance["factor_availability"]
    # Extract parameters common across all instances.
    project = parameters["project"]
    routine = parameters["routine"]
    procedure = parameters["procedure"]
    path_directory_dock = parameters["path_directory_dock"]
    report = parameters["report"]

    ##########
    # Control procedure with split for parallelization.
    control_branch_procedure(
        name_set=name_set,
        tissue=tissue, # adipose, muscle
        cohort_selection=cohort_selection,
        factor_availability=factor_availability,
        project=project,
        routine=routine,
        procedure=procedure,
        path_directory_dock=path_directory_dock,
        report=report,
    )
    pass


def collect_scrap_parallel_instances_for_analysis_sets(
):
    """
    Collect scrap parallel instances for analysis sets.

    arguments:

    raises:

    returns:

    """

    # Collect parameters specific to each instance.
    # tissue: adipose
    instances = [
        {
            "name_set": str(
                "adipose_elder-visit-second_intervention"
            ),
            "tissue": "adipose",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["adipose",],
                "cohort_age_text": ["elder",],
                "study_clinic_visit": ["second",],
            },
            "factor_availability": {
                "intervention_text": ["placebo", "active",],
            },
        },
        {
            "name_set": str(
                "adipose_elder-active_visit"
            ),
            "tissue": "adipose",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["adipose",],
                "cohort_age_text": ["elder",],
                "intervention_text": ["active",],
            },
            "factor_availability": {
                "study_clinic_visit": ["first", "second",],
            },
        },
    ]
    # tissue: muscle
    instances = [
        {
            "name_set": str(
                "muscle_exercise-0hr_age"
            ),
            "tissue": "muscle",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["muscle",],
                "exercise_time_point": ["0_hour",],
            },
            "factor_availability": {
                "cohort_age_text": ["younger", "elder",],
            },
        },
        {
            "name_set": str(
                "muscle_younger_exercise"
            ),
            "tissue": "muscle",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["muscle",],
                "cohort_age_text": ["younger",],
            },
            "factor_availability": {
                "exercise_time_point": ["0_hour", "3_hour",],
            },
        },
        {
            "name_set": str(
                "muscle_elder_exercise"
            ),
            "tissue": "muscle",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["muscle",],
                "cohort_age_text": ["elder",],
            },
            "factor_availability": {
                "exercise_time_point": ["0_hour", "3_hour",],
            },
        },
    ]
    pass


def control_parallel_instances(
    project=None,
    routine=None,
    procedure=None,
    path_directory_dock=None,
    report=None,
):
    """
    Control procedure for parallel instances.

    arguments:
        project (str): name of project
        routine (str): name of routine, either 'transcriptomics' or
            'proteomics'
        procedure (str): name of procedure, a set or step in the routine
            process
        path_directory_dock (str): path to dock directory for procedure's
            source and product directories and files
        report (bool): whether to print reports


    raises:

    returns:

    """

    # Collect parameters common across all instances.
    parameters = dict()
    parameters["project"] = project
    parameters["routine"] = routine
    parameters["procedure"] = procedure
    parameters["path_directory_dock"] = path_directory_dock
    parameters["report"] = report

    # Collect parameters specific to each instance.
    instances = [
        {
            "name_set": str(
                "muscle_exercise-0hr_age"
            ),
            "tissue": "muscle",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["muscle",],
                "exercise_time_point": ["0_hour",],
            },
            "factor_availability": {
                "cohort_age_text": ["younger", "elder",],
            },
        },
        {
            "name_set": str(
                "muscle_younger_exercise-3hr"
            ),
            "tissue": "muscle",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["muscle",],
                "cohort_age_text": ["younger",],
            },
            "factor_availability": {
                "exercise_time_point": ["0_hour", "3_hour",],
            },
        },
        {
            "name_set": str(
                "muscle_elder_exercise-3hr"
            ),
            "tissue": "muscle",
            "cohort_selection": {
                "inclusion": [1,],
                "tissue": ["muscle",],
                "cohort_age_text": ["elder",],
            },
            "factor_availability": {
                "exercise_time_point": ["0_hour", "3_hour",],
            },
        },
    ]

    # Execute procedure iteratively with parallelization across instances.
    if True:
        prall.drive_procedure_parallel(
            function_control=(
                control_parallel_instance
            ),
            instances=instances,
            parameters=parameters,
            cores=5,
            report=True,
        )
    else:
        # Execute procedure directly for testing.
        control_parallel_instance(
            instance=instances[1],
            parameters=parameters,
        )
    pass


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
    procedure="organize_signal"
    report = True

    ##########
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organize_sample.py")
        print("function: execute_procedure()")
        putly.print_terminal_partition(level=5)
        print("system: local")
        print("project: " + str(project))
        print("routine: " + str(routine))
        print("procedure: " + str(procedure))
        putly.print_terminal_partition(level=5)
        pass

    ##########
    # Preinitialize directories before parallel branches.
    paths = preinitialize_directories(
        project=project,
        routine=routine,
        procedure=procedure,
        path_directory_dock=path_directory_dock,
        restore=True,
        report=report,
    )

    ##########
    # Control procedure with split for parallelization.
    #control_split_procedure(
    #    tissue="adipose", # adipose, muscle
    #    paths=paths,
    #    report=True,
    #)

    ##########
    # Control procedure for parallel instances.
    control_parallel_instances(
        project=project,
        routine=routine,
        procedure=procedure,
        path_directory_dock=path_directory_dock,
        report=report,
    )

    pass


###############################################################################
# End
