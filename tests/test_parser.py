from datasets import TESTDATASET
from parser.parser import parse_dataset


def test_parser():
    db = parse_dataset(TESTDATASET)
    assert db == [
        [[10, 108, 192], [3, 132, 288]],
        [[1, 10, 67, 139, 212, 229, 236]],
        [[120, 229], [148, 208]]
    ]