import pandas as pd
import os

from vocabulary_grouping_tools.util.constants import HANGUL_COL_NM, HANJA_COL_NM, ENGLISH_COL_NM

STOP_WORDS = {
    'a',
    'at',
    'or',
    'to',
    'of',
    'in',
    'be',
    'that',
    'this',
    'for',
    'when',
    'the',
    'and',
    'do',
    'from'
}


FILE_NAME = 'vocab_active_korean_1_2_ttmik_1_2_refined'
EXTENSION = 'csv'
FILE_PATH = 'input_files_from_output'
OUTPUT_PATH = f'output/{FILE_NAME}'

refined_file_nm = f'{FILE_PATH}/{FILE_NAME}.{EXTENSION}'
print(refined_file_nm)
eng_korean_df = pd.read_csv(refined_file_nm).rename(columns={
    'english_phrase': 'hangeul_english_translation'
})

hangul_hanja_df = pd.read_csv('metadata/hanja_hangul_pairs.csv')

eng_korean_df['does_end_in_hada'] = eng_korean_df[HANGUL_COL_NM].apply(lambda x: x.endswith('하다'))

hanja_translation = pd.read_csv('metadata/hanja_subsequence_translation.csv').rename(
    columns={
        'english_translation': 'hanja_english_translation'
    }
)

hanja_translation = hanja_translation[hanja_translation['hanja_english_translation'].apply(
    lambda x: sum([_char.isalnum() for _char in x]) > 1)]


def remove_hada_if_there(row):
    if row['does_end_in_hada']:
        return row[HANGUL_COL_NM][:-2]
    else:
        return row[HANGUL_COL_NM]


eng_korean_df['hangul_word_wo_hada'] = eng_korean_df.apply(remove_hada_if_there, axis=1)
joined_df = eng_korean_df.set_index('hangul_word_wo_hada').join(hangul_hanja_df.set_index(HANGUL_COL_NM), how='left')

joined_df['hanja_exists'] = joined_df[HANJA_COL_NM].notna()


def add_hada_to_hanja_words(row):
    if row['does_end_in_hada'] and row['hanja_exists']:
        return row['hanja_word'] + '하다'
    else:
        return row['hanja_word']


joined_df['hanja_word_with_hada'] = joined_df.apply(add_hada_to_hanja_words, axis=1)

num_hangul_words = joined_df.groupby(HANGUL_COL_NM).agg('count')[HANJA_COL_NM].rename('num_hangul_words')
joined_df_2 = joined_df.join(num_hangul_words, on=HANGUL_COL_NM)

joined_df_2 = joined_df_2.reset_index().sort_values(['num_hangul_words', HANGUL_COL_NM], ascending=False)

joined_df_3 = joined_df_2.join(hanja_translation.set_index('hanja_subsequence'), on='hanja_word', how='left')


def do_english_defs_possibly_match(eng_def_1, eng_def_2):
    eng_def_1_words = set(str(eng_def_1).split(' ')).difference(STOP_WORDS)
    eng_def_2_words = set(str(eng_def_2).split(' ')).difference(STOP_WORDS)
    return len(eng_def_2_words.intersection(eng_def_1_words)) > 0


joined_df_3 = joined_df_3[joined_df_3.apply(
    lambda row: not row['hanja_exists'] or do_english_defs_possibly_match(
        row['hanja_english_translation'],
        row['hangeul_english_translation']),
    axis=1)]

os.makedirs(OUTPUT_PATH, exist_ok=True)
joined_df_3.to_csv(f'{OUTPUT_PATH}/{FILE_NAME}_with_hanja_v5.csv')
