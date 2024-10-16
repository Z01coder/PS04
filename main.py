from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time


def get_wikipedia_page(driver, query):
    # Переход на главную страницу Википедии
    driver.get("https://www.wikipedia.org/")

    # Поиск поля для ввода и отправка запроса
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.send_keys(query)
    search_box.submit()


def list_paragraphs(driver):
    # Получаем все параграфы статьи
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")

    for i, para in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{para.text}")
        # Ожидание перед выводом следующего параграфа
        next_step = input("\nНажмите Enter, чтобы продолжить листать, или введите 'stop', чтобы вернуться в меню: ")
        if next_step.lower() == 'stop':
            break


def show_related_links(driver):
    # Получаем все ссылки на связанные страницы
    related_links = driver.find_elements(By.CSS_SELECTOR, "a")
    links_dict = {}

    for i, link in enumerate(related_links):
        href = link.get_attribute('href')
        title = link.text
        if href and "wiki" in href and title:
            links_dict[i] = {'title': title, 'href': href}
            print(f"{i + 1}. {title}")

    return links_dict


def main():
    # Инициализация драйвера
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

    try:
        query = input("Введите запрос для поиска в Википедии: ")
        get_wikipedia_page(driver, query)
        time.sleep(2)  # Задержка для загрузки страницы

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей страницы")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")
            choice = input("Ваш выбор: ")

            if choice == '1':
                list_paragraphs(driver)
            elif choice == '2':
                related_links = show_related_links(driver)
                link_choice = input("Введите номер страницы, чтобы перейти, или 'back' для возврата: ")
                if link_choice.lower() == 'back':
                    continue
                elif link_choice.isdigit() and int(link_choice) - 1 in related_links:
                    chosen_link = related_links[int(link_choice) - 1]['href']
                    driver.get(chosen_link)
                    time.sleep(2)  # Задержка для загрузки новой страницы
                else:
                    print("Неверный выбор. Попробуйте снова.")
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
