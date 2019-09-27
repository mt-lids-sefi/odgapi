from core.model.linker import LinkStrategy


class ClosestPoints(LinkStrategy):

    def setDistance(self, distance):
        self.distance=distance

    def link(self, fileA, fileB):
        pass