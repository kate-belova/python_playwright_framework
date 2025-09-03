from playwright.sync_api import Page
from src.ui.browser.browser import Browser
from src.ui.helper.urls import BASE_URL, CART_ENDPOINT, PRODUCT_CARD_ENDPOINT
from src.ui.page_elements.button import Button
from src.ui.page_elements.element import Element
from src.ui.page_elements.text import Text


class BasePage:
    """Логика для тестов на главной странице"""

    def __init__(self, page: Page, url=BASE_URL):
        self.page = page
        self.url = url
        self.browser = Browser(page)

        self.categories_header = Text(
            page,
            strategy='locator',
            selector='#cat',
            allure_name='Заголовок Категории',
        )

        self.phones_button = Button(
            page, strategy='by_text', value='Phones', allure_name='Phones'
        )
        self.laptops_button = Button(
            page, strategy='by_text', value='Laptops', allure_name='Laptops'
        )
        self.monitors_button = Button(
            page, strategy='by_text', value='Monitors', allure_name='Monitors'
        )

        self.products = Element(
            page,
            strategy='locator',
            selector='#tbodyid',
            allure_name='Карточки товаров',
        )

        self.cards = Element(
            page,
            strategy='locator',
            selector='.card',
            allure_name='Карточка товара',
        )

        self.cards_titles = Element(
            page,
            strategy='locator',
            selector='.card-title a',
            allure_name='Заголовок карточки',
        )

        self.cart_button = Button(
            page, strategy='locator', selector='#cartur', allure_name='Корзина'
        )

    def open(self):
        """Открытие страницы по URL"""

        self.browser.go_to_url(url=self.url)

    def assert_categories_presence(self):
        """Проверка наличия заголовка CATEGORIES"""

        self.categories_header.wait_for()
        self.categories_header.have_text('CATEGORIES')

    def assert_phones_button_is_displayed_and_enabled(self):
        """Проверка кликабельности кнопки Phones"""

        self.phones_button.assert_element_visibility()
        self.phones_button.assert_element_state_of_activity()

    def navigate_to_phones_section(self):
        """Переход в раздел Телефоны"""

        self.phones_button.click()
        self.page.wait_for_timeout(1500)

    def assert_laptops_button_is_displayed_and_enabled(self):
        """Проверка кликабельности кнопки Laptops"""

        self.laptops_button.assert_element_visibility()
        self.laptops_button.assert_element_state_of_activity()

    def navigate_to_laptops_section(self):
        """Переход в раздел Ноутбуки"""

        self.laptops_button.click()
        self.page.wait_for_timeout(1500)

    def assert_monitors_button_is_displayed_and_enabled(self):
        """Проверка кликабельности кнопки Monitors"""

        self.monitors_button.assert_element_visibility()
        self.monitors_button.assert_element_state_of_activity()

    def navigate_to_monitors_section(self):
        """Переход в раздел Мониторы"""

        self.monitors_button.click()
        self.page.wait_for_timeout(1500)

    def assert_number_of_cards(self, number_of_cards: int):
        """Проверка количества карточек на странице"""

        all_cards = self.cards.get_element()
        cards_count = all_cards.count()
        assert (
            cards_count == number_of_cards
        ), f'Number of cards should be {number_of_cards} but got {cards_count}'

    def assert_display_of_cards_with_similar_title(self, title: str):
        """Проверка отображения карточек с указанным названием"""

        self.products.wait_for()

        all_cards = self.cards.get_element()
        cards_count = all_cards.count()

        cards_with_title_count = 0
        for i in range(cards_count):
            card_text = all_cards.nth(i).text_content()
            if title in card_text:
                cards_with_title_count += 1

        assert (
            cards_with_title_count >= 2
        ), f'Отображаются не все карточки с названием {title}'

    def navigate_to_certain_product_card_page(self, card_number: int):
        """Переход на страницу карточки товара по её номеру"""

        all_card_titles = self.cards_titles.get_element()

        actual_num = card_number - 1
        product_title = all_card_titles.nth(actual_num)
        product_title.wait_for()

        with self.page.expect_navigation():
            product_title.click()

        page_url = self.page.url
        assert page_url.endswith(
            f'{PRODUCT_CARD_ENDPOINT}{card_number}'
        ), f'{page_url} should end with {PRODUCT_CARD_ENDPOINT}{card_number}'

    def navigate_to_cart(self):
        """Переход в корзину"""

        self.cart_button.click()
        page_url = self.page.url

        assert page_url.endswith(
            CART_ENDPOINT
        ), f'{page_url} should end with {CART_ENDPOINT}'
