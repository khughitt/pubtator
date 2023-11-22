"""
Create a mapping from entrez gene ids to pubmed article ids
"""
import json
import numpy as np
import pandas as pd

snek = snakemake

SPECIES:str = snek.params["species"]

# load species data
species_df = pd.read_feather(snek.input[0])

# load gene data
gene_df = pd.read_feather(snek.input[1])

# load entrez id
symbol2entrez = pd.read_feather(snek.input[2])
ensgene2entrez = pd.read_feather(snek.input[3])

# create a list of all unique entrez ids associated with entries from either mapping
entrez_ids = set(symbol2entrez.entrezgene.values)
entrez_ids = sorted(list(entrez_ids.union(set(ensgene2entrez.entrezgene.values))))

# limit to articles mentioning target species
pmids = sorted(list(set(species_df.pmid[species_df.concept_id == SPECIES].values.tolist())))
gene_df = gene_df[gene_df.pmid.isin(pmids)]

# limit to species-specific entrez ids
gene_df = gene_df[gene_df.concept_id.isin(entrez_ids)]

# convert concept id to pyarrow/string type (~7x faster in testing..)
gene_df.concept_id = gene_df.concept_id.astype('string[pyarrow]')

# iterate over genes and retrieve associated pubmed ids for each
gene_pmids = {}

for entrez_id in entrez_ids:
    mask = gene_df.concept_id == entrez_id

    pmids = list(set(gene_df[mask].pmid.values))

    if len(pmids) > 0:
        gene_pmids[entrez_id] = pmids

def encoder(obj) -> int|list:
    """
    encoder to convert int64 elements to generic ints and sets to lists during
    json serialization
    """
    if isinstance(obj, np.generic):
        return obj.item()
    return obj

# store gene -> pmid mapping as json
with open(snek.output[0], "wt", encoding="utf-8") as fp:
    fp.write(json.dumps(gene_pmids, default=encoder))
