from sklearn.svm import SVC


def get_model():
    return SVC(kernel="linear", C=0.025, probability=True)
