"""
Creates a disease-disease co-occurrence matrix
"""
import json
import pandas as pd
import numpy as np

snek = snakemake

# load disease/pmid mapping
with open(snek.input[0]) as fp:
    disease_pmids = json.load(fp)

# create empty matrix to store disease-disease co-occurrence counts
mesh_ids = list(disease_pmids.keys())
num_diseases = len(mesh_ids)

comat = np.zeros((num_diseases, num_diseases), dtype=np.uint32)

# get upper triangular matrix indices
ind = np.triu_indices(num_diseases, k=1)

# iterate over pairs of diseases
for cur_ind in range(len(ind[0])):
    i = ind[0][cur_ind]
    j = ind[1][cur_ind]

    disease1 = mesh_ids[i]
    disease2 = mesh_ids[j]

    disease1_pmids = disease_pmids[disease1]
    disease2_pmids = disease_pmids[disease2]

    # compute disease-disease co-occurrence count
    num_shared = len(set(disease1_pmids).intersection(disease2_pmids))

    comat[i, j] = comat[j, i] = num_shared

# store disease-disease co-occurrence matrix
comat = pd.DataFrame(comat, index=mesh_ids, columns=mesh_ids)
comat.reset_index().rename(columns={'index': 'mesh_id'}).to_feather(snek.output[0])
