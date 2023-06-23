import pandas as pd
import glob
import os


def load_data(path):
    data = pd.read_csv(path)
    return data


class Performance:
    def __init__(self, dataname, username, acc):
        self.dataname = dataname
        self.username = username
        self.acc = acc

    def __str__(self):
        return f"{self.dataname} {self.username} {self.acc}"

    # For compare
    def __lt__(self, other):
        return self.acc < other.acc


def main():
    pattern = "*.csv"
    tr_name = glob.glob(os.path.join("data/train", pattern))
    ts_name = glob.glob(os.path.join("data/test", pattern))
    print(tr_name)
    print(ts_name)


if __name__ == "__main__":
    main()
