from core.model.linker import LinkStrategy


class Poligon(LinkStrategy):

    def setDistance(self, distance):
        self.distance=distance

    def link(self, fileA, fileB):
        pass