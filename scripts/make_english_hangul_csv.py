import os

from vocabulary_grouping_tools.ingestion.english_korean_info_ingest import text_block_to_english_hangul_df
from vocabulary_grouping_tools.util.constants import HANGUL_COL_NM

FILE_NAME = 'vocab_active_korean_1_2_ttmik_1_2'
EXTENSION = 'txt'
FILE_PATH = 'input_external_files'
OUTPUT_PATH = f'output/{FILE_NAME}'

with open(f'{FILE_PATH}/{FILE_NAME}.{EXTENSION}', 'r') as f:
    block = f.read()


eng_hangul_df = text_block_to_english_hangul_df(block)
eng_hangul_df = eng_hangul_df.sort_values(HANGUL_COL_NM)

os.makedirs(OUTPUT_PATH, exist_ok=True)
eng_hangul_df.to_csv(f'output/{FILE_NAME}/{FILE_NAME}_table.csv', index=False)
