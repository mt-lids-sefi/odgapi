from api import utils
from core.model.linker.LinkStrategy import LinkStrategy


class Similarity(LinkStrategy):
    rules = []

    def __init__(self, params):
        super().__init__(params)
        self.set_rules(self.params['rules'])

    def link(self, file_a, file_b):
        df_a = utils.clean_df(file_a)
        df_b = utils.clean_df(file_b)
        columns_left = []
        columns_right = []
        i = 0
        for rule in self.rules:
            print(rule.to_string())
            c_a = rule.get_column_a()
            c_b = rule.get_column_b()
            df_a[c_a + '_m' + str(i)] = df_a[c_a]
            columns_left.append(c_a + '_m' + str(i))
            columns_right.append(c_b)
            for m in rule.get_matches():
                df_a = df_a.replace({c_a + '_m' + str(i): m}) # reemplaza valores en df_a para que sean iguales a como son en df_b. el merge es automático después
            i += 1
            print(columns_left, columns_right)
        merged = df_a.merge(df_b, left_on=columns_left, right_on=columns_right, suffixes=('_left', '_right'))
        return merged

    def set_rules(self, rules):
        self.rules = rules

    def get_details(self):
        return {'RULES_DETAILS': "TBD"}