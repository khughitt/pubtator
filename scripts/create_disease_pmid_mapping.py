"""
Create a mapping from disease mesh ids to pubmed article ids
"""
import json
import numpy as np
import pandas as pd

snek = snakemake

# load disease data
disease_dat = pd.read_feather(snek.input[0])

# convert concept id to pyarrow/string type (~7x faster in testing..)
disease_dat.concept_id = disease_dat.concept_id.astype('string[pyarrow]')

mesh_ids = list(disease_dat.concept_id.unique())
num_diseases = len(mesh_ids)

# iterate over diseases and retrieve associated pubmed ids for each
disease_pmids = {}

for mesh_id in mesh_ids:
    mask = disease_dat.concept_id == mesh_id

    pmids = list(set(disease_dat[mask].pmid.values))

    if len(pmids) > 0:
        disease_pmids[mesh_id] = pmids

def encoder(obj) -> int|list:
    """
    encoder to convert int64 elements to generic ints and sets to lists during
    json serialization
    """
    if isinstance(obj, np.generic):
        return obj.item()
    return obj

# store disease -> pmid mapping as json
with open(snek.output[0], "wt", encoding="utf-8") as fp:
    fp.write(json.dumps(disease_pmids, default=encoder))
