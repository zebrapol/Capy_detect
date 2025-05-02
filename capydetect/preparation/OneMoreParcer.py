import time
import urllib.request
from io import BytesIO
from PIL import Image
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

options = Options()
options.add_argument("--window-size=1920,1080")


save_folder = "C:/Users/Andre/Desktop/Capy"
os.makedirs(save_folder, exist_ok=True)

driver = webdriver.Chrome(
    service=ChromeService(),
    options=options
)

driver.get("https://www.inaturalist.org/taxa/71855-Hydrochoerus/browse_photos")
time.sleep(5)


def load_more_images():
    """Функция для прокрутки страницы и загрузки дополнительных изображений"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    max_attempts = 30

    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, "a.load-more")
            driver.execute_script("arguments[0].click();", load_more_button)
            print("Нажимаем кнопку Load More...")
            time.sleep(5)
            attempts = 0
        except NoSuchElementException:
            attempts += 1
            print(f"Прокрутка страницы ({attempts}/{max_attempts})...")

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Завершена прокрутка и загрузка изображений")


load_more_images()


def extract_image_urls():
    image_urls = set()
    elements = driver.find_elements(By.CSS_SELECTOR, "div.CoverImage")

    for element in elements:
        try:
            style = element.get_attribute("style")
            if style:
                match = re.search(r'url\("?(https://[^)]+\.jpeg)"?\)', style)
                if match:
                    url = match.group(1)
                    if "/medium.jpg" in url:
                        url = url.replace("/medium.jpg", "/original.jpg")
                    elif "/small.jpg" in url:
                        url = url.replace("/small.jpg", "/original.jpg")
                    image_urls.add(url)
        except StaleElementReferenceException:
            continue

    return list(image_urls)


image_urls = extract_image_urls()

if not image_urls:
    print("Не удалось найти изображения. Попробуйте другие селекторы:")
    print("Попытка альтернативного метода...")
    img_elements = driver.find_elements(By.CSS_SELECTOR, "img.photo_image")
    image_urls = [img.get_attribute("src") for img in img_elements if img.get_attribute("src")]

print(f"\nНайдено уникальных изображений капибар: {len(image_urls)}\n")

downloaded_count = 0
max_downloads = 1000

for i, url in enumerate(image_urls[:max_downloads]):
    try:
        if not url:
            continue

        print(f"Скачивание изображения {i + 1}/{len(image_urls)}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req) as response:
            image_data = response.read()

        image = Image.open(BytesIO(image_data))
        width, height = image.size

        if width < 300:
            print(f"Пропущено (маленькое разрешение: {width}x{height})")
            continue

        file_name = os.path.join(save_folder, f"{i + 1}.png")
        with open(file_name, 'wb') as f:
            f.write(image_data)

        downloaded_count += 1
        print(f" Сохранено: {file_name} ({width}x{height})")

    except Exception as e:
        print(f"Ошибка при скачивании {url}: {str(e)}")

print(f"\nСкачивание завершено! Успешно сохранено изображений: {downloaded_count}")
driver.quit()