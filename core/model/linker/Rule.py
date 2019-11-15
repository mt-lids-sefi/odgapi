
class Rule:

    column_a = ''
    column_b = ''
    matches = []

    def set_column_a(self, col):
        self.column_a = col

    def set_column_b(self, col):
        self.column_b = col

    def add_match(self, match):
        self.matches.append(match)

    def set_matches(self, matches):
        self.matches = matches

