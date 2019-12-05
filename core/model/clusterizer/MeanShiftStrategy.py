from core.model.clusterizer.Categorizer import Categorizer
from core.model.clusterizer.ClusterStrategy import ClusterStrategy
from pandas import DataFrame
from sklearn.cluster import MeanShift


class MeanShiftStrategy(ClusterStrategy):

    def __init__(self, params={}):
        super().__init__(params)

    def clusterize(self, ds, col_a, col_b):
        dataset = ds.get_data()
        df = DataFrame()
        df['c1'] = Categorizer.categorize_column(dataset, col_a)
        df['c2'] = Categorizer.categorize_column(dataset, col_b)
        X = df[['c1', 'c2']].values
        dataset[col_a+'_cat'] = df['c1']
        dataset[col_b+'_cat'] = df['c2']
        clustering = MeanShift().fit(X)
        centroids = clustering.cluster_centers_
        labels = clustering.labels_
        dataset['cluster'] = labels
        return [centroids, labels, dataset]
