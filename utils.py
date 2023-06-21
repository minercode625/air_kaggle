import pandas as pd
import glob
import os


def load_data(path):
    data = pd.read_csv(path)
    return data


def main():
    pattern = "*.csv"
    tr_name = glob.glob(os.path.join("data/train", pattern))
    ts_name = glob.glob(os.path.join("data/test", pattern))
    print(tr_name)
    print(ts_name)


if __name__ == "__main__":
    main()
