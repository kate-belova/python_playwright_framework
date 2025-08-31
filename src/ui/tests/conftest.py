from pathlib import Path

import pytest

from src.ui.browser.browser_launcher import BrowserLauncher
from src.ui.pages.base_page import BasePage
from src.ui.pages.cart_page import CartPage

CONFIG_PATH = Path(__file__).parent.parent / 'config_browser.yaml'


@pytest.fixture()
def browser():
    driver = BrowserLauncher(str(CONFIG_PATH))
    new_page = driver.create_page()
    yield new_page
    driver.close()


@pytest.fixture
def base_page(browser):
    return BasePage(browser)


@pytest.fixture
def cart_page(browser):
    return CartPage(browser)
