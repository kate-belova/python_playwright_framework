import allure


@allure.story('Главная страница')
class TestBasePage:
    @allure.title('Проверка количества карточек товаров раздела "Monitors"')
    def test_monitors(self, base_page):
        base_page.open()
        base_page.navigate_to_monitors_section()
        base_page.assert_number_of_cards(2)

    @allure.title('Проверка возможности перехода в Корзину с Главной страницы')
    def test_navigation_to_cart(self, base_page):
        base_page.open()
        base_page.navigate_to_cart()
