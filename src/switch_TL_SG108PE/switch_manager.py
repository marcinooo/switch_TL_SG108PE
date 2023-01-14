"""Contains main class to control switch."""

from typing import List
from selenium import webdriver as wd
from selenium.webdriver.remote.webdriver import WebDriver

from .web_controller import WebController
from .control_fields.control_field import ControlField
from .control_fields.system import SystemControlField
from .control_fields.switching import SwitchingControlField
from .control_fields.monitoring import MonitoringControlField
from .control_fields.vlan import VLANControlField
from .control_fields.qos import QoSControlField
from .control_fields.poe import PoEControlField
from .exceptions import SwitchManagerNotConnectedException, UnknownControlFieldError


class SwitchManager:
    """Creates object to control switch TL-SG108PE."""

    def __init__(self) -> None:
        self.ip = None
        self.login = None
        self.password = None
        self.is_connected = False
        self._web_controller = None
        self._control_fields = {}

    def connect(self, ip: str, login: str, password: str, webdriver: WebDriver = None) -> None:
        """
        Connects SwitchManager to admin web page of switch.
        :param ip: ip address of switch
        :param login: name of login
        :param password: secret password
        :param webdriver: custom webdriver object
        :return: None
        """
        self.ip = ip  # TODO: checking ip
        self.login = login
        self.password = password
        if webdriver is None:
            # options = wd.ChromeOptions()  # TODO: add option to open web browser in background
            # options.add_argument("--headless")
            # webdriver = wd.Chrome(chrome_options=options)
            webdriver = wd.Chrome()
        self._web_controller = WebController(ip, login, password, webdriver)
        self._web_controller.login()
        self._control_fields = {
            'system': SystemControlField(self._web_controller),
            'switching': SwitchingControlField(self._web_controller),
            'monitoring': MonitoringControlField(self._web_controller),
            'VLAN': VLANControlField(self._web_controller),
            'QoS': QoSControlField(self._web_controller),
            'PoE': PoEControlField(self._web_controller)
        }
        self.is_connected = True

    def disconnect(self) -> None:
        """
        Disconnects SwitchManager from admin web page of switch.
        :return: None
        """
        self._web_controller.logout()
        self._web_controller.quit()
        self.ip = None
        self.login = None
        self.password = None
        self._web_controller = None
        self.is_connected = False
        self._destroy_control_fields()
        self._control_fields = {}

    def control(self, control_field: str) -> ControlField:
        """
        Returns object to control particular section in admin web page - control field.
        There are 6 control sections: system, switching, monitoring, VLAN, QoS, PoE
        :param control_field: name of control field (according to sidebar navigation in admin web page)
        :return: given control field
        """
        if control_field not in self._control_fields:
            raise UnknownControlFieldError(f'"{control_field}" control filed is not recognised. '
                                           f'Possible control fields: {", ".join(self._control_fields.keys())}')
        if not self.is_connected:
            raise SwitchManagerNotConnectedException('Switch manager is not connected. Please call connect() method first.')
        return self._control_fields[control_field]

    def get_control_fields(self) -> List[str]:
        """
        Returns list of possible control fields according to sidebar navigation in admin web page.
        :return: control fields
        """
        return list(self._control_fields.keys())

    def _destroy_control_fields(self) -> None:
        del self._control_fields

    def __del__(self) -> None:
        self._destroy_control_fields()
