
class Rule:

    column_a = ''
    column_b = ''
    matches = []

    def __init__(self, col_a, col_b, matches):
        self.set_column_a(col_a)
        self.set_column_b(col_b)
        self.set_matches(matches)

    def set_column_a(self, col):
        self.column_a = col

    def set_column_b(self, col):
        self.column_b = col

    def add_match(self, match):
        self.matches.append(match)

    def set_matches(self, matches):
        self.matches = matches

    def get_column_a(self):
        return self.column_a

    def get_column_b(self):
        return self.column_b

    def get_matches(self):
        return self.matches

    def to_string(self):
        return "RULE: column a: "+self.column_a+", column b: "+self.column_b+", matches: "+str(self.matches)

    def has_columns(self, col_a, col_b):
        return self.column_a == col_a & self.column_b == col_b
