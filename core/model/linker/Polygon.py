from core.model.linker.LinkStrategy import LinkStrategy
import numpy as np
from api import utils


class Polygon(LinkStrategy):
    distance = 3

    def __init__(self, params):
        super().__init__(params)
        self.set_distance(self.params['distance'])

    def set_distance(self, distance):
        self.distance = distance

    def link(self, file_a, file_b):
        file_a_df = file_a.get_data()
        file_b_df = file_b.get_data()

        lat_a = file_a.lat_col
        lon_a = file_a.lon_col

        lat_b = file_b.lat_col
        lon_b = file_b.lon_col

        file_a_df = file_a_df[np.isfinite(file_a_df[lat_a])]
        file_a_df = file_a_df[np.isfinite(file_a_df[lon_a])]

        file_b_df = file_b_df[np.isfinite(file_b_df[lat_b])]
        file_b_df = file_b_df[np.isfinite(file_b_df[lon_b])]
        file_a_df['pointA'] = [(x, y) for x, y in zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_b_df['pointB'] = [(x, y) for x, y in zip(file_b_df[lat_b], file_b_df[lon_b])]

        file_a_df['distances'] = [utils.haversine_np(x, y, list(file_b_df[lat_b]), list(file_b_df[lon_b])) for
                                 x, y in
                                 zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_a_df['closest_point'] = [file_b_df.iloc[x.argmin()]['pointB'] for x in file_a_df['distances']]
        file_a_df['closest_dist'] = [min(x) for x in file_a_df['distances']]
        file_a_df['nearby_points'] = [utils.nearby_points(x, self.distance) for x in file_a_df['distances']]
        file_a_df['count'] = [len(x) for x in file_a_df['nearby_points']]
        unrolled = utils.unroll(file_a_df)
        joined = utils.join_dfs(unrolled, file_a_df, file_b_df)
        filtered = joined.query('closest_dist < ' + str(self.distance))
        filtered = filtered.drop(columns=['distances'])
        return filtered

    @staticmethod
    def link_preview(file_a, file_b, params):
        distance = params['distance']
        file_a_df = file_a.get_data()
        file_b_df = file_b.get_data()

        lat_a = file_a.lat_col
        lon_a = file_a.lon_col

        lat_b = file_b.lat_col
        lon_b = file_b.lon_col

        file_a_df = file_a_df[np.isfinite(file_a_df[lat_a])]
        file_a_df = file_a_df[np.isfinite(file_a_df[lon_a])]

        file_b_df = file_b_df[np.isfinite(file_b_df[lat_b])]
        file_b_df = file_b_df[np.isfinite(file_b_df[lon_b])]
        file_a_df['pointA'] = [(x, y) for x, y in zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_b_df['pointB'] = [(x, y) for x, y in zip(file_b_df[lat_b], file_b_df[lon_b])]

        file_a_df['distances'] = [utils.haversine_np(x, y, list(file_b_df[lat_b]), list(file_b_df[lon_b])) for
                                 x, y in
                                 zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_a_df['closest_point'] = [file_b_df.iloc[x.argmin()]['pointB'] for x in file_a_df['distances']]
        file_a_df['closest_dist'] = [min(x) for x in file_a_df['distances']]
        file_a_df['nearby_points'] = [utils.nearby_points(x, distance) for x in file_a_df['distances']]
        file_a_df['count'] = [len(x) for x in file_a_df['nearby_points']]
        unrolled = utils.unroll(file_a_df)
        joined = utils.join_dfs(unrolled, file_a_df, file_b_df)
        filtered = joined.query('closest_dist < ' + str(distance))
        filtered = filtered.drop(columns=['distances'])
        return filtered
