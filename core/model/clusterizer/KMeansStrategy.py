from pandas import DataFrame
from sklearn.cluster import KMeans

from core.model.clusterizer import Categorizer
from core.model.clusterizer.Categorizer import Categorizer
from core.model.clusterizer.ClusterStrategy import ClusterStrategy


class KMeansStrategy(ClusterStrategy):

    def __init__(self, params):
        super().__init__(params)
        if params['k']:
            self.set_k(self.params['k'])
        else:
            self.set_k(3)

# las columnas que se reciben ya están caterogizadas
    def clusterize(self, ds, col_a, col_b):
        dataset = ds.get_data()
        df = DataFrame()
        df['c1'] = Categorizer.categorize_column(dataset, col_a)
        df['c2'] = Categorizer.categorize_column(dataset, col_b)
        X = df[['c1', 'c2']].values
        kmeans = KMeans(n_clusters=self.k).fit(X)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        return [centroids, labels]

    def set_k(self, k):
        self.k = k
