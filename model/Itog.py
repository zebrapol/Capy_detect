import os
import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from PIL import Image


MODEL_PATH = '../model.tflite'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Модель не найдена! Убедитесь, что файл model.p находится в той же директории.")

with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)


def convert_to_rgba(image_path):
    """Конвертирует изображение в RGBA и сохраняет как временный файл"""
    temp_path = "temp_rgba.png"
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img.save(temp_path, 'PNG')
        return temp_path
    except Exception as e:
        print(f"Ошибка при конвертации {image_path}: {e}")
        return image_path


def preprocess_image(image_path):

    rgba_path = convert_to_rgba(image_path)


    img = imread(rgba_path)
    img = resize(img, (15, 15, 3))


    if rgba_path != image_path:
        try:
            os.remove(rgba_path)
        except:
            pass

    return img.flatten().reshape(1, -1)


def predict(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError("Файл изображения не найден!")


    image_data = preprocess_image(image_path)


    prediction = model.predict(image_data)[0]
    label = "Капибарка найдена" if prediction == 1 else "Нет капибары, сдохни нахуй"

    return label


if __name__ == '__main__':
    image_path = input("Введите путь к изображению: ")
    result = predict(image_path)
    print(result)