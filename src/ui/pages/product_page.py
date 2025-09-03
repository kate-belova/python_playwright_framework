from playwright.sync_api import Page

from src.ui.page_elements.button import Button
from src.ui.page_elements.text import Text
from src.ui.pages.base_page import BasePage


class ProductPage(BasePage):
    """Логика для тестов карточки товара"""

    def __init__(self, page: Page):
        super().__init__(page)

        self.product_title = Text(
            page,
            strategy='locator',
            selector='h2.name',
            allure_name='Название товара',
        )

        self.product_price = Text(
            page,
            strategy='locator',
            selector='h3.price-container',
            allure_name='Цена товара',
        )

        self.add_to_cart_button = Button(
            page,
            strategy='by_text',
            value='Add to cart',
            allure_name='Кнопка добавить в корзину',
        )

    def wait_for_page_load(self):
        """Ожидание загрузки страницы товара"""

        self.product_title.wait_for()
        self.product_price.wait_for()
        self.add_to_cart_button.wait_for()

    def get_product_info(self):
        """Получение информации о товаре"""

        self.wait_for_page_load()

        product_name = self.product_title.get_text()
        full_price_text = self.product_price.get_text()
        product_price = full_price_text.split('*')[0].strip().replace('$', '')

        return product_name, product_price

    def add_product_to_cart(self):
        """Добавление товара в корзину"""

        product_name, product_price = self.get_product_info()

        with self.page.expect_event('dialog') as dialog_info:
            self.add_to_cart_button.click()

        dialog = dialog_info.value
        dialog.accept()

        self.page.wait_for_timeout(500)

        return product_name, product_price
