import re
import pandas as pd
import itertools

vocab = pd.read_csv('input_files_from_output/vocab_active_korean_1_2_ttmik_1_2_refined_with_hanja.csv')


def _get_translation_dict(writing_system):
    file_name = f'metadata/{writing_system}_subsequence_translation.csv'
    translation_df = pd.read_csv(file_name)
    return {
        _dict[f'{writing_system}_subsequence']: _dict['english_translation']
        for _dict in translation_df.to_dict(orient='records')
    }


def cutoff_ending(_word):
    if _word.endswith('하다'):
        return _word[:-2]
    elif _word.endswith('다'):
        return _word[:-1]
    else:
        return _word


english_trans_for_hangeul = _get_translation_dict('hangeul')
english_trans_for_hanja = {
    _subseq: _trans
    for _subseq, _trans in _get_translation_dict('hanja').items()
    if sum([_char.isalnum() for _char in _trans]) > 1
}

vocab = vocab[vocab['hanja_word'].apply(lambda x: x in english_trans_for_hanja)]

divider_to_use = ['|', '/']
def get_word_break_lists(_word_0):
    if str(_word_0).lower() == 'nan':
        return []
    _word = cutoff_ending(_word_0)
    if len(_word) < 2:
        return [_word]
    word_break_lists = []
    num_dividers = len(_word) - 1
    for divider_set in itertools.product(*([divider_to_use] * num_dividers)):
        current_word = ''
        for _seq, _div in zip(_word[:-1], divider_set):
            current_word += ''.join([_seq, _div])
        current_word += _word[-1]
        word_to_split = current_word.replace('/', '')
        word_break_lists.append(word_to_split.split('|'))
    return word_break_lists


vocab['hangul_syll_chains'] = vocab['hangul_word'].apply(get_word_break_lists)
vocab['hanja_syll_chains'] = vocab['hanja_word'].apply(get_word_break_lists)


def _get_hangul_hanja_chains(hangul_chains, hanja_chains):
    if len(hanja_chains) > 0:
        return list(zip(hangul_chains, hanja_chains))
    else:
        return [(_chain, []) for _chain in hangul_chains]


def _get_chain(word_chain, engish_trans):
    return ' + '.join([
        f'{syll} ({engish_trans.get(syll)})'
        for syll in word_chain
    ])


vocab['hangul_hanja_chains'] = vocab.apply(lambda row: _get_hangul_hanja_chains(
    row['hangul_syll_chains'], row['hanja_syll_chains']), axis=1)

vocab2 = vocab.explode('hangul_hanja_chains').rename(columns = {
    'hangul_hanja_chains': 'hangul_hanja_subseq_chain'
})


vocab2['hangul_chain_with_trans'] = vocab2['hangul_hanja_subseq_chain'].apply(
    lambda x: _get_chain(x[0], english_trans_for_hangeul))


vocab2['hanja_chain_with_trans'] = vocab2['hangul_hanja_subseq_chain'].apply(
    lambda x: _get_chain(x[1], english_trans_for_hanja))


vocab2 = vocab2[vocab2['hangul_word'].apply(lambda x: len(x) > 1)]
vocab2.to_csv('output/starter_vocab_with_extensive_chain__multi_syll_words.csv')
