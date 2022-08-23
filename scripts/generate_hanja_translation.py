from vocabulary_grouping_tools.ingestion.api_ingest import get_english_translation
import pandas as pd
import yaml


from vocabulary_grouping_tools.grouping.grouping_tools import make_all_subseqs


def cutoff_ending(hanja_word):
    if hanja_word.endswith('하다'):
        return hanja_word[:-2]
    elif hanja_word.endswith('다'):
        return hanja_word[:-1]
    else:
        return hanja_word


SECRETS_FILE = 'metadata/secrets.yml'
secrets = yaml.safe_load(open(SECRETS_FILE, 'r'))

INPUT_FILE = 'input_files_from_output/vocab_active_korean_1_2_ttmik_1_2_refined_with_hanja.csv'
HANJA_COL_NAME = 'hanja_word'
vocab = pd.read_csv(INPUT_FILE)

HANJA_SUBSEQ_COL_NAME = 'hanja_subsequence'
FILE_ALREADY_GENERATED = 'metadata/hanja_subsequence_translation_part1.csv'
known_translation_df = pd.read_csv(FILE_ALREADY_GENERATED)

known_subseqs = set([_word for _word in known_translation_df[HANJA_SUBSEQ_COL_NAME] if str(_word) != 'nan'])

hanja_words = [_word for _word in vocab[HANJA_COL_NAME] if str(_word) != 'nan']

subseq_set = set()
for hangul_wrd in list(hanja_words):
    subseq_set.update(make_all_subseqs(cutoff_ending(hangul_wrd)))

unknown_subseqs = subseq_set.difference(known_subseqs)
translation_for_subseq = {}
for index, subseq in enumerate(unknown_subseqs):
    print(f'Now getting translation for subseq {index+1} of {len(unknown_subseqs)}: {subseq}')
    english_trans = get_english_translation(subseq, secrets['client_id'],
                                            secrets['client_secret'],
                                            source_language='zh-TW')
    print(f'Translation is {english_trans}')
    print()
    translation_for_subseq[subseq] = english_trans

df_of_seq_translation = pd.DataFrame(translation_for_subseq.items()).rename(columns={
    0: HANJA_SUBSEQ_COL_NAME,
    1: 'english_translation'
})

df_of_seq_translation.to_csv('metadata/hanja_subsequence_translation_part2.csv')
