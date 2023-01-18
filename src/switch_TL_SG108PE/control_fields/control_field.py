"""Contains code to manage elements visible on given section form menu. It is common for all sections."""

from typing import Callable
from functools import wraps
from selenium.webdriver.common.by import By

from ..utils import Frame
from ..exceptions import TpLinkSwitchException


class ControlField:
    """Creates object to control base actions on switch page."""

    def __init__(self, web_controller):
        self.web_controller = web_controller

    @staticmethod
    def login_required(func: Callable) -> Callable:
        """
        Decorator to check if client is login. If client is not login it will try login again.

        :param func: function to decorate
        :return: internal wrapper
        """
        @wraps(func)
        def inner(self, *args, **kwargs):
            if not self.web_controller.is_logged_in():
                self.web_controller.login()
            return func(self, *args, **kwargs)
        return inner

    def open_tab(self, section: str, tab: str) -> None:
        """
        Opens given tab from menu in admin page of switch.

        :param section: main manu section (e.g. System)
        :param tab: subsection from menu (e.g. System Info)
        :return: None
        """
        self.web_controller.switch_to_frame(Frame.MENU)
        system_info_link_details = (By.XPATH, f"//ul[@id='menu']//li//a[contains(text(), '{tab}')]")
        system_info_link = self.web_controller.webdriver.find_element(*system_info_link_details)
        if not system_info_link.is_displayed():
            system_link_details = (By.XPATH,
                                   f"//ul[@id='menu']//a[@class='menulink' and contains(text(), '{section}')]")
            self.web_controller.wait_until_element_is_present(*system_link_details)
            system_link = self.web_controller.webdriver.find_element(*system_link_details)
            system_link.click()
        self.web_controller.wait_until_element_is_present(*system_info_link_details)
        system_info_link = self.web_controller.webdriver.find_element(*system_info_link_details)
        system_info_link.click()

    def wait_for_success_alert(self) -> bool:
        """
        Waits for success html alert.

        :return: True if an alert was occurred, otherwise False
        """
        confirmation_alert_details = (By.XPATH, "//span[contains(text(), 'Operation successful.')]")
        try:
            self.web_controller.wait_until_element_is_visible(*confirmation_alert_details)
        except TpLinkSwitchException:
            return False
        return True

    def get_alert_text(self) -> str:
        """
        Returns alert text.

        :return: text
        """
        alert_details = (By.XPATH, "//span[@id='sp_tip_svr']/span[@class='TIP_CONTENT']")
        try:
            self.web_controller.wait_until_element_is_visible(*alert_details)
        except TpLinkSwitchException:
            return ''
        return self.web_controller.find_element(*alert_details).text

    def apply_settings(self, method: By, query: str, wait_for_confirmation_alert: bool = False) -> None:
        """
        Applies given configuration from filled form. It searches apply button and clicks it.

        :param method: used to specify which attribute is used to locate elements on a page
        :param query: key used to locate elements on a page
        :param wait_for_confirmation_alert: indicates if method should wait for browser alert to confirm applying
        :return: None
        """
        apply_button_details = (method, query)
        self.web_controller.wait_until_element_is_present(*apply_button_details)
        apply_button = self.web_controller.find_element(*apply_button_details)
        apply_button.click()
        if wait_for_confirmation_alert:
            self.web_controller.wait_until_alert_is_present()
            alert = self.web_controller.webdriver.switch_to.alert
            alert.accept()
