from pandas import DataFrame

from core.model.clusterizer.Categorizer import Categorizer


class ClusterStrategy:

    """params is a dict with specific parameters for each subclass"""
    def __init__(self, params):
        self.params = params

    def clusterize(self, ds, col_x, col_y):
        dataset = ds.get_data()
        df = DataFrame()
        dataset.dropna(subset=[col_x], inplace=True)
        dataset.dropna(subset=[col_y], inplace=True)
        df['c1'] = Categorizer.categorize_column(dataset, col_x)
        df['c2'] = Categorizer.categorize_column(dataset, col_y)
        X = df[['c1', 'c2']].values
        dataset[col_x + '_cat'] = df['c1']
        dataset[col_y + '_cat'] = df['c2']
        return self.spec_clusterize(dataset, X, col_x, col_y)
