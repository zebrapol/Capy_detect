import time
import urllib.request
from io import BytesIO
from PIL import Image
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
    NoSuchElementException

options = Options()

options.add_argument("--window-size=1920,1080")

save_folder = "C:/Users/Andre/Desktop/empty_capy"
os.makedirs(save_folder, exist_ok=True)

driver = webdriver.Chrome(
    service=ChromeService(),
    options=options
)

driver.get("https://unsplash.com/s/photos/%D0%91%D1%83%D1%84%D0%B0%D0%BB?license=free")
#driver.get("https://www.inaturalist.org/taxa/71855-Hydrochoerus/browse_photos")
time.sleep(3)
def load_more_images():
    """Функция для прокрутки страницы и нажатия кнопки 'Load more'"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    load_more_attempts = 0
    max_attempts = 10

    while load_more_attempts < max_attempts:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)


        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR,
                                                   ".WfcG4.WybTA.yoWgy.DimJM.ae8ZH.y9IO6.VyUnB.BCGzd.pYP1f")
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Нажимаем кнопку Load more...")
            time.sleep(3)
            load_more_attempts = 0
        except (NoSuchElementException, ElementClickInterceptedException):
            load_more_attempts += 1
            print(f"Прокрутка страницы ({load_more_attempts}/{max_attempts})...")


        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Завершена прокрутка и загрузка изображений")


# Выполняем прокрутку и загрузку
load_more_images()
# Кликаем кнопку "Load more", пока она есть
while True:
    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR,
                                               ".WfcG4.WybTA.yoWgy.DimJM.ae8ZH.y9IO6.VyUnB.BCGzd.pYP1f")
        print("Нажимаем кнопку Load more...")
        load_more_button.click()
        time.sleep(3)
    except (NoSuchElementException, ElementClickInterceptedException):
        print("Кнопка 'Load more' больше не найдена.")
        break

# Сбор всех подходящих изображений
image_html_nodes = driver.find_elements(By.CSS_SELECTOR, "img[src*='images.unsplash.com']")
image_urls = []

for image_html_node in image_html_nodes:
    try:
        srcset = image_html_node.get_attribute("srcset")
        image_url = image_html_node.get_attribute("src")


        if srcset:
            srcset_parts = srcset.split(", ")

            highest_res = srcset_parts[-1].split(" ")[0]
            image_url = highest_res if highest_res.startswith('http') else image_url


        if image_url and image_url.startswith('http'):
            image_urls.append(image_url)

    except StaleElementReferenceException:
        continue

# Убираем дубликаты
image_urls = list(set(image_urls))
print(f"\nНайдено уникальных изображений: {len(image_urls)}\n")

# Скачивание
image_name_counter = 1
downloaded_count = 0

for image_url in image_urls:
    try:
        print(f"Проверка изображения №{image_name_counter} ({image_url})...")

        with urllib.request.urlopen(image_url) as response:
            image_data = response.read()

        image = Image.open(BytesIO(image_data))
        width, height = image.size

        if width < 300:
            print(f"Пропущено (ширина: {width}px < 300px)")
            image_name_counter += 1
            continue

        file_name = f"{save_folder}/{image_name_counter}.jpg"
        with open(file_name, 'wb') as f:
            f.write(image_data)

        print(f"Скачано: {file_name} (ширина: {width}px)")
        downloaded_count += 1
        image_name_counter += 1

        if downloaded_count >= 500:
            print("\nСкачано 500 изображений. Готово!")
            break

    except Exception as e:
        print(f"Ошибка при обработке изображения {image_url}: {e}")
        image_name_counter += 1

print(f"\nИтого скачано изображений: {downloaded_count}")
driver.quit()