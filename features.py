import pandas as pd
import numpy as np
from matplotlib import path
from datetime import datetime, timedelta


def check_point_inside_hexagon(counter,area,coordinates):
    p = path.Path(area)  
    if p.contains_points([(coordinates[0],coordinates[1])]) == True:
        counter += 1
    return counter

def check(area): #main function
    pickup_coords = np.array(r_df[['pickup_lat', 'pickup_lng']])
    counter = 0
    for coordinates in pickup_coords:
        counter = check_point_inside_hexagon(counter,area,coordinates)
    return counter


df = pd.read_csv('../data/clear_data.scv')
week_day, weekend, month, year = [], [], [], []

for raw in df.iterrows():
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

new_df = pd.DataFrame({'week_day': week_day, 'weekend': weekend, 'month': month, 'year': year})
new_df.to_csv("../data/time_data.scv", index=False)
