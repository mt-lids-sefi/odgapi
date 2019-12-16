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

    #file_a y file_b son gds
    def link(self, file_a, file_b):
        [file_a_df, file_b_df] = LinkStrategy.calculate_distances(file_a, file_b)
        file_a_df['nearby_points'] = [utils.nearby_points(x, self.distance) for x in file_a_df['distances']]
        file_a_df['count'] = [len(x) for x in file_a_df['nearby_points']]
        unrolled = utils.unroll(file_a_df)
        if unrolled.size == 0:
            return unrolled
        joined = utils.join_dfs(unrolled, file_a_df, file_b_df)
        filtered = joined.query('closest_dist < ' + str(self.distance))
        filtered = filtered.drop(columns=['distances'])
        return filtered
