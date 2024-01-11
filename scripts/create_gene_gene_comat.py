"""
Creates a gene-gene co-occurrence matrix

- [ ] store lower-triangular matrix?
"""
import json
import pandas as pd
import numpy as np

snek = snakemake

# load gene/pmid mapping
with open(snek.input[0]) as fp:
    gene_pmids = json.load(fp)

# create empty matrix to store gene-gene co-occurrence counts
entrez_ids = list(gene_pmids.keys())
num_genes = len(entrez_ids)

comat = np.zeros((num_genes, num_genes), dtype=np.uint32)

# indices of upper triangular matrix
indices = np.triu_indices(num_genes, k=1)

# iterate over pairs of genes and compute overlap
for ind in range(len(indices[0])):
    i = indices[0][ind]
    j = indices[1][ind]

    gene1 = entrez_ids[i]
    gene2 = entrez_ids[j]

    # get pubmed ids associated with each gene
    gene1_pmids = gene_pmids[gene1]
    gene2_pmids = gene_pmids[gene2]

    # compute gene-gene co-occurrence count
    num_shared = len(set(gene1_pmids).intersection(gene2_pmids))

    comat[i, j] = comat[j, i] = num_shared

# store gene-gene co-occurrence matrix
comat = pd.DataFrame(comat, index=entrez_ids, columns=entrez_ids)
comat.reset_index().rename(columns={'index': 'entrez_id'}).to_feather(snek.output[0])
