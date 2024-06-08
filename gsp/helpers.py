from typing import List, Dict

from models import Sequence, Database


def is_subsequence_of(smaller: Sequence, bigger: Sequence) -> bool:
    bigger_iter = iter(bigger)
    for smaller_itemset in smaller:
        while True:
            try:
                bigger_itemset = next(bigger_iter)
                if set(smaller_itemset) <= set(bigger_itemset):
                    break
            except StopIteration:
                return False
    return True


def count_support(db: Database, sequences: List[Sequence]):
    supports: Dict[int, int] = {index: 0 for index, seq in enumerate(sequences)}
    for record in db:
        for index, seq in enumerate(sequences):
            if is_subsequence_of(seq, record):
                supports[index] += 1
    return supports


def join(seq1: Sequence, seq2) -> List[Sequence] | bool:
    if not len(seq1) or not len(seq2):
        return False
    if seq1 == seq2:
        return False
    if not len([i for t in seq1 for i in t]) == len([i for t in seq2 for i in t]):
        return False
    if len(seq1[0]) > 1:
        seq1_without_first = [seq1[0][1:], *seq1[1:]]
    else:
        seq1_without_first = seq1[1:]
    last_in_seq2_is_alone = len(seq2[-1]) < 2
    if not last_in_seq2_is_alone:
        seq2_without_last = [*seq2[:-1], seq2[-1][:-1]]
    else:
        seq2_without_last = seq2[:-1]
    if not seq2_without_last == seq1_without_first:
        return False
    with_second_as_separate = [*seq1, [seq2[-1][-1]]]
    with_second_as_element = [*seq1[:-1], [*sorted(list({*seq1[-1], seq2[-1][-1]}))]]
    return [with_second_as_separate, with_second_as_element]

