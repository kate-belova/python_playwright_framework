import allure
from playwright.sync_api import expect

from src.ui.page_elements.base import Base


class CheckBox(Base):
    """Методы чекбоксов"""

    def set_checkbox(self, index: int) -> None:
        """Выбор чекбокса

        :param index: индекс чекбокса.
        """

        with allure.step(f'Установка чекбокса "{self.allure_name}"'):
            elements = self._element
            elements.nth(index).check()

    def is_checked(self):
        """Проверка, что чек-бокс выбран"""

        with allure.step(
            f'Проверка, что чекбокс "{self.allure_name}" проставлен'
        ):
            expect(self._element).to_be_checked()
