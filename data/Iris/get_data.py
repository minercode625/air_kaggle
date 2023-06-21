import glob
import os
import pandas as pd


def get_tr_ts_data():
    pattern = "*.csv"
    a = os.getcwd()
    tr_name = glob.glob(os.path.join("./data/Iris/train", pattern))
    ts_name = glob.glob(os.path.join("./data/Iris/test", pattern))
    tr_data = pd.read_csv(tr_name[0])
    ts_data = pd.read_csv(ts_name[0])
    x_tr = tr_data.iloc[:, :-1]
    y_tr = tr_data.iloc[:, -1]
    x_ts = ts_data.iloc[:, :-1]
    y_ts = ts_data.iloc[:, -1]

    return x_tr, y_tr, x_ts, y_ts
