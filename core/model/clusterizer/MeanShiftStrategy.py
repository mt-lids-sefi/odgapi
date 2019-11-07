from core.model.clusterizer.ClusterStrategy import ClusterStrategy
from pandas import DataFrame
from sklearn.cluster import MeanShift


class MeanShiftStrategy(ClusterStrategy):

    def clusterize(self, ds, col_a, col_b):
        dataset = ds.get_data()
        df = DataFrame()
        df['c1'] = dataset[col_a]
        df['c2'] = dataset[col_b]
        X = df[['c1', 'c2']].values
        clustering = MeanShift().fit(X)
        print(clustering.labels_)
        print(clustering.cluster_centers_)
        pass
