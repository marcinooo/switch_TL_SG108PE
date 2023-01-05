"""Contains main class to control switch."""

from typing import List
from selenium import webdriver as wd

from switch_TL_SG108PE.web_controller import WebController
from switch_TL_SG108PE.control_fields.control_field import ControlField
from switch_TL_SG108PE.control_fields.system import SystemControlField
from switch_TL_SG108PE.control_fields.switching import SwitchingControlField
from switch_TL_SG108PE.control_fields.monitoring import MonitoringControlField
from switch_TL_SG108PE.control_fields.vlan import VLANControlField
from switch_TL_SG108PE.control_fields.qos import QoSControlField
from switch_TL_SG108PE.control_fields.poe import PoEControlField
from switch_TL_SG108PE.errors import LoginError, LogoutError, TpLinkSwitchError, SwitchManagerNotConnectedError


class SwitchManager:
    """Creates object to control switch admin page via selenium library."""

    def __init__(self):
        self.ip = None
        self.login = None
        self.password = None
        self.is_connected = False
        self._web_controller = None
        self._control_fields = {}

    def connect(self, ip: str, login: str, password: str, webdriver=None) -> None:  # TODO: add type of webdriver
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
            webdriver = wd.Chrome()
        self._web_controller = WebController(ip, login, password, webdriver)
        self._web_controller.login()
        self.is_connected = True
        self._control_fields = {
            'system': SystemControlField(self._web_controller),
            'switching': SwitchingControlField(self._web_controller),
            'monitoring': MonitoringControlField(self._web_controller),
            'VLAN': VLANControlField(self._web_controller),
            'QoS': QoSControlField(self._web_controller),
            'PoE': PoEControlField(self._web_controller)
        }

    def disconnect(self) -> None:
        """
        Disconnects SwitchManager from admin web page of switch.
        :return: None
        """
        self._web_controller.logout()
        self.ip = None
        self.login = None
        self.password = None
        self._web_controller = None
        self.is_connected = False
        self._destroy_control_fields()
        self._control_fields = {}

    def control(self, control_field: str) -> ControlField:
        """
        Returns object to control particular section in admin web page.
        :param control_field: name of control field (according to menu nav in admin web page)
        :return: given control field
        """
        if not self.is_connected:
            raise SwitchManagerNotConnectedError('Switch manager is not connected. Please call connect() method first.')
        return self._control_fields[control_field]

    def get_control_fields(self) -> List[str]:
        """
        Returns list of possible control fields according to manu in admin web page.
        :return: control fields
        """
        return list(self._control_fields.keys())

    def _destroy_control_fields(self):
        for value in self._control_fields.values():
            del value

    def __del__(self):
        self._destroy_control_fields()
