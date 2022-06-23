
#Ref: https://github.com/JDongian/python-jamo/blob/d9ce26fd60a4011b80b7d78c016728b019afbca1/jamo/jamo.py#L146
def is_char_korean(_char):
    return 0xAC00 <= ord(_char) <= 0xD7A3


def is_word_all_hangul(_word):
    for letter in _word:
        if not is_char_korean(letter):
            return False
    return True


def is_one_char_hangul(_word):
    for letter in _word:
        if is_char_korean(letter):
            return True
    return False
