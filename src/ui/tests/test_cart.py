import allure


@allure.story('Корзина')
class TestCartPage:
    @allure.title('Проверка того, что кнопка "Place Order" активна')
    def test_place_order_button_visibility(self, cart_page):
        cart_page.open()
        cart_page.assert_place_order_button_is_displayed_and_enabled()

    @allure.title(
        'Проверка возможности добавления и удаления товаров из корзины'
    )
    def test_add_and_remove_items(self, base_page, product_page, cart_page):
        base_page.open()
        base_page.navigate_to_certain_product_card_page(3)

        product_name, product_price = product_page.add_product_to_cart()
        product_page.navigate_to_cart()

        cart_page.verify_product_added(product_name, product_price, 1)
        cart_page.delete_product()
        cart_page.verify_product_removed(product_name, product_price)
