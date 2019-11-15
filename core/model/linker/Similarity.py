from core.model.linker.LinkStrategy import LinkStrategy


class Similarity(LinkStrategy):
    rules = []

    def __init__(self, params):
        super().__init__(params)
        self.set_rules(self.params['rules'])

    def link(self, file_a, file_b):
        pass

    def set_rules(self, rules):
        self.rules = rules
