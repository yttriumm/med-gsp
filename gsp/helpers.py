import functools
import math
from typing import List, Dict, Tuple, Union
from models import Sequence, Database


@functools.cache
def convert_data_sequence(data_sequence: Tuple[Tuple[int]]):
    times = {}
    for i in range(len(data_sequence)):
        for element in data_sequence[i]:
            if element not in times:
                times[element] = []
            times[element].append(i)
    return times


def contains_element(data_sequence: Dict[int, List[int]], element: List[int],
                     window_size: int = 0, start_time: int = 0) -> Union[bool, Tuple[int, int]]:
    try:
        times = {e: next(time for time in data_sequence[e] if time >= start_time) for index, e in enumerate(element)}
    except (StopIteration, KeyError):
        return False
    start_time = min(times.values())
    end_time = max(times.values())
    if end_time - start_time > window_size:
        return contains_element(data_sequence=data_sequence, element=element,
                                window_size=window_size, start_time=end_time - window_size)
    return start_time, end_time


def is_subsequence_of(smaller: Sequence, bigger: Sequence, min_gap: int = 0, max_gap: int = math.inf,
                      window_size: int = 0) -> bool:
    start_time = 0
    alternate_repr = convert_data_sequence(tuple(tuple(i for i in its) for its in bigger))
    index_to_times: Dict[int, int | None] = {i: None for i in range(len(smaller))}
    smaller_index = 0
    while smaller_index < len(smaller):
        result_for_index = contains_element(data_sequence=alternate_repr, element=smaller[smaller_index],
                                            window_size=window_size, start_time=start_time)
        if not result_for_index:
            return False
        index_to_times[smaller_index] = result_for_index
        if not smaller_index == 0:
            times_for_previous = index_to_times[smaller_index - 1]
            if result_for_index[1] - times_for_previous[0] > max_gap:
                smaller_index -= 1
                start_time = result_for_index[1] - max_gap
                continue
        smaller_index += 1
        index_to_times[smaller_index] = result_for_index
        start_time = result_for_index[1] + min_gap + 1
        continue
    return True


def count_support(db: Database, sequences: List[Sequence], min_gap: int = 0, max_gap: int = math.inf,
                  window_size: int = 0):
    supports: Dict[int, int] = {index: 0 for index, seq in enumerate(sequences)}
    for record in db:
        for index, seq in enumerate(sequences):
            if is_subsequence_of(seq, record, min_gap=min_gap, max_gap=max_gap, window_size=window_size):
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
