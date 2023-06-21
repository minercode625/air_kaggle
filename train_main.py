from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import importlib
import os


def train_main(model_path="", preproc_path="", data_name="Iris"):
    module_name = os.path.splitext(
        os.path.join("data", data_name, "get_data")
    )[0].replace("/", ".")
    data_module = importlib.import_module(module_name)
    x_tr, y_tr, x_ts, y_ts = data_module.get_tr_ts_data()
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


if __name__ == "__main__":
    train_main("temp_user/model", "temp_user/preprocess")
