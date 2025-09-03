import allure


@allure.story('Главная страница')
class TestBasePage:

    @allure.title('Проверка количества товаров на главной странице')
    def test_products_amount(self, base_page):
        base_page.open()
        base_page.assert_categories_presence()

        base_page.assert_phones_button_is_displayed_and_enabled()
        base_page.navigate_to_phones_section()
        base_page.assert_number_of_cards(7)

        base_page.assert_laptops_button_is_displayed_and_enabled()
        base_page.navigate_to_laptops_section()
        base_page.assert_number_of_cards(6)

        base_page.assert_monitors_button_is_displayed_and_enabled()
        base_page.navigate_to_monitors_section()
        base_page.assert_number_of_cards(2)

    @allure.title('Проверка соответствия описания вторых товаров')
    def test_products_with_similar_title_display(self, base_page):
        base_page.open()
        base_page.assert_display_of_cards_with_similar_title('Samsung galaxy')

        base_page.navigate_to_laptops_section()
        base_page.assert_display_of_cards_with_similar_title('Sony vaio')

    @allure.title('Проверка возможности перехода в Корзину с Главной страницы')
    def test_navigation_to_cart(self, base_page):
        base_page.open()
        base_page.navigate_to_cart()
