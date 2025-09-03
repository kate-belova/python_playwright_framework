from playwright.sync_api import Page
from src.ui.helper.urls import BASE_URL, CART_ENDPOINT
from src.ui.page_elements.button import Button
from src.ui.page_elements.element import Element
from src.ui.page_elements.text import Text
from src.ui.pages.base_page import BasePage


class CartPage(BasePage):
    """Логика для тестов корзины"""

    def __init__(self, page: Page, url=BASE_URL + CART_ENDPOINT):
        super().__init__(page, url)

        self.place_order_button = Button(
            page,
            strategy='by_role',
            role='button',
            value='Place Order',
            allure_name='Кнопка Place Order',
        )

        self.products_table = Element(
            page,
            strategy='locator',
            selector='.table-responsive',
            allure_name='Таблица товаров в корзине',
        )

        self.product_rows = Element(
            page,
            strategy='locator',
            selector='#tbodyid tr',
            allure_name='Строки товаров',
        )

        self.total_price = Text(
            page,
            strategy='locator',
            selector='#totalp',
            allure_name='Общая цена',
        )

        self.delete_button = Button(
            page,
            strategy='by_text',
            value='Delete',
            allure_name='Кнопка удаления товара',
        )

    def assert_place_order_button_is_displayed_and_enabled(self):
        """Проверка кликабельности кнопки Place Order"""

        self.products_table.wait_for()
        self.place_order_button.assert_element_visibility()
        self.place_order_button.assert_element_state_of_activity()

    def is_product_in_cart(
        self, expected_name: str, expected_price: str
    ) -> bool | None:
        """Проверка наличия товара с указанными названием и ценой"""

        rows = self.product_rows.get_element()
        count = rows.count()

        for i in range(count):
            row_text = rows.nth(i).text_content()
            return expected_name in row_text and expected_price in row_text
        return None

    def get_product_count(self) -> int:
        """Получение количества товаров в корзине"""

        return self.product_rows.get_element().count()

    def verify_product_added(
        self, expected_name: str, expected_price: str, expected_count: int
    ):
        """Проверка добавления товара в корзину"""

        self.page.wait_for_timeout(1500)

        assert self.is_product_in_cart(expected_name, expected_price), (
            f'Товар {expected_name} с ценой {expected_price} '
            f'не найден в корзине'
        )

        total_price = self.total_price.get_text()
        assert total_price == expected_price, (
            f'Общая сумма {total_price} не соответствует '
            f'цене товара {expected_price}'
        )

        products_count = self.get_product_count()
        assert products_count == expected_count, (
            f'Количество товара {products_count} не соответствует '
            f'ожидаемому {expected_count}'
        )

    def delete_product(self):
        """Удаление товара из корзины"""

        self.delete_button.wait_for()
        self.delete_button.assert_element_visibility()
        self.delete_button.assert_element_state_of_activity()

        self.delete_button.click()
        self.product_rows.get_element().first.wait_for(state='detached')

    def verify_cart_is_empty(self):
        """Проверка, что корзина пуста"""
        rows = self.product_rows.get_element()
        assert rows.count() == 0, 'Корзина не пуста — остались товары'

    def verify_product_removed(self, product_name: str, product_price: str):
        """Проверка того, что товар удален из корзины
        :param product_name: название товара
        :param product_price: цена товара
        """

        assert not self.is_product_in_cart(
            product_name, product_price
        ), f'Товар {product_name} все еще находится в корзине после удаления'

        self.verify_cart_is_empty()

    def click_place_order_button(self):
        """Нажатие на кнопку Place Order"""

        self.place_order_button.click()
