import numpy as np
import pandas as pd

def haversine_np(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

def nearby_points(points, dist):
    pos= []
    for idx, val in enumerate(points):
        if(val < dist):
            pos.append(idx)
    return pos

def unroll(df1):
    adf = pd.DataFrame()
    for index, row in df1.iterrows():
        for nearp in row['nearby_points']:
            adf = adf.append({'id1': index, 'id2': nearp}, ignore_index=True)
    return adf

def join_dfs(ids, df1, df2):
    return ids.join(df1, on='id1').join(df2, on='id2')