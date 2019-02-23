import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder


def delete_nones(frame):
    # select values whithout none for drive_id
    clear_frame = frame[frame['driver_id'].isna() == False]

    print('frame shape = ', frame.shape)
    print('clear frame shape = ', clear_frame.shape)

    return clear_frame


def encode_ids(frame):
    # ID encoding

    columns_id = ['ride_id', 'user_id', 'driver_id']

    for column_id in columns_id:
        le = LabelEncoder()
        frame[column_id] = le.fit_transform(frame[column_id])

    return frame




