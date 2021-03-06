import numpy as np
import pandas as pd

"""calcula la distancia entre dos puntos en la tierra"""


def haversine_np(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def nearby_points(points, dist):
    pos = []
    for idx, val in enumerate(points):
        if (val < dist):
            pos.append(idx)
    return pos


def unroll(df1):
    adf = pd.DataFrame()
    for index, row in df1.iterrows():
        for nearp in row['nearby_points']:
            adf = adf.append({'id1': index, 'id2': nearp}, ignore_index=True)
    return adf


def join_dfs(ids, df1, df2):
    return ids.join(df1, on='id1', rsuffix='_1').join(df2, on='id2', rsuffix='_2')


# ids es un geodatasource, tnego el nombre
def clean_df(ids):
    df = ids.get_data()
    lat_a = ids.get_lat_col()
    lon_a = ids.get_lon_col()

    df = df[np.isfinite(df[lat_a])]
    df = df[np.isfinite(df[lon_a])]
    return df

