from selenium.webdriver import Chrome, ChromeOptions
from utils.paths import DRIVER


class Driver(Chrome):
    def __init__(self):
        _options = self._initialize_options()
        super().__init__(executable_path=DRIVER, options=_options)

        self.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def _initialize_options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        return options

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.quit()
