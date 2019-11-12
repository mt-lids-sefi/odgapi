from core.model.linker.LinkStrategy import LinkStrategy
import numpy as np
from api import utils


class ClosestPoint(LinkStrategy):
    distance = 3
    filter = True

    def __init__(self, params):
        super().__init__(params)
        self.set_distance(self.params['distance'])
        self.set_filter(self.params['filter'])

    def set_filter(self, filter):
        self.filter = filter

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

        file_a_df['distances'] = [utils.haversine_np(x, y, list(file_b_df[lat_b]), list(file_b_df[lon_b])) for x, y in
                                 zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_a_df['closest_point'] = [file_b_df.iloc[x.argmin()]['pointB'] for x in file_a_df['distances']]
        file_a_df['closest_dist'] = [min(x) for x in file_a_df['distances']]
        file_a_df['closest_point_index'] = [x.argmin() for x in file_a_df['distances']]
        joined = file_a_df.join(file_b_df, on='closest_point_index', rsuffix='_b')
        joined = joined.drop(columns=['distances', 'closest_point_index'])
        if self.filter:
            filtered = joined.query('closest_dist < '+str(self.distance))
            return filtered
        else:
            return joined

    @staticmethod
    def link_preview(file_a, file_b, params):
        filter = params['filter']
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

        file_a_df['distances'] = [utils.haversine_np(x, y, list(file_b_df[lat_b]), list(file_b_df[lon_b])) for x, y in
                                  zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_a_df['closest_point'] = [file_b_df.iloc[x.argmin()]['pointB'] for x in file_a_df['distances']]
        file_a_df['closest_dist'] = [min(x) for x in file_a_df['distances']]
        file_a_df['closest_point_index'] = [x.argmin() for x in file_a_df['distances']]
        joined = file_a_df.join(file_b_df, on='closest_point_index', rsuffix='_b')
        joined = joined.drop(columns=['distances', 'closest_point_index'])
        if filter:
            filtered = joined.query('closest_dist < ' + str(params['distance']))
            return filtered
        else:
            return joined
