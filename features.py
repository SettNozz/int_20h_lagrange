from h3 import h3
import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import path
from datetime import datetime


def find_hexagon_id_of_pickup_coords(hexagon_frame, frame):
    pickup_coords = np.array(frame[['pickup_lat', 'pickup_lng']])

    hexagon_arr = np.array(hexagon_frame)[:, 1:]
    hexagon_ids = np.array(hexagon_frame['hexagon_id'])

    hexagon_pickup_ids = []

    for coord_ind, pickup_coord in tqdm(enumerate(pickup_coords)):
        # TODO: use kNN for optimization
        for hexagon_ind, hexagon in enumerate(hexagon_arr):
            hexagon = np.array([hexagon[0:6], hexagon[6:]]).reshape(-1, 6).T
            hexagon_path = path.Path(hexagon)

            if hexagon_path.contains_points([(pickup_coord[0], pickup_coord[1])]):
                hexagon_pickup_ids.append(hexagon_ids[hexagon_ind])
                break
            elif hexagon_ind == hexagon_arr.shape[0]-1:
                hexagon_pickup_ids.append(None)
            else:
                continue

    return hexagon_pickup_ids


def time_discretization(frame):
    week_day, weekend, month, year = [], [], [], []

    for raw in frame.iterrows():
        try:
            created_at = datetime.strptime(raw[1].created_at[:-3], '%Y-%m-%d %H:%M:%S.%f')
            weekday = created_at.weekday()
            week_day.append(int(weekday))

            weekend.append(True if weekday in (5, 6) else False)
            month.append(int(created_at.month))
            year.append(int(created_at.year))
        except:
            week_day.append(None)
            weekend.append(None)
            month.append(None)
            year.append(None)

    time_period_frame = pd.DataFrame({'week_day': week_day, 'weekend': weekend, 'month': month, 'year': year})
    return time_period_frame


def create_city_hexagons(lat=49.83826, lon=24.02324):
    """
    For Lviv, coordinates: 49.83826, 24.02324.
    Function, for deviding city into regions, and save coordinates for this boundaries to DF.
    Coordinates must be a city center from OpenStreetMap

    Takes:
        lat: float value of latitude
        lon: float value of longitude
    Return:
        df with coordinates

    """
    h3_address = h3.geo_to_h3(lat, lon, 8)
    hexagons = h3.k_ring_distances(h3_address, 6)
    list_address = [hex for el in hexagons for hex in el]

    latitudes1, latitudes2, latitudes3, latitudes4, latitudes5, latitudes6 = \
        list(), list(), list(), list(), list(), list()
    longitudes1, longitudes2, longitudes3, longitudes4, longitudes5, longitudes6 = \
        list(), list(), list(), list(), list(), list()
    hexagon_id = list()

    for index, element in enumerate(list_address):
        hex_boundary = h3.h3_to_geo_boundary(element)
        hexagon_id.append(index + 1)
        latitudes1.append(hex_boundary[0][0])
        longitudes1.append(hex_boundary[0][1])
        latitudes2.append(hex_boundary[1][0])
        longitudes2.append(hex_boundary[1][1])
        latitudes3.append(hex_boundary[2][0])
        longitudes3.append(hex_boundary[2][1])
        latitudes4.append(hex_boundary[3][0])
        longitudes4.append(hex_boundary[3][1])
        latitudes5.append(hex_boundary[4][0])
        longitudes5.append(hex_boundary[4][1])
        latitudes6.append(hex_boundary[5][0])
        longitudes6.append(hex_boundary[5][1])

    df_address = pd.DataFrame({"hexagon_id": hexagon_id, "latitude1": latitudes1, "latitude2":latitudes2, 
                               "latitude3": latitudes3, "latitude4": latitudes4, "latitude5": latitudes5,
                               "latitude6": latitudes6, "longitude1": longitudes1, "longitude2": longitudes2,
                               "longitude3": longitudes3, "longitude4": longitudes4, "longitude5": longitudes5,
                               "longitude6": longitudes6})

    return df_address
