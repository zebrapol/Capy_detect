import os

import csv

from skimage.io import imread
from skimage.transform import resize



def images_to_csv(folder_path, output_csv):
    """
    Преобразует все изображения в папке в CSV файл
    :param folder_path: путь к папке с изображениями
    :param output_csv: имя выходного CSV файла
    """
    data = []

    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, file)
            try:
                img = imread(img_path)
                img = resize(img, (15, 15, 3))
                flattened = img.flatten()
                data.append(flattened)
            except Exception as e:
                print(f"Ошибка при обработке {img_path}: {e}")

    if not data:
        print("Не найдено изображений для обработки")
        return

    # Сохраняем в CSV
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    print(f"Данные сохранены в {output_csv}, всего {len(data)} изображений")

images_to_csv('C:/Users/Andre/Desktop/capy_rgb_2', 'capy_2.csv')