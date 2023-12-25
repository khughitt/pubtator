"""
Creates a gene-disease co-occurrence matrix
"""
import json
import pandas as pd
import numpy as np

snek = snakemake

# load gene and drug pmid mappings
with open(snek.input[0]) as fp:
    gene_pmid_mapping = json.load(fp)

with open(snek.input[1]) as fp:
    disease_pmid_mapping = json.load(fp)

# create empty matrix to store gene-disease co-occurrence counts
entrez_ids = gene_pmid_mapping.keys()
num_genes = len(entrez_ids)

mesh_ids = disease_pmid_mapping.keys()
num_diseases = len(mesh_ids)

comat = np.zeros((num_genes, num_diseases), dtype=np.uint32)

# iterate over genes & diseases
for i, gene in enumerate(entrez_ids):
    # get pubmed ids associated with gene
    gene_pmids = gene_pmid_mapping[gene]

    for j, disease in enumerate(mesh_ids):
        # get pubmed ids associated with disease
        disease_pmids = disease_pmid_mapping[disease]

        # compute gene-disease co-occurrence count
        num_shared = len(set(gene_pmids).intersection(disease_pmids))

        comat[i, j] = num_shared

# store gene-disease co-occurrence matrix
comat = pd.DataFrame(comat, index=entrez_ids, columns=mesh_ids)
comat.reset_index().rename(columns={'index': 'entrez_id'}).to_feather(snek.output[0])
