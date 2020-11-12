from pandas import DataFrame

from core.model.clusterizer.Categorizer import Categorizer


class ClusterStrategy:

    """params is a dict with specific parameters for each subclass"""
    def __init__(self, params):
        self.params = params
        self.cat_x = False
        self.cat_y = False

    def clusterize(self, ds, col_x, col_y):
        dataset = ds.get_data()
        df = DataFrame()
        dataset.dropna(subset=[col_x], inplace=True)
        dataset.dropna(subset=[col_y], inplace=True)
        if (dataset.dtypes[col_x] == 'object'):
            df['c1'] = Categorizer.categorize_column(dataset, col_x)
            self.cat_x = True
        else: df['c1'] = dataset[col_x]
        if (dataset.dtypes[col_y] == 'object'):
            df['c2'] = Categorizer.categorize_column(dataset, col_y)
            self.cat_y = True
        else: df['c2'] = dataset[col_y]
        X = df[['c1', 'c2']].values
        dataset[col_x + '_cat'] = df['c1']
        dataset[col_y + '_cat'] = df['c2']
        [centroids, labels, dataset] = self.spec_clusterize(dataset, X, col_x, col_y)
        cat_col_x = DataFrame()
        cat_col_y = DataFrame()
        if (self.cat_x):
            cat_col_x = Categorizer.get_cats_n_labels(dataset, col_x)
        if (self.cat_y):
            cat_col_y = Categorizer.get_cats_n_labels(dataset, col_y)
        return [centroids, labels, dataset, {"x" : cat_col_x, "y" : cat_col_y}]
        #return self.spec_clusterize(dataset, X, col_x, col_y)
        #uncat_centroids = Categorizer.uncategorize_centroids(centroids, dataset, col_x, col_y)
