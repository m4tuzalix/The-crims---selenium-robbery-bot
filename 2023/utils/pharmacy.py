from utils.html_elements import ElementFinder


class Pharmacy:
    TOXIC = 0

    def __init__(self, finder: ElementFinder) -> None:
        self.finder = finder

    def enter_pharmacy(self):
        self.finder.button_click(selector="li[id='menu-hospital']")

    def detoxicate(self):
        self.finder.button_click(
            selector="button[class='btn btn-small btn-inverse pull-left']"
        )

    @staticmethod
    def reset_toxic():
        Pharmacy.TOXIC = 0

    @staticmethod
    def update_toxic(value: float | int):
        Pharmacy.TOXIC += value
