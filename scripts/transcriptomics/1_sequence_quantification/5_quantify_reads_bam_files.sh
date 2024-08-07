#!/bin/bash

#chmod u+x script.sh
#chmod -R 777

###############################################################################
# Author: T. Cameron Waller
# Date, first execution: 13 July 2024
# Date, last execution or modification: 14 July 2024
# Review: TCW; 14 July 2024
###############################################################################
# Note

# View header of file in BAM or CRAM format to discern details of its prior
# processing.
# samtools head --headers 100 /path/to/input/file.bam
# samtools view --header-only --output /path/to/output/header/file.txt /path/to/input/file.bam

# Slurm batch job: 10545340
# - instances: 2
# - date: 14 July 2024
# threads=16
###SBATCH --nodes=1                            # count of cluster nodes (CPUs)
###SBATCH --ntasks-per-node=16                 # count of CPU cores or threads on node
###SBATCH --mem=10G                            # memory per node (per CPU)
###SBATCH --time=0-48:00:00                    # time allocation request (days-hours:minutes:seconds)
# This batch job, consisting of 154 samples in the first instance and 185
# samples in the second instance, required about 34 hours to run on one node
# for each instance with 16 CPU cores and 10 Gigabytes of memory for each node.

# For future quantifications, refer to script
# "5-1_trial_array_chunk_expansion.sh" for a demonstration of how to divide up
# an array of paths to files into smaller chunks and then expand these into a
# text string that can be passed as an argument and reformatted with a white
# space delimiter to hand as a parameter to HTSeq. This approach will make it
# practical to parallelize the HTSeq quantification more extensively. Then also
# implement a driver script to merge together the separate report tables from
# parallel quantification in HTSeq. Refer to the preliminary draft of script
# "merge_quantification_tables.sh" within "/.../partner/scripts/htseq".

###############################################################################


###############################################################################
# Organize arguments.

###############################################################################
# Organize paths.

# Directories.
cd ~
path_directory_parent_project=$(<"./paths/endocrinology/parent_tcameronwaller.txt")
path_directory_reference="${path_directory_parent_project}/reference"
path_directory_tool="${path_directory_parent_project}/tool"
path_directory_process="${path_directory_parent_project}/process"
path_directory_dock="${path_directory_process}/dock"

path_directory_source_adipose="${path_directory_dock}/consolidation_adipose_2024-05-31/filter_sort_index" # 14 July 2024
path_directory_source_muscle="${path_directory_dock}/consolidation_muscle_2022-07-13/filter_sort_index" # 14 July 2024
path_directory_product="${path_directory_dock}/quantification"
#stamp_date=$(date +%Y-%m-%d)
#path_directory_temporary="${path_directory_product}/temporary_${stamp_date}" # hopefully unique
path_directory_parallel="${path_directory_product}/parallel"

# Files.
path_file_annotation_gtf_gzip="${path_directory_reference}/human_genome/gencode/grch38/annotation/gencode.v46.primary_assembly.annotation.gtf.gz"
#path_file_annotation_gtf="${path_directory_temporary}/gencode.v46.primary_assembly.annotation.gtf"
path_file_product_adipose="${path_directory_product}/quantification_rna_reads_gene_adipose.tsv"
path_file_product_muscle="${path_directory_product}/quantification_rna_reads_gene_muscle.tsv"
path_file_parallel_instances="${path_directory_parallel}/instances_parallel.txt"

# Scripts.
path_script_quantify_1="${path_directory_process}/partner/scripts/htseq/quantify_rna_reads_slurm_1.sh"
path_script_quantify_2="${path_directory_process}/partner/scripts/htseq/quantify_rna_reads_slurm_2.sh"
path_script_quantify_3="${path_directory_process}/partner/scripts/htseq/quantify_rna_reads.sh"

# Executable handles.
path_environment_htseq="${path_directory_tool}/python/environments/htseq"

# Initialize directory.
rm -r $path_directory_product # caution
mkdir -p $path_directory_product
#mkdir -p $path_directory_temporary
mkdir -p $path_directory_parallel
# Initialize file.
rm $path_file_parallel_instances # caution

###############################################################################
# Organize parameters.

threads=16
report="true"

#set -x # enable print commands to standard error
set +x # disable print commands to standard error
#set -v # enable print input to standard error
set +v # disable print input to standard error

###############################################################################
# Execute procedure.


##########
if true; then
  # Define explicit instances for parallel batch of jobs.
  # Organize information within multi-dimensional array.
  instances_parallel=()
  instance="${path_directory_source_adipose};${path_file_product_adipose}"
  instances_parallel+=($instance)
  instance="${path_directory_source_muscle};${path_file_product_muscle}"
  instances_parallel+=($instance)
  # Write to file parameters for job instances.
  for instance in "${instances_parallel[@]}"; do
    echo $instance >> $path_file_parallel_instances
  done
  # Call script to submit parallel batch of job instances.
  /usr/bin/bash $path_script_quantify_1 \
  $path_file_parallel_instances \
  $path_directory_parallel \
  $path_file_annotation_gtf_gzip \
  $threads \
  $report \
  $path_script_quantify_2 \
  $path_script_quantify_3 \
  $path_environment_htseq
fi


##########
# Report.

if [ "$report" == "true" ]; then
  echo "----------"
  echo "----------"
  echo "----------"
  echo "Script:"
  echo $0 # Print full file path to script.
  echo "5_quantify_reads_bam_files.sh"
  echo "Quantify reads allocatable to specific genomic features."
  echo "----------"
  echo "Adipose"
  #echo "count of source files: " $count_paths_file_source_adipose
  echo "----------"
  echo "Muscle"
  #echo "count of source files: " $count_paths_file_source_muscle
  echo "----------"
fi

##########
# Remove directory of temporary, intermediate files.
#rm -r $path_directory_temporary

###############################################################################
# End.
