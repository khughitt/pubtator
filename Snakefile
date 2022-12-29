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
        expand(os.path.join(config["output_dir"], "raw", "{annot}2pubtatorcentral.gz"), annot=ANNOT_TYPES),

rule download_cellline_data:
    output:
        os.path.join(config["output_dir"], "raw", "{annot}2pubtatorcentral.gz")
    shell:
        """
        curl --output {output} https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/{wildcards.annot}2pubtatorcentral.gz
        """
