from sklearn import preprocessing

class Categorizer:

    def __init__(self):
        pass

    @staticmethod
    def categorize_dataset(dataset, column):
        le = preprocessing.LabelEncoder()
        cat_col = le.fit_transform(dataset[column])
        dataset[column+'_categorized'] = cat_col
        return dataset

    @staticmethod
    def categorize_column(dataset, column):
        le = preprocessing.LabelEncoder()
        cat_col = le.fit_transform(dataset[column])
        return cat_col
