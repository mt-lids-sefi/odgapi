
class ClusterStrategy:

    """params is a dict with specific parameters for each subclass"""
    def __init__(self, params):
        self.params = params

    def clusterize(self, ds, col_a, col_b):
        pass
