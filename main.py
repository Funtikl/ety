import requests
from bs4 import BeautifulSoup
import sys
import time
import itertools

# Функция загрузочного спиннера
def loading_spinner(duration):
    spinner = itertools.cycle(['-', '\\', '|', '/'])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f"\r{next(spinner)} Loading...")
        sys.stdout.flush()
        time.sleep(0.1)
    print()  # Печатает новую строку в конце

# Функция эффекта печатной машинки
def typewriter_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Печатает новую строку в конце

# Функция прогресс-бара
def progress_bar(duration, total=30):
    for i in range(total + 1):
        percent = int((i / total) * 100)
        bar = '#' * i + '-' * (total - i)
        sys.stdout.write(f'\r[{bar}] {percent}%')
        sys.stdout.flush()
        time.sleep(duration / total)
    print()  # Печатает новую строку в конце

def fetch_page(url):
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()

            response.encoding = response.apparent_encoding

            return response.text

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print("Error 404: Səhifə tapılmadı. Yeni söz yazın: ")
                word = input('Araşdırmaq istədiyiniz sözü türkcə daxil edin: ').strip().lower()  # Преобразуем ввод в нижний регистр
                url = 'https://www.etimolojiturkce.com/kelime/' + word
            else:
                print(f"HTTP error occurred: {http_err}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Разделитель
    print('-' * 40)

    # Получаем заголовок страницы безопасно
    title = soup.title.string if soup.title else "No title found"
    typewriter_effect(f"Araşdırma səhifəsi: {title}")

    # Добавление спиннера для визуализации ожидания поиска информации
    loading_spinner(2)

    # Получаем первый <p> тег безопасно
    first_paragraph = soup.find('p')
    if first_paragraph:
        word = first_paragraph.get_text()
        typewriter_effect(f"\nQısa məlumat:\n    {word}")
    else:
        print("\nNo <p> tag found on the page.")

    # Извлекаем текст от 'Kelime Kökeni' до следующего <p> тега
    kelime_kokeni_section = soup.find(string='Kelime Kökeni')
    if kelime_kokeni_section:
        parent_div = kelime_kokeni_section.find_parent()
        next_p_tag = parent_div.find_next('p') if parent_div else None
        if next_p_tag:
            content = next_p_tag.get_text()
            typewriter_effect(f"\nDaha geniş məlumat:\n    {content.strip()}")
        else:
            print("\nNo <p> tag found after 'Kelime Kökeni'.")
    else:
        print("\nNo 'Kelime Kökeni' section found.")

    # Заключительный разделитель
    print('-' * 40)

if __name__ == "__main__":
    url = 'https://www.etimolojiturkce.com'

    while True:
        word = input("Araşdırmaq istədiyiniz sözü türkcə daxil edin: ").strip().lower()  # Преобразуем ввод в нижний регистр
        
        # Печать с эффектом печатной машинки
        typewriter_effect("Məlumatlar toplanılır, zəhmət olmasa gözləyin...\n", delay=0.05)
        
        # Добавляем прогресс-бар, чтобы визуализировать процесс запроса
        progress_bar_duration = 3  # Длительность 3 секунды
        progress_bar(progress_bar_duration)

        html_content = fetch_page(url + '/kelime/' + word)
        if html_content:
            extract_info(html_content)
        
        # Спрашиваем пользователя, хочет ли он искать ещё одно слово
        repeat = input("Başqa söz araşdırmaq istəyirsiniz? (yes/no): ").strip().lower()
        if repeat not in ['yes', 'y']:
            print("Sağ olun!")
            break
