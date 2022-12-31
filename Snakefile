"""
lit-explore: PubTator Central Data Preparation

Processes data from PubTator Central into a form that can be easily used in various lit-explore
efforts.

For more information about the source data, see:

https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/README.txt
"""
import os

configfile: "config/config.yml"

# PubTator Central annotation types
ANNOT_TYPES = ["cellline", "chemical", "disease", "gene", "mutation", "species"]

rule all:
    input:
        expand(os.path.join(config["output_dir"], "counts", "{annot}_concept_ids.feather"), annot=ANNOT_TYPES),
        expand(os.path.join(config["output_dir"], "counts", "{annot}_mentions.feather"), annot=ANNOT_TYPES)

rule summarize_counts:
    input:
        os.path.join(config["output_dir"], "filtered", "{annot}.feather")
    output:
        os.path.join(config["output_dir"], "counts", "{annot}_concept_ids.feather"),
        os.path.join(config["output_dir"], "counts", "{annot}_mentions.feather")
    script:
        "scripts/summarize_counts.py"

rule filter_data:
    input:
        os.path.join(config["output_dir"], "raw", "{annot}.gz")
    output:
        os.path.join(config["output_dir"], "filtered", "{annot}.feather")
    script:
        "scripts/filter_data.py"

rule download_cellline_data:
    output:
        os.path.join(config["output_dir"], "raw", "{annot}.gz")
    shell:
        """
        curl --output {output} https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/{wildcards.annot}2pubtatorcentral.gz
        """
