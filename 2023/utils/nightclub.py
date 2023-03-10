from utils.html_elements import ElementFinder
from utils.exceptions import ElementNotFoundException
import random

class NightClub:
    def __init__(self, finder: ElementFinder) -> None:
        self.finder = finder

    def enter_nightlife(self):
        self.finder.button_click(selector="li[id='menu-nightlife']", delay=3)

    def enter_club(self):
        clubs = self.finder.by_css(selector="button[class='btn btn-inverse btn btn-inverse btn-small pull-right']", multiple=True)
        _i = random.randint(0, 3)
        clubs[_i].click()

    def restore_stamina(self):
        self.finder.button_click(selector="button[id^='nightclub']")

    def exit_club(self):
        self.finder.button_click(
            selector="button[class='btn btn-inverse btn btn-inverse']", delay=3
        )
