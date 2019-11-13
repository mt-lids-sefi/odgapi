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
        [file_a_df, file_b_df] = LinkStrategy.calculate_distances(file_a, file_b)
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
        [file_a_df, file_b_df] = LinkStrategy.calculate_distances(file_a, file_b)
        file_a_df['closest_point_index'] = [x.argmin() for x in file_a_df['distances']]
        joined = file_a_df.join(file_b_df, on='closest_point_index', rsuffix='_b')
        joined = joined.drop(columns=['distances', 'closest_point_index'])
        if filter:
            filtered = joined.query('closest_dist < ' + str(params['distance']))
            return filtered
        else:
            return joined
