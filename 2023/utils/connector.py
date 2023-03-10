from selenium.webdriver import Chrome
from utils.html_elements import ElementFinder
import os
from dotenv import load_dotenv


load_dotenv()


class Connector(Chrome):
    def __init__(self, driver: Chrome, finder: ElementFinder) -> None:
        self.driver = driver
        self.finder = finder

    def open_page(self) -> None:
        self.driver.get("https://www.thecrims.com/")

    def login(self) -> None:
        _login = os.environ["login"]
        _password = os.environ["password"]
        _inputs = self.finder.by_css(selector="form input", multiple=True)
        try:
            login_field, password_field = _inputs[0], _inputs[1]
        except IndexError:
            raise Exception("Not enough inputs found")
        else:
            login_field.send_keys(_login)
            password_field.send_keys(_password)

        self.finder.js_click(
            selector="button[class='btn btn-large btn-inverse btn-block']"
        )
