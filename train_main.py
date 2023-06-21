from utils import load_data
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import importlib
import glob
import os


def get_tr_ts_data():
    pattern = "*.csv"
    tr_name = glob.glob(os.path.join("data/train", pattern))
    ts_name = glob.glob(os.path.join("data/test", pattern))
    tr_data = load_data(tr_name[0])
    ts_data = load_data(ts_name[0])
    x_tr = tr_data.iloc[:, :-1]
    y_tr = tr_data.iloc[:, -1]
    x_ts = ts_data.iloc[:, :-1]
    y_ts = ts_data.iloc[:, -1]

    return x_tr, y_tr, x_ts, y_ts


def train_main(model_path="", preproc_path=""):
    x_tr, y_tr, x_ts, y_ts = get_tr_ts_data()
    if model_path == "":
        model = KNeighborsClassifier(n_neighbors=3)
    else:
        module_name = os.path.splitext(model_path)[0].replace("/", ".")
        model_module = importlib.import_module(module_name)
        model = model_module.get_model()

    if preproc_path != "":
        module_name = os.path.splitext(preproc_path)[0].replace("/", ".")
        preproc_module = importlib.import_module(module_name)
        x_tr, x_ts = preproc_module.preprocess(x_tr, x_ts)

    model = model.fit(x_tr, y_tr)
    y_pred = model.predict(x_ts)
    acc = accuracy_score(y_ts, y_pred)
    print("Accuracy: ", acc)


if __name__ == "__main__":
    train_main("temp_user/model", "temp_user/preprocess")
