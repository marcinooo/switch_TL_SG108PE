from selenium import webdriver as wd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from switch_TL_SG108PE.control_fields.system import SystemControlField
from switch_TL_SG108PE.control_fields.switching import SwitchingControlField
from switch_TL_SG108PE.errors import LoginError, LogoutError, TpLinkSwitchError
from switch_TL_SG108PE.utils import Frame


class SwitchManager:

    def __init__(self):
        self.ip = None
        self.login = None
        self.password = None
        self.webdriver = None
        self.is_connected = False
        self._control_fields = {}
        self._active_frame = ''

    def is_logged_in(func):
        def inner(self, *args, **kwargs):
            self.switch_to_default_content()
            top_frame_details = (By.XPATH, f"//frame[@name='{Frame.TOP.value}']")
            self.webdriver.find_element(*top_frame_details)
            return func(self, *args, **kwargs)
        return inner

    def connect(self, ip, login, password, webdriver=None):
        if webdriver is None:
            webdriver = wd.Chrome()
        self.ip = ip  # TODO: checking ip
        self.login = login
        self.password = password
        self.webdriver = webdriver
        self._login()
        self.is_connected = True
        self._control_fields = {
            'system': SystemControlField(self),
            'switching': SwitchingControlField(self),
            # 'monitoring': MonitoringControlField(self),
            # 'VLAN': VLANControlField(self),
            # 'QoS': QoSControlField(self),
            # 'PoE': PoEControlField(self)
        }

    @is_logged_in
    def disconnect(self):
        self._logout()
        self.ip = None
        self.login = None
        self.password = None
        self.webdriver = None
        self.is_connected = False
        self._active_frame = ''

    @is_logged_in
    def get(self, control_field):
        return self._control_fields[control_field]

    def _login(self):
        self.webdriver.get(f'http://{self.ip}')
        try:
            self.wait_until_element_is_present(By.ID, 'logon', close_browser=False)
        except TpLinkSwitchError:
            self._logout()
        self.wait_until_element_is_present(By.ID, 'logon', exception=LoginError)
        self.webdriver.find_element(By.ID, 'username').send_keys(self.login)
        self.webdriver.find_element(By.ID, 'password').send_keys(self.password)
        self.webdriver.find_element(By.ID, 'logon').click()
        self.wait_until_element_is_present(By.XPATH, f"//frame[@name='{Frame.TOP.value}']", exception=LoginError)

    def _logout(self):
        self.switch_to_frame(Frame.MENU)
        logout_link_details = (By.XPATH, "//div[@id='logout']//a[@class='menulink']")
        self.wait_until_element_is_present(*logout_link_details, exception=LogoutError)
        logout_link = self.webdriver.find_element(*logout_link_details)
        logout_link.click()
        self.wait_until_alert_is_present()
        alert = self.webdriver.switch_to.alert
        alert.accept()

    def switch_to_frame(self, frame_name):
        self.switch_to_default_content()
        frame_details = (By.XPATH, f"//frame[@name='{frame_name.value}']")
        self.wait_until_element_is_present(*frame_details)
        frame = self.webdriver.find_element(*frame_details)
        self.webdriver.switch_to.frame(frame)
        self._active_frame = frame_name

    def switch_to_default_content(self):
        self.webdriver.switch_to.default_content()
        self._active_frame = None

    def wait_until_element_is_present(self, method, query, timeout=4, close_browser=True, exception=TpLinkSwitchError):
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.presence_of_element_located((method, query)))
        except (TimeoutException, Exception):
            if close_browser:
                self.webdriver.quit()
            raise exception(f'Element identified as "({method}, {query})" not present after {timeout} seconds')

    def wait_until_element_is_visible(self, method, query, timeout=4, close_browser=True, exception=TpLinkSwitchError):
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.visibility_of_element_located((method, query)))
        except (TimeoutException, Exception):
            if close_browser:
                self.webdriver.quit()
            raise exception(f'Element identified as "({method}, {query})" not visible after {timeout} seconds')

    def wait_until_alert_is_present(self, timeout=4, close_browser=True, exception=TpLinkSwitchError):
        try:
            WebDriverWait(self.webdriver, int(timeout)).until(EC.alert_is_present())
        except (TimeoutException, Exception):
            if close_browser:
                self.webdriver.quit()
            raise exception(f'Alert not present after {timeout} seconds')  # Change error




        #
    # def system_info(self):
    #     pass
    #
    # def ip_setting(self):
    #     pass
    #
    # def led_on(self):
    #     pass
    #
    # def led_off(self):
    #     pass
    #
    # def user_account(self):
    #     pass
    #
    # def config_backup(self):
    #     pass
    #
    # def config_restore(self):
    #     pass
    #
    # def system_reboot(self):
    #     pass
    #
    # def system_reset(self):
    #     pass
    #
    # def firmware_upgrade(self):
    #     pass
    #
    # ###
    #
    # def port_setting_info(self):
    #     pass
    #
    # def port_setting(self):
    #     pass
    #
    # def IGMP_snooping_info(self):
    #     pass
    #
    # def IGMP_snooping(self):
    #     pass
    #
    # def static_LAG_setting_info(self):
    #     pass
    #
    # def static_LAG_setting(self):
    #     pass

    ###




