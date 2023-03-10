from typing import Callable, Optional
from selenium.webdriver.remote.webelement import WebElement
from typing import Dict, Literal

FINDER_METHOD = Callable[[Optional[int], str, Optional[bool]], WebElement]

RESOURCES: Dict[str, str] = {
    "stamina": "div[id='nightclub-singleassault-attack-19'] div",
    "addiction": "div[id='nightclub-singleassault-attack-22'] div",
}


def get_resource(
    method: FINDER_METHOD, resource: Literal["stamina", "hp", "addiction"]
) -> float:
    _stamina_el: WebElement = method(selector=RESOURCES.get(resource))
    value = _stamina_el.value_of_css_property("width").split("px")[0]
    return float(f"{((float(value) / 128) * 100):.2f}")
