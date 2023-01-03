from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from switch_TL_SG108PE.control_fields.control_field import ControlField
from switch_TL_SG108PE.utils import Frame
from switch_TL_SG108PE.errors import InvalidDescription, TpLinkSwitchError, DHCPSettingsEnabledError


class SystemControlField(ControlField):

    MENU_SECTION = 'System'

    def system_info(self):
        system_info = {}
        self.open_tab(self.MENU_SECTION, 'System Info')
        self.manager.switch_to_frame(Frame.MAIN)
        system_info_artifacts_ids = {
            'Device Description': 'sp_devicetype',
            'MAC Address': 'sp_macaddress',
            'IP Address': 'sp_ipaddress',
            'Subnet Mask': 'sp_netmask',
            'Default Gateway': 'sp_gateway',
            'Firmware Version': 'sp_firewareversion',
            'Hardware Version': 'sp_hardwareversion',
        }
        for key, value in system_info_artifacts_ids.items():
            artifact_details = (By.XPATH, f"//span[@id='{value}']")
            self.manager.wait_until_element_is_present(*artifact_details)
            artifact = self.manager.webdriver.find_element(*artifact_details)
            system_info[key] = artifact.text
        return system_info

    def set_device_description(self, description):
        description = str(description)
        if len(description) > 32:
            raise InvalidDescription('The length of device description should not be more than 32 characters.')
        self.open_tab(self.MENU_SECTION, 'System Info')
        self.manager.switch_to_frame(Frame.MAIN)
        input_field_details = (By.XPATH, "//input[@id='tDevDscr']")
        self.manager.wait_until_element_is_present(*input_field_details)
        input_field = self.manager.webdriver.find_element(*input_field_details)
        input_field.clear()
        input_field.send_keys(description)
        apply_button_details = (By.XPATH, "//input[@id='btApply']")
        self.manager.webdriver.find_element(*apply_button_details).click()
        return self._wait_for_success_alert()

    def ip_settings(self):
        ip_info = {}
        self.open_tab(self.MENU_SECTION, 'IP Setting')
        self.manager.switch_to_frame(Frame.MAIN)
        ip_settings_artifacts_ids = {
            'DHCP Setting': {'id': 'check_dhcp', 'ele_type': 'select'},
            'IP Address': {'id': 'txt_addr', 'ele_type': 'input'},
            'Subnet Mask': {'id': 'txt_mask', 'ele_type': 'input'},
            'Default Gateway': {'id': 'txt_gateway', 'ele_type': 'input'},
        }
        for key, value in ip_settings_artifacts_ids.items():
            artifact_details = (By.XPATH, f"//{value['ele_type']}[@id='{value['id']}']")
            self.manager.wait_until_element_is_present(*artifact_details)
            artifact = self.manager.webdriver.find_element(*artifact_details)
            ip_info[key] = artifact.get_attribute('value')
        return ip_info

    def enable_dhcp_settings(self):
        self._select_dhcp_option_in_ip_settings('Enable')

    def disable_dhcp_settings(self):
        self._select_dhcp_option_in_ip_settings('Disable')

    def set_ip(self, ip_address, subnet_mask, default_gateway):
        # TODO: Add ips validation
        ip_settings = self.ip_settings()
        if ip_settings['DHCP Setting'] != 'disable':
            raise DHCPSettingsEnabledError('DHCP settings are enabled. '
                                           'Disable it to set own ip. Use "disable_dhcp_settings()" method.')
        self._enter_text_value_in_ip_settings(ip_address, 'txt_addr')
        self._enter_text_value_in_ip_settings(subnet_mask, 'txt_mask')
        self._enter_text_value_in_ip_settings(default_gateway, 'txt_gateway')
        self._apply_ip_settings()
        return self._wait_for_success_alert()

    def led_on(self):
        return self._select_led_radio_in_led_settings('on')

    def led_off(self):
        return self._select_led_radio_in_led_settings('off')

    def user_account(self):
        pass

    def set_user_account_details(self, username, current_password, new_password, confirm_password):
        pass

    def _wait_for_success_alert(self):
        confirmation_alert_details = (By.XPATH, "//span[contains(text(), 'Operation successful.')]")
        try:
            self.manager.wait_until_element_is_visible(*confirmation_alert_details)
        except TpLinkSwitchError:
            return False
        return True

    def _enter_text_value_in_ip_settings(self, value, input_id):
        input_field_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.manager.wait_until_element_is_present(*input_field_details)
        input_field = self.manager.webdriver.find_element(*input_field_details)
        input_field.clear()
        input_field.send_keys(value)

    def _select_dhcp_option_in_ip_settings(self, action='Enable'):
        self.open_tab(self.MENU_SECTION, 'IP Setting')
        self.manager.switch_to_frame(Frame.MAIN)
        dhcp_settings_select_details = (By.XPATH, "//select[@id='check_dhcp']")
        self.manager.wait_until_element_is_present(*dhcp_settings_select_details)
        dhcp_settings_select = Select(self.manager.webdriver.find_element(*dhcp_settings_select_details))
        dhcp_settings_select.select_by_visible_text(action)
        self._apply_ip_settings()
        return self._wait_for_success_alert()

    def _select_led_radio_in_led_settings(self, action='on'):
        self.open_tab(self.MENU_SECTION, 'LED On/Off')
        self.manager.switch_to_frame(Frame.MAIN)
        led_on_radio_details = (By.XPATH, f"//input[@id='led_{action}']")
        self.manager.wait_until_element_is_present(*led_on_radio_details)
        led_on_radio = self.manager.webdriver.find_element(*led_on_radio_details)
        led_on_radio.click()
        self._apply_led_settings()
        return self._wait_for_success_alert()

    def _apply_ip_settings(self):
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='submit']")
        self.manager.wait_until_element_is_present(*apply_button_details)
        self.manager.webdriver.find_element(*apply_button_details).click()
        self.manager.wait_until_alert_is_present()
        alert = self.manager.webdriver.switch_to.alert
        alert.accept()

    def _apply_led_settings(self):
        apply_button_details = (By.XPATH, "//td/a[@class='BTN']/input[@name='led_cfg']")
        self.manager.wait_until_element_is_present(*apply_button_details)
        self.manager.webdriver.find_element(*apply_button_details).click()
