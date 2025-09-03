from faker import Faker
from playwright.sync_api import Page

from src.ui.page_elements.button import Button
from src.ui.page_elements.element import Element
from src.ui.page_elements.input import Input
from src.ui.page_elements.text import Text
from src.ui.pages.base_page import BasePage

faker = Faker()


class OrderPage(BasePage):
    """Логика для тестов формы оформления заказов"""

    def __init__(self, page: Page):
        super().__init__(page)

        self.order_modal_window = Element(
            page,
            strategy='locator',
            selector='#orderModal',
            allure_name='Окно оформления заказа',
        )

        self.name_input = Input(
            page,
            strategy='by_role',
            role='textbox',
            value='Name',
            allure_name='Поле ввода имени',
        )
        self.country_input = Input(
            page,
            strategy='by_role',
            role='textbox',
            value='Country',
            allure_name='Поле ввода страны',
        )
        self.city_input = Input(
            page,
            strategy='by_role',
            role='textbox',
            value='City',
            allure_name='Поле ввода города',
        )
        self.card_input = Input(
            page,
            strategy='by_role',
            role='textbox',
            value='Credit card',
            allure_name='Поле ввода кредитной карты',
        )
        self.month_input = Input(
            page,
            strategy='by_role',
            role='textbox',
            value='Month',
            allure_name='Поле ввода месяца',
        )
        self.year_input = Input(
            page,
            strategy='by_role',
            role='textbox',
            value='Year',
            allure_name='Поле ввода года',
        )

        self.purchase_button = Button(
            page,
            strategy='by_role',
            role='button',
            value='Purchase',
            allure_name='Кнопка Purchase',
        )

        self.congrats = Text(
            page,
            strategy='locator',
            selector='.sweet-alert h2',
            value='Текст спасибо за заказ',
        )

        self.customers_info = Text(
            page,
            strategy='locator',
            selector='p.lead.text-muted',
            allure_name='Информация о покупателе',
        )

    def fill_out_order_form(self):
        """Заполнение данными формы заказа товаров"""

        self.order_modal_window.wait_for()

        name = faker.name()

        self.name_input.fill(name)
        self.country_input.fill(faker.country())
        self.city_input.fill(faker.city())
        self.card_input.fill(faker.credit_card_number(card_type='visa'))
        self.month_input.fill(str(faker.random_int(min=1, max=12)))
        self.year_input.fill(str(faker.random_int(min=2024, max=2030)))

        self.purchase_button.click()
        return name

    def verify_informational_window(self, expected_name):
        """Проверка появления информационного окна и информации в нем

        :param expected_name: ожидаемое имя в информационно окне
        """

        self.order_modal_window.assert_element_visibility()
        self.congrats.have_text('Thank you for your purchase!')

        customers_info = self.customers_info.get_text()

        name_start = customers_info.find('Name')
        name_end = customers_info.rfind('Date')
        name = customers_info[name_start:name_end]
        actual_name = name.split(':')[1].strip()

        assert expected_name == actual_name, (
            f'Фактическое имя {actual_name} покупателя не совпадает '
            f'с ожидаемым {expected_name}'
        )
