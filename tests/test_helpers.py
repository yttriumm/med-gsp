import pytest

from gsp.helpers import is_subsequence_of, count_support, join, contains_element, convert_data_sequence


@pytest.mark.parametrize("smaller,bigger,min_gap,max_gap,window_size,expected", [
    ([[3], [4, 5], [8]], [[7], [3, 8], [9], [4, 5, 6], [8]], 0, 50, 0, True),
    ([[3], [5]], [[3, 5]], 0, 50, 0,  False),
    ([], [], 0, 50, 0,  True),
    ([[1], [2], [3, 4], [5]], [[1], [2]], 0, 50, 0,  False),
    ([[5, 3], [15]], [[10], [22], [5, 3], [2, 15]], 0, 50, 0,  True),
    ([[5, 22], [15]], [[10], [22], [5, 3], [2, 15]], 0, 2, 1,  True),
    ([[5, 22], [15]], [[10], [22], [5, 3], [2, 15]], 0, 1, 1,  False),
    ([[10], [22]], [[10], [22], [5, 3], [2, 15]], 1, 1, 1,  False),
    ([[10], [22]], [[10], [22], [5, 3], [2, 15]], 1, 1, 1,  False),
    ([[2], [4], [3], [4]], [[1, 2],[3, 4]], 0, 50, 0, False),
    ([[5], [4, 5], [4, 5], [4, 5]], [[1], [2], [3], [4, 5]], 0, 50, 0, False)

])
def test_issubsequence(smaller, bigger, min_gap, max_gap, window_size,expected):
    result = is_subsequence_of(smaller, bigger, min_gap=min_gap, max_gap=max_gap, window_size=window_size)
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



@pytest.mark.parametrize("data_sequence,element,window_size,start_time,expected_result", [
    ([[1], [1], [2], [3]], [1, 2],  0, 0, False),
    ([[1], [1], [2], [3]], [1, 2], 1,  0, (1, 2)),
    ([[1], [1, 2], [2], [3]], [1, 2], 0,  0, (1, 1)),
    ([[1], [1, 3], [2], [3]], [3], 0,  0, (1, 1)),
    ([[1], [1, 3], [2], [3]], [3], 0,  0, (1, 1)),
    ([[1], [1, 3], [2], [3]], [1, 2], 1,  1, (1, 2)),
    ([[1, 2], [1, 2], [1, 2], [1]], [1, 2], 3,  1, (1, 1)),
    ([[1], [3], [2], [3]], [1, 2], 1,  0, False),




])
def test_contains_element(data_sequence, element,  window_size, start_time, expected_result):
    converted_sequence = convert_data_sequence(data_sequence)
    result = contains_element(converted_sequence, element,  window_size, start_time)
    assert result == expected_result