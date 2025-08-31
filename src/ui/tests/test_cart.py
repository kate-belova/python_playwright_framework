import allure


class TestCartPage:
    @allure.title('Проверка того, что кнопка "Place Order" активна')
    def test_place_order_button_visibility(self, cart_page):
        cart_page.open()
        cart_page.assert_place_order_button_is_displayed_and_enabled()
