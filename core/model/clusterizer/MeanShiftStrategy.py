from sklearn.cluster import MeanShift
from core.model.clusterizer.ClusterStrategy import ClusterStrategy


class MeanShiftStrategy(ClusterStrategy):

    def __init__(self, params={}):
        super().__init__(params)

    def spec_clusterize(self, dataset, X, col_x, col_y):
        clustering = MeanShift().fit(X)
        centroids = clustering.cluster_centers_
        labels = clustering.labels_
        dataset.insert(0,  'cluster', labels)
        #dataset['cluster'] = labels
        return [centroids, labels, dataset]

    def get_details(self):
        return {'strategy': 'Mean Shift'}