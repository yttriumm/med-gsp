import math
from typing import List
from gsp.helpers import join, count_support
from models import Sequence
from parser.parser import parse_dataset


def generate_candidates(k_sequences: List[Sequence]):
    candidates = []
    for seq1 in k_sequences:
        for seq2 in k_sequences:
            join_result = join(seq1, seq2)
            if join_result:
                for r in join_result:
                    if r not in candidates:
                        candidates.append(r)
    return candidates


def generate_initial_candidates(database: List[Sequence]) -> List[Sequence]:
    items = set()
    for sequence in database:
        for transaction in sequence:
            for item in transaction:
                items.add(item)

    return [[[i]] for i in sorted(list(items))]


def prune_candidates(database: List[Sequence], sequences: List[Sequence], min_sup: int = 0, min_gap: int = 0,
                     max_gap: int = 0, window_size: int = 0):
    support_map = count_support(database, sequences=sequences, min_gap=min_gap, max_gap=max_gap,
                                window_size=window_size)
    return [(seq, support_map[index]) for index, seq in enumerate(sequences) if support_map[index] > min_sup]


def gsp_algorithm(database: List[Sequence], min_sup=1, min_gap=0, max_gap=math.inf, window_size=0):
    candidates = generate_initial_candidates(database)
    candidates_pruned_with_support = prune_candidates(database=database, sequences=candidates, min_sup=min_sup,
                                                      min_gap=min_gap, max_gap=int(max_gap), window_size=window_size)
    sequences = [*candidates_pruned_with_support]
    while len(candidates_pruned_with_support):
        candidates = generate_candidates([c[0] for c in candidates_pruned_with_support])
        candidates_pruned_with_support = prune_candidates(database=database, sequences=candidates, min_sup=min_sup,
                                                          min_gap=min_gap, max_gap=int(max_gap),
                                                          window_size=window_size)
        sequences.extend(candidates_pruned_with_support)

    return sequences


if __name__ == "__main__":
    _database = parse_dataset("datasets/leviathan.txt")
    _min_sup = 2
    _min_gap = 0
    _max_gap = 600
    _window_size = 0
    result = gsp_algorithm(database=_database, min_sup=_min_sup, min_gap=_min_gap, max_gap=_max_gap,
                           window_size=_window_size)
    for transaction_with_support in result:
        print(f"Sequence: {transaction_with_support[0]} support: {transaction_with_support[1]}")
