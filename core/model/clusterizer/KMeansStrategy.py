from core.model.clusterizer import ClusterStrategy

class KMeansStrategy(ClusterStrategy):

    def __init__(self):
        self.distance= 3

    def clusterize(self, lFile, colA, colB):
        pass

    def setDistance(self, distance):
        self.distance = distance