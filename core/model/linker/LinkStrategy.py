from api import utils


class LinkStrategy:
    params = {}

    '''params is a dict with specific parameters for each subclass'''
    def __init__(self, params):
        self.params = params

    def link(self, file_a, file_b):
        pass

    @staticmethod
    def calculate_distances(file_a, file_b):
        file_a_df = utils.clean_df(file_a)
        file_b_df = utils.clean_df(file_b)

        lat_a = file_a.get_lat_col()
        lon_a = file_a.get_lon_col()

        lat_b = file_b.get_lat_col()
        lon_b = file_b.get_lon_col()

        file_a_df['pointA'] = [(x, y) for x, y in zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_b_df['pointB'] = [(x, y) for x, y in zip(file_b_df[lat_b], file_b_df[lon_b])]

        file_a_df['distances'] = [utils.haversine_np(x, y, list(file_b_df[lat_b]), list(file_b_df[lon_b])) for x, y in
                                  zip(file_a_df[lat_a], file_a_df[lon_a])]
        file_a_df['closest_point'] = [file_b_df.iloc[x.argmin()]['pointB'] for x in file_a_df['distances']]
        file_a_df['closest_dist'] = [min(x) for x in file_a_df['distances']]
        return [file_a_df, file_b_df]
