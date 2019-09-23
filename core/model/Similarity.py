from core.model.LinkStrategy import LinkStrategy


class Similarity(LinkStrategy):


    def link(self, fileA, fileB):
        pass

    def setSimilColumns(self, colFileA, colFileB):
        self.colFileA = colFileA
        self.colFileB = colFileB

