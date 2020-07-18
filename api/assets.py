import numpy as np
from sklearn.preprocessing import LabelEncoder


class LabelEncoder(LabelEncoder):
    """Override the LabelEncoder in order to use it on pipeline."""

    def fit_transform(self, y, *args, **kwargs):
        return super().fit_transform(np.array(y).ravel()).reshape(-1, 1)

    def transform(self, y, *args, **kwargs):
        return super().transform(np.array(y).ravel()).reshape(-1, 1)
