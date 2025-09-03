import allure


@allure.story('Форма заказа')
class TestOrderPage:

    @allure.title('Проверка оформления товара')
    def test_place_order(self, base_page, product_page, cart_page, order_page):
        base_page.open()
        base_page.navigate_to_certain_product_card_page(3)

        product_page.add_product_to_cart()
        product_page.navigate_to_cart()

        cart_page.click_place_order_button()

        name = order_page.fill_out_order_form()
        order_page.verify_informational_window(name)
