import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn import metrics
from sklearn.cross_validation import KFold
from sklearn.preprocessing import normalize
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

from utils import delete_nones, encode_ids
from features import time_discretization, check, check_point_inside_hexagon


def main():
    # TODO: insert data cleaning
    frame = pd.read_csv("../data/clear_data.scv")

    # DATA PREPROCESSING
    frame = delete_nones(frame)
    frame = encode_ids(frame)
    # delete canceled requests
    frame = frame[(frame['canceled_by_client'] == 0) & (frame['canceled_by_driver'] == 0)]

    # get hexagon frame
    hexagon_frame = ...

    # FEATURE GENERATION
    time_period_frame = time_discretization(frame=frame)



    # SPLIT DATA
    X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.9, random_state=42)

    X_test = test_df





if __name__ == '__main__':
    main()
