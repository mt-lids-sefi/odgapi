from core.model.linker import LinkStrategy
import numpy as np
from api import utils

class ClosestPoint(LinkStrategy):

    def setDistance(self, distance):
        self.distance=distance

    def link(self, fileA, fileB):
        fileA_df = fileA.get_data()
        fileB_df = fileB.get_data()

        latA = fileA.lat_col
        lonA = fileA.lon_col

        latB = fileB.lat_col


        lonB = fileB.lon_col
        fileA_df = fileA_df[np.isfinite(fileA_df[latA])]
        fileA_df = fileA_df[np.isfinite(fileA_df[lonA])]

        fileB_df = fileB_df[np.isfinite(fileB_df[latB])]
        fileB_df = fileB_df[np.isfinite(fileB_df[lonB])]

        fileA_df['pointA'] = [(x, y) for x, y in zip(fileA_df[latA], fileA_df[lonA])]
        fileB_df['pointB'] = [(x, y) for x, y in zip(fileB_df[latB], fileB_df[lonB])]

        fileA_df['distances'] = [utils.haversine_np(x, y, list(fileB_df[latB]), list(fileB_df[lonB])) for x, y in
                                 zip(fileA_df[latA], fileA_df[lonA])]
        fileA_df['closest_point'] = [fileB_df.iloc[x.argmin()]['pointB'] for x in fileA_df['distances']]
        fileA_df['closest_dist'] = [min(x) for x in fileA_df['distances']]
        fileA_df['closest_point_index'] = [x.argmin() for x in fileA_df['distances']]
        return fileA_df.join(fileB_df, on='closest_point_index')