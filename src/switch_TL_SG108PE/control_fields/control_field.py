from selenium.webdriver.common.by import By

from switch_TL_SG108PE.utils import Frame


class ControlField:

    def __init__(self, manager):
        self.manager = manager

    def open_tab(self, section, tab):
        self.manager.switch_to_frame(Frame.MENU)
        system_info_link_details = (By.XPATH, f"//ul[@id='menu']//li//a[contains(text(), '{tab}')]")
        system_info_link = self.manager.webdriver.find_element(*system_info_link_details)
        if not system_info_link.is_displayed():
            system_link_details = (By.XPATH,
                                   f"//ul[@id='menu']//a[@class='menulink' and contains(text(), '{section}')]")
            self.manager.wait_until_element_is_present(*system_link_details)
            system_link = self.manager.webdriver.find_element(*system_link_details)
            system_link.click()
        self.manager.wait_until_element_is_present(*system_info_link_details)
        system_info_link = self.manager.webdriver.find_element(*system_info_link_details)
        system_info_link.click()

