class Clusterizer:

    def __init__(self, strategy):
        self.strategy = strategy

    def clusterize(self, linkedFile, colA, colB):
        return self.strategy.clusterize(linkedFile, colA, colB)

    def setStrategy(self, strategy):
        self.strategy=strategy