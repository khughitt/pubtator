"""
Filter PubTator Central data

This script filters a raw data file from Pubtator Central removing problematic and low frequency
entries.
"""
import pandas as pd

# re-assign "snakemake" variable to hide warnings
snek = snakemake

# filtering settings
PMID_MAX_ENTRIES:int = snek.config['filtering']['pmid_max_entries']
MENTIONS_MIN_FREQ:int = snek.config['filtering']['mentions_min_freq']
CONCEPT_ID_MIN_FREQ:int = snek.config['filtering']['concept_id_min_freq']

# load data
infile:str = snek.input[0]

df = pd.read_csv(infile, sep='\t',
                 names=['pmid', 'type', 'concept_id', 'mentions', 'resource'],
                 dtype={'pmid': 'int32', 'type': 'category', 'concept_id': 'category',
                        'mentions': 'category', 'resource': 'category'},
                 quoting=3)

# remove entries whose "mentions" field contains tabs/newline characters;
# these are often associated with erroneous entries
contains_tab_or_newline = df.mentions.str.contains("\n") | df.mentions.str.contains("\t")
print(f"Removing {contains_tab_or_newline.sum()} entries with unexpected tab/newline characters")
df = df[~contains_tab_or_newline]

# remove articles with an unexpectedly large number of associated annotations
pmid_counts = df.pmid.value_counts()
to_keep = pmid_counts.index[pmid_counts <= PMID_MAX_ENTRIES]
mask = df.pmid.isin(to_keep)
print(f"Removing {(~mask).sum()} entries with > {PMID_MAX_ENTRIES} associated PMIDs")
df = df[mask]

# remove mentions with a small number of occurrences
mention_counts = df.mentions.value_counts()
to_keep = mention_counts.index[mention_counts >= MENTIONS_MIN_FREQ]
mask = df.mentions.isin(to_keep)
num_removed = (~mask).sum()
pct_removed = num_removed / len(mask) * 100
print(f"Removing {num_removed} ({pct_removed:0.2f}%) articles with mentions that appear < {MENTIONS_MIN_FREQ} times")
df = df[mask]

# remove concept ids with a small number of occurrences
concept_id_counts = df.concept_id.value_counts()
to_keep = concept_id_counts.index[concept_id_counts >= CONCEPT_ID_MIN_FREQ]
mask = df.concept_id.isin(to_keep)
print(f"Removing {(~mask).sum()} entries with concepts that appear < {CONCEPT_ID_MIN_FREQ} times")
df = df[mask]

# exclude concept ids listed as "-" (e.g. in chemical mesh ids)
mask = df.concept_id != "-"
print(f"Removing {(~mask).sum()} entries with missing concept IDs")
df = df[mask]

# drop category levels no longer needed
df.concept_id = df.concept_id.cat.remove_unused_categories()
df.mentions = df.mentions.cat.remove_unused_categories()
df.resource = df.resource.cat.remove_unused_categories()

# save filtered dataset
df.reset_index(drop=True).to_feather(snek.output[0])
