from abc import ABC
from typing import Literal

import allure
from playwright.sync_api import Page, expect, Locator, ElementHandle


class Base(ABC):
    """Базовый класс для взаимодействия с элементами"""

    def __init__(
        self,
        page: Page,
        strategy: str = None,
        selector: str = None,
        role=None,
        value: str = None,
        allure_name: str = None,
    ):
        self.page = page
        self.strategy = strategy
        self.selector = selector
        self.role = role
        self.value = value
        self.allure_name = allure_name

        if strategy is None or strategy == 'locator':
            if isinstance(selector, str):
                self._element = self.page.locator(self.selector)
                return
            else:
                raise ValueError('Не указан аргумент selector')

        if strategy in [
            'by_role',
            'by_label',
            'by_title',
            'by_placeholder',
            'by_alt_text',
            'by_test_id',
        ]:
            if not isinstance(value, str):
                raise ValueError('Не указан аргумент value')

        if strategy == 'by_role':
            if not isinstance(role, str):
                raise ValueError('Не указан аргумент role')
            self._element = self.page.get_by_role(
                role=self.role, name=self.value
            )
        elif strategy == 'by_label':
            self._element = self.page.get_by_label(text=self.value)
        elif strategy == 'by_title':
            self._element = self.page.get_by_title(text=self.value)
        elif strategy == 'by_placeholder':
            self._element = self.page.get_by_placeholder(text=self.value)
        elif strategy == 'by_alt_text':
            self._element = self.page.get_by_alt_text(text=self.value)
        elif strategy == 'by_text':
            self._element = self.page.get_by_text(text=self.value)
        elif strategy == 'by_test_id':
            self._element = self.page.get_by_test_id(test_id=self.value)
        else:
            raise ValueError(
                f'Указана неверная стратегия: {strategy}. Доступные значения: '
                f'"locator, by_role, by_label, by_title, by_placeholder, '
                f'by_alt_text, by_test_id"'
            )

    def get_element(self) -> Locator:
        """Получение локатора элемента"""
        return self._element

    def get_attribute(self, attribute_name: str) -> str:
        """Получение значение атрибута

        :param attribute_name: локатор с атрибутом (напр. 'p#name')
        """

        with allure.step(
            f'Получение значение атрибута "{attribute_name}" у элемента '
            f'"{self.allure_name}"'
        ):
            return self._element.get_attribute(attribute_name)

    def get_text(self) -> str:
        """Получение текста элемента"""

        with allure.step(f'Получение текста "{self.allure_name}"'):
            return self._element.text_content()

    def click(self) -> None:
        """Клик по элементу"""

        with allure.step(f'Клик по элементу "{self.allure_name}"'):
            self._element.click()

    def double_click(self) -> None:
        """Двойной клик по элементу"""

        with allure.step(f'Клик по элементу "{self.allure_name}"'):
            self.page.dblclick(self.selector)

    def choose_dropdown_option(self, option: str) -> None:
        """Выбор значения из выпадающего списка

        :param option: значение, которое нужно выбрать
        """

        with allure.step(
            f'Выбор значения "{self.value}" у элемента "{self.allure_name}"'
        ):
            self.page.select_option(self.selector, option)

    def is_enabled(self) -> bool:
        """Проверка того, что элемент активирован"""

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" активирован'
        ):
            return self._element.is_enabled()

    def is_disabled(self) -> bool:
        """Проверка того, что элемент неактивен"""

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" неактивен'
        ):
            return self._element.is_disabled()

    def assert_element_state_of_activity(self, enabled=True):
        """Проверка состояния активности элемента

        :param enabled: состояние элемента (включен / выключен)
        """

        element_status = 'активирован' if enabled else 'неактивный'

        with allure.step(
            f'Проверка того, что {self.allure_name} {element_status}'
        ):
            if enabled:
                expect(self._element).to_be_enabled()
            else:
                expect(self._element).to_be_disabled()

    def is_visible(self, timeout_msec: int = None) -> bool:
        """Проверка видимости элемента

        :param timeout_msec: максимальное время ожидания в миллисекундах
        """

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" видимый'
        ):
            return self._element.is_visible(timeout=timeout_msec)

    def assert_element_visibility(self, visible=True):
        """Проверка состояния видимости элемента
        :param visible: видимость элемента
        """

        element_status = 'видимый' if visible else 'невидимый'

        with allure.step(
            f'Проверка того, что {self.allure_name} {element_status}'
        ):
            if visible:
                expect(self._element).to_be_visible()
            else:
                expect(self._element).not_to_be_visible()

    def drag_and_drop(
        self,
        target: Locator,
        start_position: dict = None,
        target_position: dict = None,
    ):
        """Перетаскивание элемента к другому элементу

        :param target: локатор элемента, куда нужно перетащить
        :param start_position: координаты для клика внутри исходного элемента
                            (self._element) напр. {'x':0, 'y':70}
        :param target_position: координаты для клика внутри целевого элемента
                                            напр. {'x':10, 'y':70}
        """

        with allure.step(f'Перетаскивание элемента "{self.allure_name}"'):
            self._element.drag_to(
                target,
                source_position=start_position,
                target_position=target_position,
            )

    def have_text(self, text: str):
        """Проверка того, что элемент содержит указанный текст
                                         (полное соответствие)

        :param text: текст для проверки
        """

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" '
            f'содержит текст: "{text}"'
        ):
            expect(self._element).to_have_text(text)

    def not_have_text(self, text: str):
        """Проверка того, что элемент не содержит указанный текст.

        :param text: текст для проверки
        """

        with allure.step(
            f'Проверка того, что у элемента "{self.allure_name}" '
            f'отсутствует текст: "{text}"'
        ):
            expect(self._element).not_to_have_text(text)

    def contains_text(self, text: str):
        """Проверка того, что текст элемента содержит указанный текст

        :param text: текст для проверки.
        """

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" '
            f'содержит текст: "{text}"'
        ):
            expect(self._element).to_contain_text(text)

    def is_editable(self):
        """Проверка того, что элемент является редактируемым"""

        with allure.step(
            f'Проверка, что элемент "{self.allure_name}" можно редактировать'
        ):
            expect(self._element).to_be_editable()

    def is_empty(self):
        """Проверка того, что элемент ничего не содержит"""

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" пустой'
        ):
            expect(self._element).to_be_empty()

    def hover(self):
        """Установка фиксации (hover) на элементе"""

        with allure.step(f'Поставим hover на элементе "{self.allure_name}"'):
            self._element.hover()

    def focus(self):
        """Установка фокуса на элементе"""

        with allure.step(f'Установка фокуса на элементе "{self.allure_name}"'):
            self._element.focus()

    def locator_has_values(self, value: str | list[str]):
        """Проверка того, что элемент содержит указанные value(s)

        :param value: проверяемые значения
        """

        with allure.step(
            f'Проверка того, что элемент "{self.allure_name}" '
            f'содержит значени(е/я): {value}'
        ):
            element_locator = self._element.select_option(value)
            expect(element_locator).to_have_values(value)

    def wait_for(
        self,
        state: (
            Literal['visible', 'hidden', 'attached', 'detached'] | None
        ) = 'visible',
        timeout_msec: int | None = None,
    ):
        """Ожидание того, что элемент удовлетворяет определенному состоянию

        param: state: ожидаемое состояние
        -`visible` элемент отображается на экране;
        -`hidden` элемент не отображается на экране;
        -`attached` элемент появился в DOM;
        -`detached` элемент исчез из DOM;
        """

        valid_states = ['visible', 'hidden', 'attached', 'detached']
        if state not in valid_states:
            raise ValueError(
                f'State must be one of {", ".join(valid_states)}, '
                f'but got "{state}"'
            )

        element_status = (
            'видимый' if state in ('visible', 'attached') else 'невидимый'
        )
        with allure.step(
            f'Ожидание того, что {self.allure_name} станет {element_status}'
        ):
            self._element.wait_for(state=state, timeout=timeout_msec)

    def get_by_selector(self) -> ElementHandle:
        """Поиск элемента по селектору"""

        return self.page.query_selector(selector=self.selector)

    def get_all_by_selector(self) -> list:
        """Поиск всех элементов по селектору"""

        return self.page.query_selector_all(selector=self.selector)

    def wait_for_selector(
        self,
        state: (
            Literal['visible', 'hidden', 'attached', 'detached'] | None
        ) = 'visible',
        timeout_msec: int | None = None,
    ):
        """Ожидание того, что элемент по селектору будет удовлетворять
        определенному состоянию

        param: state: ожидаемое состояние
        -`visible` элемент отображается на экране;
        -`hidden` элемент не отображается на экране;
        -`attached` элемент появился в DOM;
        -`detached` элемент исчез из DOM;
        """

        valid_states = ['visible', 'hidden', 'attached', 'detached']
        if state not in valid_states:
            raise ValueError(
                f'State must be one of {", ".join(valid_states)}, '
                f'but got "{state}"'
            )

        element_status = (
            'видимый' if state in ('visible', 'attached') else 'невидимый'
        )
        with allure.step(
            f'Ожидание того, что {self.allure_name} станет {element_status}'
        ):
            self.page.wait_for_selector(
                selector=self.selector, state=state, timeout=timeout_msec
            )
