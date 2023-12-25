"""
Creates a chemical-chemical co-occurrence matrix
"""
import json
import pandas as pd
import numpy as np

snek = snakemake

# load chemical/pmid mapping
with open(snek.input[0]) as fp:
    unfiltered_chemical_pmids = json.load(fp)

# filter any chemicals with less than N citations; helps keep the co-occurrence
# matrix size more manageable while only losing relatively low-information
# low-citation counts..
concept_id_min_freq = snek.config["filtering"]["chem_comat_concept_id_min_freq"]

chemical_pmids = {}

for mesh_id in unfiltered_chemical_pmids:
    if len(unfiltered_chemical_pmids[mesh_id]) > concept_id_min_freq:
        chemical_pmids[mesh_id] = unfiltered_chemical_pmids[mesh_id]

# create empty matrix to store chemical-chemical co-occurrence counts
mesh_ids = list(chemical_pmids.keys())
num_chemicals = len(mesh_ids)

comat = np.zeros((num_chemicals, num_chemicals), dtype=np.uint32)

# get upper triangular matrix indices
ind = np.triu_indices(num_chemicals, k=1)

# iterate over pairs of chemicals
for cur_ind in range(len(ind[0])):
    i = ind[0][cur_ind]
    j = ind[1][cur_ind]

    chemical1 = mesh_ids[i]
    chemical2 = mesh_ids[j]

    chemical1_pmids = chemical_pmids[chemical1]
    chemical2_pmids = chemical_pmids[chemical2]

    # compute chemical-chemical co-occurrence count
    num_shared = len(set(chemical1_pmids).intersection(chemical2_pmids))

    comat[i, j] = comat[j, i] = num_shared

# store chemical-chemical co-occurrence matrix
comat = pd.DataFrame(comat, index=mesh_ids, columns=mesh_ids)
comat.reset_index().rename(columns={"index": "mesh_id"}).to_feather(snek.output[0])
