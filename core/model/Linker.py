class Linker:

    def __init__(self, strategy):
        self.strategy = strategy


    def linkFiles(self, fileA, fileB):
        return self.strategy.linkFiles(fileA, fileB)

    def setStrategy(self, strategy):
        self.strategy=strategy