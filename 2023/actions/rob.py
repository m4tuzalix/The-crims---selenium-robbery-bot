from utils.html_elements import ElementFinder
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.nightclub import NightClub
from utils.pharmacy import Pharmacy
from typing import Tuple, List
import re


BEST_OPTION = Tuple[WebElement, str]


class Robbery:
    ALL_STAMINA = False

    def __init__(
        self, finder: ElementFinder, night_club: NightClub, pharmacy: Pharmacy
    ) -> None:
        self.finder = finder
        self.night_club = night_club
        self.pharmacy = pharmacy

    def _enter_robbery(self):
        self.finder.button_click(selector="li[id='menu-robbery']")

    def _choose_the_highest_ratio(self, select_el: WebElement) -> BEST_OPTION:
        options_el = select_el.find_elements(by=By.CSS_SELECTOR, value="option")
        while len(options_el) < 2:
            options_el = select_el.find_elements(by=By.CSS_SELECTOR, value="option")
        _best = None
        for option in options_el:
            if "SP: 100%" in option.text:
                _best = option

        return _best, re.findall(r"\d+", _best.text)[0]

    def _select_value(self) -> None:
        if _select := self.finder.by_css(
            selector="select[id='singlerobbery-select-robbery']"
        ):
            _best_option, stamina = self._choose_the_highest_ratio(select_el=_select)
            Select(_select).select_by_visible_text(_best_option.text)

    def _use_all_stamina(self) -> None:
        if not Robbery.ALL_STAMINA:
            self.finder.button_click(
                selector="label[for='full-stamina-robbery-toggle']"
            )
            Robbery.ALL_STAMINA = True

    def _rob(self) -> None:
        self.finder.button_click(selector="button[id='singlerobbery-rob']")

    def _night_club_actions(self) -> None:
        self.night_club.enter_nightlife()
        self.night_club.enter_club()
        self.night_club.restore_stamina()
        self.night_club.exit_club()
        Pharmacy.update_toxic(0.5)

    def _pharmacy_actions(self) -> None:
        self.pharmacy.enter_pharmacy()
        self.pharmacy.detoxicate()
        Pharmacy.reset_toxic()

    def do_action(self) -> None:
        self._enter_robbery()
        self._select_value()
        self._use_all_stamina()
        self._rob()

    def restore(self) -> None:
        self._night_club_actions()
        if Pharmacy.TOXIC > 20:
            self._pharmacy_actions()
