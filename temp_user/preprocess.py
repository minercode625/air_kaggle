from sklearn.preprocessing import MinMaxScaler


def preprocess(x_tr, x_ts):
    scaler = MinMaxScaler()
    scaler.fit(x_tr)
    return scaler.transform(x_tr), scaler.transform(x_ts)
