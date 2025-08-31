from playwright.sync_api import Page

from src.ui.helper.urls import BASE_URL, CART_ENDPOINT
from src.ui.page_elements.button import Button
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

    def assert_place_order_button_is_displayed_and_enabled(self):
        """Проверка кликабельности кнопки Place Order"""
        self.place_order_button.assert_element_visibility()
        self.place_order_button.assert_element_state_of_activity()
