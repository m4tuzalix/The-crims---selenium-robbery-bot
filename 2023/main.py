from utils.connector import Connector
from actions.rob import Robbery
from utils.nightclub import NightClub
from actions.hunt import Hunt
from utils.pharmacy import Pharmacy
from utils.abstract import Action
from utils.html_elements import ElementFinder
from typing import Dict
from Driver import Driver
import time


ACTIONS: Dict[str, Action] = {"rob": Robbery, "hunt": Hunt}


def main(action: Action, connector: Connector) -> None:
    connector.open_page()
    connector.login()
    while True:
        try:
            action.do_action()
        except:
            continue
        time.sleep(1)


if __name__ == "__main__":
    with Driver() as chrome_driver:
        element_finder = ElementFinder(chrome_driver)
        connector = Connector(driver=chrome_driver, finder=element_finder)
        night_club = NightClub(element_finder)
        pharmacy = Pharmacy(element_finder)

        actionClass: Action = ACTIONS.get("hunt")(element_finder, night_club, pharmacy)

        main(actionClass, connector)
