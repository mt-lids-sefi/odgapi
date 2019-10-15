class LinkStrategy:
    params = {}

    '''params is a dict with specific parameters for each subclass'''
    def __init__(self, params):
        self.params = params

    def link(self, fileA, fileB):
        pass
