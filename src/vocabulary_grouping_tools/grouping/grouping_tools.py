

def make_all_subseqs(_iterable):
    return [_iterable[i:j] for i in range(len(_iterable)) for j in range(i+1, len(_iterable)+1)]
