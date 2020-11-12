from pandas import DataFrame
from sklearn import preprocessing
import json

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

    @staticmethod
    def uncategorize_value(dataset, column, value):
        value = round(value, 0)
        i_value = int(value)
        uncat_val = dataset.query(column+'_cat == ' + str(i_value)).iloc[0][column]
        return uncat_val

    @staticmethod
    def uncategorize_centroid(centroid, dataset, col_x, col_y):
        if (dataset.dtypes[col_x] == 'object'):
            vx = centroid[0]
        else: vx = Categorizer.uncategorize_value(dataset, col_x, centroid[0])
        if (dataset.dtypes[col_y] == 'object'):
            vy = Categorizer.uncategorize_value(dataset, col_y, centroid[1])
        else: vy = centroid[1]
        return [vx, vy]

    @staticmethod
    def uncategorize_centroids(centroids, dataset, col_x, col_y):
        uncat_centroids = []
        for c in centroids:
            uncat_centroid = Categorizer.uncategorize_centroid(c, dataset, col_x, col_y)
            uncat_centroids.append(uncat_centroid)
        return uncat_centroids

    @staticmethod
    def get_cats_n_labels(dataset, col):
        le = preprocessing.LabelEncoder()
        le.fit(dataset[col])
        cl = le.classes_
        trans = le.transform(cl)
        dfc = DataFrame({
            "original": cl,
            "categorized": trans
        })
        data = dfc.to_json(orient='index')
        data = json.loads(data)
        return data
