"""
Create a mapping from chemical mesh ids to pubmed article ids
"""
import json
import numpy as np
import pandas as pd

snek = snakemake

# load chemical data
chemical_dat = pd.read_feather(snek.input[0])

# convert concept id to pyarrow/string type (~7x faster in testing..)
chemical_dat.concept_id = chemical_dat.concept_id.astype('string[pyarrow]')

# baseline
# %timeit chemical_dat.concept_id == mesh_id
# 3.13 s ± 49.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# string
# %timeit chemical_dat.concept_id == mesh_id
# 4.25 s ± 33.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# string[pyarrow]
# %timeit  chemical_dat.concept_id == mesh_id
# 428 ms ± 48.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# iterate over chemicals
mesh_ids = list(chemical_dat.concept_id.unique())
num_chemicals = len(mesh_ids)

# iterate over chemicals and retrieve associated pubmed ids for each
chemical_pmids = {}

for i, mesh_id in enumerate(mesh_ids):
    # slow step..
    mask = chemical_dat.concept_id == mesh_id

    pmids = list(set(chemical_dat[mask].pmid.values))

    if len(pmids) > 0:
        chemical_pmids[mesh_id] = pmids

def encoder(obj) -> int|list:
    """
    encoder to convert int64 elements to generic ints and sets to lists during
    json serialization
    """
    if isinstance(obj, np.generic):
        return obj.item()
    return obj

# store chemical -> pmid mapping as json
with open(snek.output[0], "wt", encoding="utf-8") as fp:
    fp.write(json.dumps(chemical_pmids, default=encoder))
