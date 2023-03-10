from utils.html_elements import ElementFinder
from utils.nightclub import NightClub
from utils.pharmacy import Pharmacy
from utils.exceptions import ElementNotFoundException
from utils.resources import get_resource
from selenium.webdriver.common.by import By
from typing import Tuple, TypeVar
import time

VICTIM_INFO = TypeVar("VICTIM_INFO", bound=Tuple[str, str, str, int])


class Hunt:
    def __init__(
        self, element_finder: ElementFinder, night_club: NightClub, pharmacy: Pharmacy
    ) -> None:
        self.element_finder = element_finder
        self.night_club = night_club
        self.pharmacy = pharmacy

    def _wait_for_victim(self) -> VICTIM_INFO:
        try:
            victim_info = self.element_finder.by_css(
                delay=3, selector="div[class='visitor_information']"
            )
        except ElementNotFoundException:
            return None

        name = victim_info.find_element(
            by=By.CSS_SELECTOR, value="div[class='user_list_username']"
        ).text
        proffesion = victim_info.find_element(
            by=By.CSS_SELECTOR, value="div:nth-child(3)"
        ).text
        rank = victim_info.find_element(
            by=By.CSS_SELECTOR, value="div:nth-child(4)"
        ).text
        respect: int
        for x in victim_info.find_elements(
            by=By.CSS_SELECTOR, value="div:nth-child(5) span"
        ):
            if x.text.isdecimal():
                respect = int(x.text)
        return name, proffesion, rank, respect


    def _good_to_kill(self, respect: int, proffesion: str, rank: str):
        restricted = set("Hitman")
        return 8000 < respect < 40000 and proffesion not in restricted


    def _select_and_kill(self):
        
        if _select := self.element_finder.by_css(
            selector="button[id^='nightclub-singleassault']", delay=5
        ):
            _select.click()
        if _kill := self.element_finder.by_css(
            selector="a[id^='nightclub-select-assault-type-single']", delay=5
        ):
            _kill.click()
        if execution := self.element_finder.by_css(
            selector="button[id*='nightclub-attack']", delay=5
        ):
            execution.click()
            time.sleep(1)


    def _killing_actions(self):
        try:
            if victim_info := self._wait_for_victim():
                name, proffesion, rank, respect = victim_info
                print(f"{name}: {proffesion}/{rank} - {respect}")
                if self._good_to_kill(respect, proffesion, rank):
                    self._select_and_kill()
                    print(f"Killed: {name}")
        except:
            self.night_club.exit_club()

    def do_action(self):
        self.night_club.enter_nightlife()
        self.night_club.enter_club()
        self.restore()
        self._killing_actions()
        self.night_club.exit_club()

    def restore(self):
        try:
            if get_resource(self.element_finder.by_css, "stamina") < 50:
                self.night_club.restore_stamina()
        except:
            pass


