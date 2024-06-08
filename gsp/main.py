from typing import List
from gsp.helpers import join, count_support
from models import Sequence


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


def prune_candidates(database: List[Sequence], sequences: List[Sequence], min_sup):
    support_map = count_support(database, sequences=sequences)
    return [(seq, support_map[index]) for index, seq in enumerate(sequences) if support_map[index] > min_sup]


def gsp_algorithm(database: List[Sequence], min_sup=1):
    candidates = generate_initial_candidates(database)
    candidates_pruned_with_support = prune_candidates(database=database, sequences=candidates, min_sup=min_sup)
    sequences = [*candidates_pruned_with_support]
    while len(candidates_pruned_with_support):
        candidates = generate_candidates([c[0] for c in candidates_pruned_with_support])
        candidates_pruned_with_support = prune_candidates(database=database, sequences=candidates, min_sup=min_sup)
        sequences.extend(candidates_pruned_with_support)

    return sequences


if __name__ == "__main__":
    min_sup = 3
    database = [
        [[1], [2], [3], [4]],
        [[1], [2], [4]],
        [[1], [2], [4], [5]],
        [[4], [5]],
        [[4], [5], [6]],
        [[4], [5], [6]],
        [[1, 2], [3, 4], [5, 6]],
        [[1, 2], [3, 4], [3, 4], [5]]
    ]
    result = gsp_algorithm(database=database, min_sup=min_sup)
    for transaction_with_support in result:
        print(f"Sequence: {transaction_with_support[0]} support: {transaction_with_support[1]}")




