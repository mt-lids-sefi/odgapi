from sklearn.cluster import KMeans

from core.model.clusterizer.ClusterStrategy import ClusterStrategy


class KMeansStrategy(ClusterStrategy):

    def __init__(self, params):
        super().__init__(params)
        if params['k']:
            self.set_k(self.params['k'])
        else:
            self.set_k(3)

    def spec_clusterize(self, dataset, X):
        kmeans = KMeans(n_clusters=self.k).fit(X)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        dataset['cluster'] = labels
        return [centroids, labels, dataset]

    def set_k(self, k):
        self.k = k
