import os
from PIL import Image


def convert_jpg_to_rgba(input_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg','.png')):
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, rel_path)
                os.makedirs(output_subdir, exist_ok=True)

                output_path = os.path.join(output_subdir, os.path.splitext(file)[0] + '.png')

                try:
                    with Image.open(input_path) as img:
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        img.save(output_path, 'PNG')
                    print(f"Конвертировано: {input_path} -> {output_path}")
                except Exception as e:
                    print(f"Ошибка при конвертации {input_path}: {e}")


if __name__ == "__main__":
    input_directory = input("Введите путь к исходной директории: ").strip()
    output_directory = input("Введите путь к выходной директории: ").strip()

    convert_jpg_to_rgba(input_directory, output_directory)