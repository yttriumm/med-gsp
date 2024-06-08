from typing import List

import pytest

from gsp.main import generate_candidates, generate_initial_candidates, prune_candidates, gsp_algorithm
from models import Sequence


@pytest.mark.parametrize("k_sequences,expected_candidates", [
    ([
         [[1, 2], [3]],
         [[1, 2], [4]],
         [[1], [3, 4]],
         [[1, 3], [5]],
         [[2], [3, 4]],
         [[2], [3], [5]]
     ],
     [[[1, 2], [3], [4]], [[1, 2], [3, 4]], [[1, 2], [3], [5]], [[1, 2], [3, 5]]]),
    ([
         [[1, 2]],
         [[2, 3]],
         [[3], [4]],
         [[2, 4]],
         [[2], [2]]
     ],
     [[[1, 2], [3]],
      [[1, 2, 3]],
      [[1, 2], [4]],
      [[1, 2, 4]],
      [[1, 2], [2]],
      [[1, 2]],
      [[2, 3], [4]],
      [[2, 3, 4]],
      [[2], [2], [3]],
      [[2], [2, 3]],
      [[2], [2], [4]],
      [[2], [2, 4]]])
])
def test_generate_candidates(k_sequences: List[Sequence], expected_candidates: List[Sequence]):
    candidates = generate_candidates(k_sequences)
    assert candidates == expected_candidates


@pytest.mark.parametrize("database,expected_candidates", [
    ([
         [[1], [4], [1, 7]],
         [[2, 4], [5], [1]],
         [[7, 4, 12], [5]]
     ],
     [[[1]], [[2]], [[4]], [[5]], [[7]], [[12]]])
])
def test_generate_initial_candidates(database: List[Sequence], expected_candidates):
    candidates = generate_initial_candidates(database)
    assert candidates == expected_candidates


@pytest.fixture
def database_for_pruning():
    return [
        [[1], [2], [3, 4]],
        [[2, 3], [4, 5], [6]],
        [[1, 3], [2], [7]]
    ]


@pytest.mark.parametrize("sequences,expected_result", [
    ([
         [[2], [4]],
         [[3], [4]],
         [[1, 3], [7]]
     ], [
         ([[2], [4]], 2)
     ])
])
def test_prune_candidates(database_for_pruning: List[Sequence], sequences: List[Sequence],
                          expected_result: List[Sequence]):
    result = prune_candidates(database=database_for_pruning, sequences=sequences, min_sup=1)
    assert result == expected_result
