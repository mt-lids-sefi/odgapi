from pandas import DataFrame

from core.model.clusterizer.Categorizer import Categorizer


class ClusterStrategy:

    """params is a dict with specific parameters for each subclass"""
    def __init__(self, params):
        self.params = params

    def clusterize(self, ds, col_a, col_b):
        dataset = ds.get_data()
        df = DataFrame()
        df['c1'] = Categorizer.categorize_column(dataset, col_a)
        df['c2'] = Categorizer.categorize_column(dataset, col_b)
        X = df[['c1', 'c2']].values
        dataset[col_a + '_cat'] = df['c1']
        dataset[col_b + '_cat'] = df['c2']
        return self.spec_clusterize(dataset, X)
