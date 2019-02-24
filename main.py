import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn import metrics
from sklearn.cross_validation import KFold
from sklearn.preprocessing import normalize
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

from utils import delete_nones, encode_ids
from features import time_discretization, find_hexagon_id_of_pickup_coords, create_city_hexagons


def main(features = False, discr_period = 0.05):
    # TODO: insert data cleaning
    if not features:
        frame = pd.read_csv("./data/clear_data.csv")

        # DATA PREPROCESSING
        frame = delete_nones(frame)
        frame = encode_ids(frame)
        # delete canceled requests
        frame = frame[(frame['canceled_by_client'] == 0) & (frame['canceled_by_driver'] == 0)]

        # get hexagon frame
        # TODO: pass params of city
        hexagon_frame = create_city_hexagons()

        # TODO: add city column
        # FEATURE GENERATION
        time_period_frame = time_discretization(frame=frame)
        frame['week_day'], frame['weekend'], frame['month'], frame['year'] = time_period_frame['week_day'], \
                                                                             time_period_frame['weekend'], \
                                                                             time_period_frame['month'], \
                                                                             time_period_frame['year']
        frame['hexagon_id'] = find_hexagon_id_of_pickup_coords(hexagon_frame, frame)
        frame= frame.dropna()
        frame = frame.reset_index(drop=True)

        features = frame.groupby(['week_day', 'month', 'year', 'hexagon_id']).count()
        feature_frame = features.reset_index()
        feature_frame = feature_frame[['week_day', 'month', 'year', 'hexagon_id', 'ride_id']]
        feature_frame.columns = ['week_day', 'month', 'year', 'hexagon_id', 'num_in']
        feature_frame['weekend'] = [True if weekday in (5, 6) else False for weekday in feature_frame.week_day.values]
        feature_frame['ride_distance'] = frame.groupby(['week_day', 'month', 'year', 'hexagon_id']).sum()['ride_distance'].values

        feature_frame['load_coef'] = feature_frame.num_in / feature_frame.num_in.max()

        feature_frame['weekend'] = feature_frame['weekend'].apply(int)
        feature_frame['load_coef'] = (feature_frame['load_coef'] // discr_period) * discr_period

        # save feature frame
        feature_frame.to_csv("./data/features.scv", index=False)
    else:
        feature_frame = pd.read_csv("./data/features.csv")



    # # SPLIT DATA
    # X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.9, random_state=42)
    #
    # # X_test = test_df




if __name__ == '__main__':
    main()
