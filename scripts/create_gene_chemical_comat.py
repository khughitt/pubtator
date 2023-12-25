"""
Creates a gene-chemical co-occurrence matrix
"""
import json
import pandas as pd
import numpy as np

snek = snakemake

# load gene and drug pmid mappings
with open(snek.input[0]) as fp:
    gene_pmid_mapping = json.load(fp)

with open(snek.input[1]) as fp:
    chem_pmid_mapping = json.load(fp)

# create empty matrix to store gene-chemical co-occurrence counts
entrez_ids = gene_pmid_mapping.keys()
num_genes = len(entrez_ids)

mesh_ids = chem_pmid_mapping.keys()
num_chemicals = len(mesh_ids)

comat = np.zeros((num_genes, num_chemicals), dtype=np.uint32)

print(f"Processing {num_genes} genes...")

# iterate over pairs of genes
for i, gene in enumerate(entrez_ids):
    # get pubmed ids associated with gene
    gene_pmids = gene_pmid_mapping[gene]

    if i % 100 == 0:
        print(f"gene {i}/{num_genes}...")

    for j, chemical in enumerate(mesh_ids):
        # get pubmed ids associated with chemical
        chemical_pmids = chem_pmid_mapping[chemical]

        # compute gene-chemical co-occurrence count
        num_shared = len(set(gene_pmids).intersection(chemical_pmids))

        comat[i, j] = num_shared

# store gene-chemical co-occurrence matrix
comat = pd.DataFrame(comat, index=entrez_ids, columns=mesh_ids)
comat.reset_index().rename(columns={'index': 'entrez_id'}).to_feather(snek.output[0])
