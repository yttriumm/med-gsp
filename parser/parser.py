from models import Database
from datasets import TESTDATASET



def parse_dataset(filename: str) -> Database:
    database = []
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            sequence_str = line.strip().split("-2")[0]
            itemsets_str = [its for its in sequence_str.split("-1") if its]
            sequence = []
            for itemset in itemsets_str:
                items_str = [i for i in itemset.strip().split(" ") if i]
                if items_str:
                    sequence.append(sorted(int(i) for i in items_str))
            database.append(sequence)
    return database



if __name__ == "__main__":
    db = parse_dataset(TESTDATASET)
    for sequence in db:
        print(sequence)