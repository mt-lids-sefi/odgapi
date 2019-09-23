from pandas.core.frame import DataFrame


class LinkedFile:
    linkedData = DataFrame()

    def __init__(self, fileA, fileB):
        self.fileA = fileA
        self.fileB = fileB
