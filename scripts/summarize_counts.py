"""
Summarizes concept_id and mentions counts
"""
import pandas as pd

snek = snakemake

df = pd.read_feather(snek.input[0])

# count concept ids
concept_counts = df.concept_id.value_counts().to_frame()

concepts = df.concept_id.value_counts().to_frame().reset_index()
concepts = concepts.rename(columns={'concept_id': 'n', 'index': 'concept_id'})

# count mentions
mention_counts = df.mentions.value_counts().to_frame()

mentions = df.mentions.value_counts().to_frame().reset_index()
mentions = mentions.rename(columns={'mentions': 'n', 'index': 'mentions'})

# store results
concepts.to_feather(snek.output[0])
mentions.to_feather(snek.output[1])
