from playwright.sync_api import Page

from src.ui.browser.browser import Browser
from src.ui.helper.urls import BASE_URL, CART_ENDPOINT
from src.ui.page_elements.button import Button
from src.ui.page_elements.element import Element


class BasePage:
    """Логика для тестов на главной странице"""

    def __init__(self, page: Page, url=BASE_URL):
        self.page = page
        self.url = url
        self.browser = Browser(page)
        self.monitors_button = Button(
            page, strategy='by_text', value='Monitors', allure_name='Monitors'
        )
        self.monitors = Element(
            page,
            strategy='locator',
            selector='.card-block',
            allure_name='Карточка товара',
        )
        self.cart_button = Button(
            page, strategy='locator', selector='#cartur', allure_name='Корзина'
        )

    def open(self):
        """Открытие страницы по URL"""
        return self.browser.go_to_url(url=self.url)

    def navigate_to_monitors_section(self):
        """Переход в раздел Мониторы"""

        self.monitors_button.click()
        self.page.wait_for_timeout(1500)

    def assert_number_of_cards(self, number_of_cards: int):
        """Проверка количества карточек с товаром
        param: number_of_cards - количество карточек с товаром"""

        all_monitor_cards = self.monitors.get_element()
        cards_count = all_monitor_cards.count()
        assert (
            cards_count == number_of_cards
        ), f'Number of cards should be {number_of_cards} but got {cards_count}'

    def navigate_to_cart(self):
        """Переход в корзину"""
        self.cart_button.click()
        page_url = self.page.url

        assert page_url.endswith(
            CART_ENDPOINT
        ), f'{page_url} should end with {CART_ENDPOINT}'
