from selenium.webdriver.common.by import By

from switch_TL_SG108PE.utils import Frame


class ControlField:

    def __init__(self, web_controller):
        self.web_controller = web_controller

    @staticmethod
    def require_login(func):
        def inner(self, *args, **kwargs):
            if not self.web_controller.is_logged_in():
                self.web_controller.login()
            return func(self, *args, **kwargs)
        return inner

    def open_tab(self, section, tab):
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
