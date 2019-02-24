import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn import metrics
from sklearn.cross_validation import KFold
from sklearn.preprocessing import normalize
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

from utils import delete_nones, encode_ids




def main():
    frame = pd.read_csv("../data/clear_data.scv")

    # DATA PREPROCESSING
    frame = delete_nones(frame)
    frame = encode_ids(frame)

    # FEATURE GENERATION
    X = ...
    y = ...

    # SPLIT DATA
    X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.75, random_state=42)

    X_test = test_df





if __name__ == '__main__':
    main()
