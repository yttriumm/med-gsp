import pytest

from gsp.helpers import is_subsequence_of, count_support, join


@pytest.mark.parametrize("smaller,bigger,expected", [
    ([[3], [4, 5], [8]], [[7], [3, 8], [9], [4, 5, 6], [8]], True),
    ([[3], [5]], [[3, 5]], False),
    ([], [], True),
    ([[1], [2], [3, 4], [5]], [[1], [2]], False),
    ([[5, 3], [15]], [[10], [22], [5, 3], [2, 15]], True)
])
def test_issubsequence(smaller, bigger, expected):
    result = is_subsequence_of(smaller, bigger)
    assert result == expected

@pytest.fixture
def database():
    return [
        [[1, 2], [3, 4], [5], [6]],
        [[3], [4], [5], [6]],
        [[3,4], [4,5], [6]]
    ]


def test_count_support(database):

    records = [
        [[3], [5]],
        [[3]],
        [[4], [5]],
        [[4, 5]],
        [[1], [6]],
        [[4], [4]],
        [[5], [6]],
        [[1,2], [5,6]],
        []
    ]
    supports = count_support(database, records)
    assert supports == {
        0: 3,
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 1,
        6: 3,
        7: 0,
        8: 3
    }


@pytest.mark.parametrize("seq1,seq2,expected_result", [
    ([[1], [2], [3]], [[2], [3], [4]], [[[1], [2], [3], [4]], [[1], [2], [3, 4]]]),
    ([[1, 2], [3, 4], [5]], [[2], [3, 4], [5, 6]], [[[1, 2], [3, 4], [5], [6]], [[1, 2], [3, 4], [5, 6]]]),
    ([[1, 2], [3]], [[2], [3], [5]], [[[1, 2], [3], [5]], [[1, 2], [3, 5]]])
]
)
def test_join(seq1, seq2, expected_result):
    result = join(seq1, seq2)
    assert result == expected_result