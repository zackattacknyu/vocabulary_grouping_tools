import pandas as pd

from vocabulary_grouping_tools.util.constants import HANGUL_COL_NM, ENGLISH_COL_NM
from vocabulary_grouping_tools.util.korean_util import is_one_char_hangul


"""
Converts a string to a dictionary of hangul, english definitions

String must be in one of the following forms: 
 <hangul_word> <non-hangul characters> <hangul_word> <non-hangul characters>
 <non-hangul characters> <hangul_word> <non-hangul characters> <hangul_word>
 <non-hangul characters>

"""
def str_to_english_hangul_pairs(str_with_info):
    if len(str_with_info) < 1 or str_with_info.startswith('#'):
        return []

    str_parts = str_with_info.split(' ')

    if len(str_parts) < 1:
        return []

    hangul_words_indices = [(_ind, _part) for _ind, _part in enumerate(str_parts) if is_one_char_hangul(_part)]

    # no english, hangul pairs detected
    if len(hangul_words_indices) < 1:
        return []

    hangul_indexes = [tup[0] for tup in hangul_words_indices]
    hangul_words = [tup[1] for tup in hangul_words_indices]

    if hangul_indexes[0] < 1:
        hangul_indexes.append(len(str_parts))
    else:
        hangul_indexes = [-1] + hangul_indexes

    english_phrases = [
        ' '.join(str_parts[init_ind+1:end_ind])
        for init_ind, end_ind in zip(hangul_indexes[:-1], hangul_indexes[1:])
    ]

    if len(hangul_words) != len(english_phrases):
        print(len(hangul_words))
        print(len(english_phrases))
        for _ind in range(min(len(hangul_words), len(english_phrases))):
            print(f'Index {_ind} ; Hangul: {hangul_words[_ind]} ; English: {english_phrases[_ind]}')
    assert len(hangul_words) == len(english_phrases)

    return [
        {
            HANGUL_COL_NM: hangul_word,
            ENGLISH_COL_NM: english_phrase
        }
        for hangul_word, english_phrase
        in zip(hangul_words, english_phrases)
    ]


def text_block_to_english_hangul_pairs(text_block):
    output_pairs = []
    for _line in text_block.split('\n'):
        output_pairs.extend(str_to_english_hangul_pairs(_line))
    return output_pairs


def text_block_to_english_hangul_df(text_block):
    return pd.DataFrame(text_block_to_english_hangul_pairs(text_block))
