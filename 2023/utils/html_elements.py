from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from utils.exceptions import ElementNotFoundException
from typing import Callable, List, Tuple, Dict
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
import time

ELEMENT_TYPE = WebElement | List[WebElement] | None
FINDER_METHOD = Callable[[str, str], ELEMENT_TYPE]
FINDER_TYPES = Dict[str, Dict[bool, ELEMENT_TYPE]]

IGNORED_EXCEPTIONS = (ElementClickInterceptedException, StaleElementReferenceException)


class ElementFinder:
    types: FINDER_TYPES = {
        "by_css": {
            False: EC.element_to_be_clickable,
            True: EC.presence_of_all_elements_located,
        }
    }

    def __init__(self, driver: Chrome) -> None:
        self.driver = driver

    def by_css(
        self, delay: int = 10, selector: str = None, multiple: bool = False
    ) -> WebElement | List[WebElement]:
        method: FINDER_METHOD = ElementFinder.types.get("by_css").get(multiple)
        args: Tuple[str, str] = (By.CSS_SELECTOR, selector)
        try:
            return WebDriverWait(
                driver=self.driver, timeout=delay, ignored_exceptions=IGNORED_EXCEPTIONS
            ).until(method(args))
        except:
            raise ElementNotFoundException(
                "Element could not be found in the given time"
            )

    def button_click(self, selector: str, delay: int = 10):
        if button := self.by_css(selector=selector, delay=delay):
            try:
                button.click()
            except ElementClickInterceptedException:
                self.button_click(selector, delay=delay)
            except StaleElementReferenceException:
                time.sleep(0.5)
                self.driver.refresh()
                self.button_click(selector, delay=delay)

    def js_click(self, selector: str):
        if self.by_css(selector=selector):
            self.driver.execute_script(
                """
                                            const selector = arguments[0]
                                            const button = document.querySelector(selector)
                                            button.click()
                                       """,
                selector,
            )
