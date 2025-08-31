import allure
from playwright.sync_api import Page, Cookie


class Browser:
    """Методы браузера, взаимодействие с вкладками и ifram'ами"""

    def __init__(self, page: Page):
        self.page = page

    def go_to_url(self, url: str):
        """Переход по указанному URL

        :param url: адрес страницы
        """

        with allure.step(f'Переход на страницу: {url}'):
            return self.page.goto(url)

    def reload_page(self):
        """Перезагрузка страницы"""

        with allure.step('Обновление страницы'):
            return self.page.reload()

    def get_current_url(self) -> str:
        """Получение URL текущей страницы."""

        with allure.step('Получение URL страницы'):
            return self.page.url

    def get_cookies(self) -> list[Cookie]:
        """Получение cookies страницы"""

        with allure.step('Получение cookies страницы'):
            return self.page.context.cookies()

    def add_cookies(self, cookies: Cookie):
        """Добавление cookies в хранилище браузера

        :param cookies: список кук
        """

        with allure.step('Добавление cookies'):
            return self.page.context.add_cookies(list(cookies))

    def close_tab(self, tab_number: int):
        """Закрытие вкладки с указанным порядковым номером

        :param tab_number: номер вкладки, которую нужно закрыть (начиная с 0)
        """

        with allure.step(f'Закрытие вкладки под номером {tab_number}'):
            all_tabs = self.page.context.pages
            all_tabs[tab_number].close()

    def switch_to_tab(self, tab_number: int) -> Page | None:
        """Переключение на вкладку с указанным номером
        и закрытие других вкладок

        :param tab_number: номер вкладки, на которую нужно переключиться
        (начиная с 0)
        """

        with allure.step(
            f'Переключение на вкладку {tab_number} и закрытие других вкладок'
        ):
            all_tabs = self.page.context.pages
            tab_to_switch = all_tabs[tab_number]
            tab_to_switch.bring_to_front()
            tab_to_switch.wait_for_load_state()
            return tab_to_switch

    def close_all_tabs_except_first(self):
        """Закрытие всех страниц, кроме первой"""

        with allure.step('Закрытие всех страниц, кроме первой'):
            all_tabs = self.page.context.pages
            for page in range(1, len(all_tabs)):
                all_tabs[page].close()

    def switch_to_iframe_and_click_element_inside_it(
        self, iframe_locator: str, element_to_click_locator: str
    ):
        """Переход на iframe и клик по элементу внутри него

        :param iframe_locator: локатор iframe
        :param element_to_click_locator: локатор элемента внутри iframe,
                                         на который нужно кликнут
        """

        with allure.step('Переход на iframe и клик по элементу внутри него'):
            iframe = self.page.frame_locator(iframe_locator)
            iframe.locator(element_to_click_locator).click()

    def switch_to_iframe_and_fill_the_field(
        self, iframe_locator: str, field_locator: str, text: str
    ):
        """Переход на iframe и ввод текста в поле внутри iframe

        :param iframe_locator: локатор iframe
        :param field_locator: локатор поля внутри iframe,
                              куда нужно ввести текст
        :param text: текст для ввода
        """

        with allure.step(f'Переход на iframe и ввод текста "{text}"'):
            iframe = self.page.frame_locator(iframe_locator)
            iframe.locator(field_locator).fill(text)

    def get_iframe_by_index(self, iframe_index: int):
        """Получение дочернего iframe по его индексу.

        :param iframe_index: индекс iframe
        """

        with allure.step(f'Получение iframe с индексом {iframe_index}'):
            return self.page.main_frame.child_frames[iframe_index]

    def switch_to_main_iframe(self):
        """Переключение на основной iframe"""

        with allure.step('Переключение на основной iframe'):
            return self.page.main_frame

    def alert_accept(self):
        """Принятие диалогового окна (нажатие OK)"""

        with allure.step('Принятие диалогового окна (нажатие OK)'):
            self.page.on('dialog', lambda dialog: dialog.accept())

    def scroll_down(self):
        """Скролл вниз страницы"""

        with allure.step('Прокрутка вниз страницы'):
            self.page.evaluate(
                'window.scrollTo(0, document.body.scrollHeight)'
            )

    def take_screenshot(self, path_to_save: str):
        """Создание screenshot'а страницы

        :param path_to_save: путь для сохранения файла
                            (например: screenshots/image1.png)
        """

        with allure.step('Сохранение скриншота страницы'):
            return self.page.screenshot(path=path_to_save)

    def execute_javascript(self, script: str):
        """Выполнение javascript на странице

        :param script: код js-скрипта
        """

        with allure.step('Выполнение действий с помощью кода на javascript'):
            return self.page.evaluate(script)

    def assert_file_is_downloaded(self):
        """Проверка загрузки файла"""

        with self.page.expect_download() as download_info:
            downloaded_file = download_info.value

            with allure.step('Проверка загрузки файла'):
                assert (
                    downloaded_file.path() != ''
                ), 'Downloaded file not found.'

    def press_keys(self, keys: str):
        """Эмуляция нажатия клавиш(и) на клавиатуре

        :param keys: строка с клавишей или сочетанием клавиш
        """

        with allure.step(f'Нажатие клавиш(и) {keys}'):
            self.page.keyboard.press(keys)
