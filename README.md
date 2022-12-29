# PubTator Central Data Preparation Pipeline

## Overview

This repo contains a [Snakemake](https://snakemake.readthedocs.io/) pipeline for downloading and
processing [Pubtator Central (PTC)](https://www.ncbi.nlm.nih.gov/research/pubtator/) annotation data into
a form more readily usable by other lit-explore projects.

Data is acquired from the [PubTator Central FTP
site](https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/) as gzip-compressed tab-delimited files.

PTC annotations are divided into six types:

1. Cell lines
2. Chemicals
3. Diseases
4. Genes
5. Mutations
6. Species

Each source file includes the five fields, "_pmid_", "_type_", "_concept_id_", "_mentions_", and
"_resource_", e.g.:

```
|     pmid | type     | concept_id   | mentions   | resource   |
|---------:|:---------|:-------------|:-----------|:-----------|
| 25817000 | CellLine | B cell       | B-cell     | TaggerOne  |
| 34546000 | CellLine | CVCL_0030    | HeLa       | TaggerOne  |
| 34546000 | CellLine | CVCL_0032    | SiHa       | TaggerOne  |
| 34546000 | CellLine | CVCL_0291    | HCT116     | TaggerOne  |
| 34546000 | CellLine | CVCL_1100    | CaSki      | TaggerOne  |
```

_Note_: the original PTC data files do not include a header row as in the example above.

This pipeline checks each of the files for problematic entries related to the upstream data
processing, filters the data to exclude uncommon annotations, and saves the cleaned and filtered
versions of the annotations along with some summary data tables.

For more information about the source data, refer to the
[README.txt](https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/README.txt) in the PTC FTP.

## Usage

To use the pipeline, first create and activate a [conda
environment](https://docs.conda.io/en/latest/) using the provided `requirements.txt` file:

```
conda create -n pubtator --file requirements.txt
conda activate pubtator
```

Next, copy the example config file, `config/config.example.yml`, and modify the config to indicate
the desired output directory to use, along with any other changes to the settings.

```
cp config/config.example.yml config/config.yml
```

Finally, launch the Snakemake pipeline, provided the config file along with any other desired
settings, e.g.:

```
snakemake -j4 --configfile config/config.yml
```
