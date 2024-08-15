"""
Supply functionality for process and analysis of data from transcriptomics.

This module 'select_gene_sets' is part of the 'transcriptomics' package within
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
        print("module: exercise.transcriptomics.select_gene_sets.py")
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
        name_set (str): name for set of samples and parameters in the
            analysis of differential expression
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
    paths["out_plot"] = os.path.join(
        paths["out_set"], "plot",
    )
    # Initialize directories in main branch.
    paths_initialization = [
        #paths["out_project"],
        #paths["out_routine"],
        #paths["out_procedure"], # omit to avoid conflict in parallel branches
        paths["out_set"],
        paths["out_data"],
        paths["out_plot"],
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
        print("module: exercise.transcriptomics.select_gene_sets.py")
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


def define_column_types_table_deseq2():
    """
    Defines the names and types of variable columns within table from DESeq2.

    Review: TCW; 7 August 2024

    arguments:

    raises:

    returns:
        (dict<str>): variable types of columns within table

    """

    # Specify variable types of columns within table.
    types_columns = dict()
    types_columns["identifier_gene"] = "string"
    types_columns["baseMean"] = "float32"
    types_columns["log2FoldChange"] = "float32"
    types_columns["lfcSE"] = "float32"
    types_columns["stat"] = "float32"
    types_columns["pvalue"] = "float64"
    types_columns["padj"] = "float64"
    types_columns["gene_identifier"] = "string"
    types_columns["gene_name"] = "string"
    types_columns["gene_type"] = "string"
    types_columns["gene_chromosome"] = "string"
    # Return information.
    return types_columns


def read_source(
    tissue=None,
    name_set=None,
    paths=None,
    report=None,
):
    """
    Reads and organizes source information from file.

    Notice that Pandas does not accommodate missing values within series of
    integer variable types.

    arguments:
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        name_set (str): name for set of samples and parameters in the
            analysis of differential expression
        paths : (dict<str>): collection of paths to directories for procedure's
            files
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of source information read from file

    """

    # Define paths to parent directories.
    #paths["in_data"]
    #paths["in_parameters"]

    # Define paths to child files.
    path_file_table_deseq2 = os.path.join(
        paths["out_routine"], "deseq2", tissue, name_set,
        "table_result_deseq2.tsv",
    )

    # Collect information.
    pail = dict()
    # Read information from file.

    # Table of fold changes for genes with differential expression from DESeq2.
    types_columns = define_column_types_table_deseq2()
    pail["table_deseq2"] = pandas.read_csv(
        path_file_table_deseq2,
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
        print("module: exercise.transcriptomics.select_gene_sets.py")
        print("function: read_source()")
        print("tissue: " + tissue)
        putly.print_terminal_partition(level=4)
        count_rows = (pail["table_deseq2"].shape[0])
        count_columns = (pail["table_deseq2"].shape[1])
        print("deseq2 table: ")
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        print(pail["table_deseq2"])
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return pail


##########
# 3. Organize from source the information about differential expression of
#    genes.


def define_column_sequence_table_change_deseq2():
    """
    Defines the columns in sequence within table.

    arguments:

    raises:

    returns:
        (list<str>): names of columns in sequence by which to filter and sort
            columns in table

    """

    # Specify sequence of columns within table.
    columns_sequence = [
        "identifier_gene",
        #"baseMean",
        "fold_change_log2",
        "fold_change_log2_standard_error",
        #"stat",
        "p_value",
        "p_value_threshold",
        "p_value_negative_log10",
        "q_value",
        "q_value_threshold",
        "q_value_negative_log10",
        "gene_identifier",
        "gene_name",
        "gene_type",
        "gene_chromosome",
    ]
    # Return information.
    return columns_sequence


def organize_table_change_deseq2(
    table=None,
    columns_sequence=None,
    tissue=None,
    name_set=None,
    report=None,
):
    """
    Organizes information in table about differential expression of genes.

    arguments:
        table (object): Pandas data-frame table of information about genes
            that demonstrate differential expression
        columns_sequence (list<str>): names of columns in sequence by which to
            filter and sort columns in table
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        name_set (str): name for set of samples and parameters in the
            analysis of differential expression
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of information

    """

    # Copy information in table.
    table_change = table.copy(deep=True)
    # Copy other information.
    columns_sequence = copy.deepcopy(columns_sequence)

    # Translate names of columns.
    translations = dict()
    translations["log2FoldChange"] = "fold_change_log2"
    translations["lfcSE"] = "fold_change_log2_standard_error"
    translations["pvalue"] = "p_value"
    translations["padj"] = "q_value"
    table_change.rename(
        columns=translations,
        inplace=True,
    )

    # Replace values of zero for p-value and q-value with reasonable
    # approximation of precision.
    # Set threshold on very small values of p-value and q-value.
    # DESeq2 returns values of zero for p-value and q-value when the actual
    # value is smaller than a threshold of approximately 1E-250.
    #table_change["p_value_fill"] = table_change["p_value"].replace(
    #    to_replace=0.0,
    #    value=1E-250,
    #)
    #table_change["q_value_fill"] = table_change["q_value"].replace(
    #    to_replace=0.0,
    #    value=1E-250,
    #)
    table_change = table_change.loc[
        (
            (pandas.notna(table_change["p_value"])) &
            (pandas.notna(table_change["q_value"])) &
            (table_change["p_value"] >= float(0)) &
            (table_change["q_value"] >= float(0))
        ), :
    ]
    table_change["p_value_threshold"] = table_change.apply(
        lambda row:
            1E-250 if (float(row["p_value"]) < 1E-250) else row["p_value"],
        axis="columns", # apply function to each row
    )
    table_change["q_value_threshold"] = table_change.apply(
        lambda row:
            1E-250 if (float(row["q_value"]) < 1E-250) else row["q_value"],
        axis="columns", # apply function to each row
    )
    # Filter rows in table for selection of non-missing values for fold change.
    table_change = table_change.loc[
        (
            (pandas.notna(table_change["fold_change_log2"])) &
            (pandas.notna(table_change["fold_change_log2_standard_error"])) &
            (pandas.notna(table_change["p_value_threshold"])) &
            (pandas.notna(table_change["q_value_threshold"])) &
            (table_change["p_value_threshold"] > float(0)) &
            (table_change["q_value_threshold"] > float(0))
        ), :
    ]

    # Calculate the negative, base-ten logarithm of the p-value for
    # differential expression of each gene.
    #table_change["p_value_negative_log10"] = numpy.log10(
    #    table_change["p_value"]
    #)
    table_change["p_value_negative_log10"] = table_change.apply(
        lambda row: (-1*math.log(row["p_value_threshold"], 10)),
        axis="columns", # apply function to each row
    )
    table_change["q_value_negative_log10"] = table_change.apply(
        lambda row: (-1*math.log(row["q_value_threshold"], 10)),
        axis="columns", # apply function to each row
    )

    # Filter and sort columns within table.
    table_change = porg.filter_sort_table_columns(
        table=table_change,
        columns_sequence=columns_sequence,
        report=report,
    )

    # Collect information.
    pail = dict()
    pail["table_change"] = table_change
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organize_signal.py")
        print("function: organize_table_change_deseq2()")
        putly.print_terminal_partition(level=5)
        print("tissue: " + tissue)
        print("name_set: " + name_set)
        putly.print_terminal_partition(level=4)
        count_rows = (pail["table_change"].shape[0])
        count_columns = (pail["table_change"].shape[1])
        print("table of genes with differential expression: ")
        print("count of rows in table: " + str(count_rows))
        print("Count of columns in table: " + str(count_columns))
        print(pail["table_change"].iloc[0:10, 0:])
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return pail


##########
# 4. Select sets of genes with differential expression.


def select_sets_differential_expression_gene(
    table=None,
    column_identifier=None,
    column_name=None,
    column_fold=None,
    column_p=None,
    threshold_fold=None,
    threshold_p=None,
    tissue=None,
    name_set=None,
    report=None,
):
    """
    Selects sets of genes applying filters at specific thresholds on their
    statistics for differential expression.

    arguments:
        table (object): Pandas data-frame table of information about genes
            that demonstrate differential expression
        column_identifier (str): name of column in table for the unique
            identifier corresponding to the fold change
        column_name (str): name of column in table for the name corresponding
            to the fold change
        column_fold (str): name of column in table on which to apply the
            threshold for the fold change
        column_p (str): name of column in table on which to apply the threshold
            for the p-value or q-value corresponding to the fold change
            estimate
        threshold_fold (float): value for threshold on fold change
            (fold change > threshold) that is on the same scale, such as
            base-two logarithm, as the actual values themselves
        threshold_p (float): value for threshold on p-values or q-values
            (p-value > threshold) that is on the same scale, such as negative
            base-ten logarithm, as the actual values themselves
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        name_set (str): name for set of samples and parameters in the
            analysis of differential expression
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of information

    """

    # Copy information in table.
    table = table.copy(deep=True)

    # Filter rows in table for selection of sets of genes that demonstrate
    # specific characteristics of differential expression.
    pail_threshold = porg.segregate_fold_change_values_by_thresholds(
        table=table,
        column_fold=column_fold,
        column_p=column_p,
        threshold_fold=threshold_fold,
        threshold_p=threshold_p,
        report=False,
    )
    # Extract identifiers genes with differential expression beyond thresholds.
    genes_threshold = copy.deepcopy(
        pail_threshold["table_pass_any"][column_identifier].to_list()
    )
    genes_up = copy.deepcopy(
        pail_threshold["table_pass_up"][column_identifier].to_list()
    )
    genes_down = copy.deepcopy(
        pail_threshold["table_pass_down"][column_identifier].to_list()
    )

    # Collect information.
    pail = dict()
    pail["genes_threshold"] = genes_threshold
    pail["genes_up"] = genes_up
    pail["genes_down"] = genes_down
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.organize_signal.py")
        print("function: select_sets_differential_expression_gene()")
        putly.print_terminal_partition(level=5)
        print("tissue: " + tissue)
        print("name_set: " + name_set)
        putly.print_terminal_partition(level=4)
        count_both = (len(pail["genes_threshold"]))
        count_up = (len(pail["genes_up"]))
        count_down = (len(pail["genes_down"]))
        print("count of genes beyond thresholds: " + str(count_both))
        print("count of those with positive change: " + str(count_up))
        print("count of those with negative change: " + str(count_down))
        putly.print_terminal_partition(level=5)
        pass
    # Return information.
    return pail


##########
# 5. Create chart to represent fold changes and write to file.


def create_write_chart_fold_change(
    table=None,
    column_identifier=None,
    column_name=None,
    column_fold=None,
    column_p=None,
    threshold_fold=None,
    threshold_p=None,
    tissue=None,
    name_set=None,
    paths=None,
    report=None,
):
    """
    Create chart representation of fold change and write to file.

    arguments:
        table (object): Pandas data-frame table of information about genes
            that demonstrate differential expression
        column_identifier (str): name of column in table for the unique
            identifier corresponding to the fold change
        column_name (str): name of column in table for the name corresponding
            to the fold change
        column_fold (str): name of column in table on which to apply the
            threshold for the fold change
        column_p (str): name of column in table on which to apply the threshold
            for the p-value or q-value corresponding to the fold change
            estimate
        threshold_fold (float): value for threshold on fold change
            (fold change > threshold) that is on the same scale, such as
            base-two logarithm, as the actual values themselves
        threshold_p (float): value for threshold on p-values or q-values
            (p-value > threshold) that is on the same scale, such as negative
            base-ten logarithm, as the actual values themselves
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
        name_set (str): name for set of samples and parameters in the
            analysis of differential expression
        paths : (dict<str>): collection of paths to directories for procedure's
            files
        report (bool): whether to print reports

    raises:

    returns:
        (object): figure object from MatPlotLib

    """

    # Organize parameters.
    name_figure = name_set
    path_directory = paths["out_plot"]

    # Define fonts.
    fonts = pplot.define_font_properties()
    # Define colors.
    colors = pplot.define_color_properties()
    # Create figure.
    figure = pplot.plot_scatter_fold_change_volcano(
        table=table,
        column_identifier=column_identifier,
        column_name=column_name,
        column_fold=column_fold,
        column_p=column_p,
        threshold_fold=threshold_fold, # base two logarithm
        threshold_p=threshold_p, # negative base ten logarithm
        identifiers_emphasis=[
            "ENSG00000119508.18", # gene name: NR4A3
            "ENSG00000105329.11", # gene name: TGFB1
        ],
        emphasis_label=True,
        count_label=True,
        minimum_abscissa=(
            (numpy.nanmin(table[column_fold].to_numpy())) - 0.5
        ),
        maximum_abscissa=(
            (numpy.nanmax(table[column_fold].to_numpy())) + 0.5
        ),
        minimum_ordinate=-0.1,
        maximum_ordinate=(
            (numpy.nanmax(table[column_p].to_numpy())) + 1
        ),
        title_abscissa="log2(Fold Change)",
        title_ordinate="-1*log10(BH FDR q-value)",
        size_title_abscissa="eight", # ten
        size_title_ordinate="eight", # ten
        size_label_abscissa="twelve", # multi-panel: ten; individual: twelve
        size_label_ordinate="twelve", # multi-panel: ten; individual: twelve
        size_label_emphasis="twelve",
        size_label_count="twelve",
        aspect="landscape", # square, portrait, landscape, ...
        fonts=fonts,
        colors=colors,
        report=report,
    )
    # Write figure to file.
    pplot.write_product_plot_figure(
        figure=figure,
        format="jpg", # jpg, png, svg
        resolution=300,
        name_file=name_figure,
        path_directory=path_directory,
    )
    # Return information.
    return figure





# TODO: TCW; 8 August 2024
# NEXT STEPS
# 1. filter genes by fold change and by p-value
#    - potentially consider the 95%CI of fold change for this threshold filter
#    - this would look funny on the volcano plot...
#    - maybe the volcano plot could look normal, except that the genes that pass
#    - filter by 95% CI could be the ones that I actually highlight in orange
# 2.


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
    project=None,
    routine=None,
    procedure=None,
    path_directory_dock=None,
    report=None,
):
    """
    Control branch of procedure.

    arguments:
        name_set (str): name for set of samples and parameters in the
            analysis of differential expression
        tissue (list<str>): name of tissue that distinguishes study design and
            set of relevant samples, either 'adipose' or 'muscle'
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
        name_set=name_set,
        paths=paths,
        report=report,
    )

    ##########
    # 3. Organize from source the information about differential expression of
    #    genes.
    columns_sequence = define_column_sequence_table_change_deseq2()
    pail_organization = organize_table_change_deseq2(
        table=pail_source["table_deseq2"],
        columns_sequence=columns_sequence,
        tissue=tissue,
        name_set=name_set,
        report=report,
    )
    #pail_organization["table_change"]

    ##########
    # 4. Select sets of genes with differential expression.
    pail_selection = select_sets_differential_expression_gene(
        table=pail_organization["table_change"],
        column_identifier="gene_identifier",
        column_name="gene_name",
        column_fold="fold_change_log2",
        column_p="q_value_negative_log10",
        threshold_fold=math.log(float(1.7), 2), # base two logarithm
        threshold_p=float(2.0), # negative base ten logarithm
        tissue=tissue,
        name_set=name_set,
        report=report,
    )

    ##########
    # 5. Create chart to represent fold changes and write to file.
    create_write_chart_fold_change(
        table=pail_organization["table_change"],
        column_identifier="gene_identifier",
        column_name="gene_name",
        column_fold="fold_change_log2",
        column_p="q_value_negative_log10",
        threshold_fold=math.log(float(1.7), 2), # base two logarithm
        threshold_p=float(2.0), # negative base ten logarithm
        tissue=tissue,
        name_set=name_set,
        paths=paths,
        report=report,
    )


    ##########
    # Collect information.
    # Collections of files.
    #pail_write_tables = dict()
    pail_write_lists = dict()
    pail_write_lists[str("genes_threshold")] = (
        pail_selection["genes_threshold"]
    )
    pail_write_lists[str("genes_up")] = (
        pail_selection["genes_up"]
    )
    pail_write_lists[str("genes_down")] = (
        pail_selection["genes_down"]
    )
    ##########
    # Write product information to file.
    putly.write_lists_to_file_text(
        pail_write=pail_write_lists,
        path_directory=paths["out_data"],
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
            name_set (str): name for set of samples and parameters in the
                analysis of differential expression
            tissue (str): name of tissue, either 'adipose' or 'muscle', which
                distinguishes study design and sets of samples
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
        },
        {
            "name_set": str(
                "muscle_all_age-exercise-3hr"
            ),
            "tissue": "muscle",
        },
        {
            "name_set": str(
                "muscle_younger_exercise-3hr"
            ),
            "tissue": "muscle",
        },
        {
            "name_set": str(
                "muscle_elder_exercise-3hr"
            ),
            "tissue": "muscle",
        },
    ]

    # Execute procedure iteratively with parallelization across instances.
    if False:
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
    procedure="select_gene_sets"
    report = True

    ##########
    # Report.
    if report:
        putly.print_terminal_partition(level=3)
        print("module: exercise.transcriptomics.select_gene_sets.py")
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
