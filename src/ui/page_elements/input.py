import allure

from src.ui.page_elements.base import Base


class Input(Base):
    """Методы для работы с полями ввода"""

    def fill(self, text: str, secure: bool = False, delay: int | float = None):
        """Метод для ввода текста"""

        text = text if not secure else '***'

        with allure.step(f'Ввод текста {text} в поле {self.allure_name}'):
            if delay:
                self._element.type(text=text, delay=delay)
            else:
                self._element.fill(text=text)

    def clear(self):
        """Очистка поля ввода"""

        with allure.step(f'Очистка поля "{self.allure_name}"'):
            self._element.clear()

    def get_input_value(self, timeout_msec: float = None) -> str:
        """Получение текстового значения поля ввода

        :param timeout_msec: время ожидания в миллисекундах
        """

        with allure.step(
            f'Получение значения поля ввода "{self.allure_name}"'
        ):
            return self._element.input_value(timeout=timeout_msec)

    def input_text_into_shadow_root(
        self, shadow_locator: str, shadow_input_locator: str, text: str
    ):
        """Ввод текста в теневом элементе (Shadow DOM) с помощью JS-кода

        :param shadow_locator: локатор теневого элемента
        :param shadow_input_locator: поле для ввода в теневом элементе
        :param text: текст для ввода.
        """

        with allure.step(
            f'Ввод текста: {text} в поле {shadow_input_locator} '
            f'теневого элемента {shadow_locator}'
        ):
            shadow_root = self._element.evaluate_handle(
                f'document.querySelector("{shadow_locator}").shadowRoot'
            )
            input_element = shadow_root.evaluate_handle(
                f'document.querySelector("{shadow_input_locator}")'
            )
            input_element.as_element().fill(text)
