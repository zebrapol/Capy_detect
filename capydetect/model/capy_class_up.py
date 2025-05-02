import os
import pickle
import csv
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def load_data_from_csv(capy_csv, empty_csv):
    """
    Загружает данные из двух CSV файлов (с капибарами и без)
    :param capy_csv: путь к CSV с капибарами
    :param empty_csv: путь к CSV без капибар
    :return: данные и метки
    """
    data = []
    labels = []

    with open(capy_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append([float(x) for x in row])
            labels.append(1)


    with open(empty_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append([float(x) for x in row])
            labels.append(0)

    return np.asarray(data), np.asarray(labels)


# Основной код
if __name__ == "__main__":
    capy_csv = 'capy.csv'
    empty_csv = 'empty_capy.csv'

    data, labels = load_data_from_csv(capy_csv, empty_csv)


    x_train, x_test, y_train, y_test = train_test_split(
        data, labels, test_size=0.2, shuffle=True, stratify=labels
    )


    classifier = SVC()
    parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]
    grid_search = GridSearchCV(classifier, parameters)
    grid_search.fit(x_train, y_train)

    best_estimator = grid_search.best_estimator_
    y_prediction = best_estimator.predict(x_test)
    score = accuracy_score(y_prediction, y_test)

    print(f'{score * 100}% правильно отработано')

    # Сохранение модели
    pickle.dump(best_estimator, open('../../model.tflite', 'wb'))