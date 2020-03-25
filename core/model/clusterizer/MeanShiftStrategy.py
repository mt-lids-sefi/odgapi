from sklearn.cluster import MeanShift

from core.model.clusterizer.Categorizer import Categorizer
from core.model.clusterizer.ClusterStrategy import ClusterStrategy


class MeanShiftStrategy(ClusterStrategy):

    def __init__(self, params={}):
        super().__init__(params)

    def spec_clusterize(self, dataset, X, col_x, col_y):
        clustering = MeanShift().fit(X)
        centroids = clustering.cluster_centers_
        labels = clustering.labels_
        dataset['cluster'] = labels
        uncat_centroids = Categorizer.uncategorize_centroids(centroids, dataset, col_x, col_y)
        return [uncat_centroids, labels, dataset]
