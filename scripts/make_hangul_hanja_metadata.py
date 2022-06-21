"""
This is a one-off script to take the
metadata in metadata/hanja-0.0.7
and make a csv of the hangul hanja pairs
"""
import pandas as pd

METADATA_FILE_PATH_INPUT = 'metadata/hanja-0.0.7/dic4.txt'
METADATA_FILE_PATH_OUTPUT = 'metadata/hanja_hangul_pairs.csv'

HANJA_COL_NAME = 'hanja_word'
HANGUL_COL_NAME = 'hangul_word'

with open(METADATA_FILE_PATH_INPUT, 'r') as f:
    file_lines = [_line for _line in f.read().split('\n')
                  if not _line.startswith('#')]

hanja_hangul_df = pd.DataFrame([tuple(_line.split('\t'))
                                for _line in file_lines])\
    .rename(columns={
        0: HANJA_COL_NAME,
        1: HANGUL_COL_NAME
    })

hanja_hangul_df.to_csv(METADATA_FILE_PATH_OUTPUT, index=False)