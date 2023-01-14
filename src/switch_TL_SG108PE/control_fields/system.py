"""Contains code to manage system section from menu tab."""

import ipaddress
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .control_field import ControlField
from ..utils import Frame
from ..exceptions import InvalidDescriptionException, InvalidUserAccountDetailsException, DHCPSettingsEnabledException


class SystemControlField(ControlField):
    """Creates object to control system settings on switch."""

    MENU_SECTION = 'System'

    @ControlField.login_required
    def system_info(self) -> dict[str, str]:
        """
        Gets switch system information.
        :return: dict with basic information about switch system
        """
        system_info = {}
        self.open_tab(self.MENU_SECTION, 'System Info')
        self.web_controller.switch_to_frame(Frame.MAIN)
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
            self.web_controller.wait_until_element_is_present(*artifact_details)
            artifact = self.web_controller.find_element(*artifact_details)
            system_info[key] = artifact.text
        return system_info

    @ControlField.login_required
    def set_device_description(self, description: str) -> bool:
        """
        Sets name of switch visible in network.
        :param description: name of device
        :return: True if name was successfully changed, otherwise False
        """
        description = str(description)
        if len(description) > 32:
            raise InvalidDescriptionException('The length of device description should not be more than 32 characters.')
        self.open_tab(self.MENU_SECTION, 'System Info')
        self.web_controller.switch_to_frame(Frame.MAIN)
        input_field_details = (By.XPATH, "//input[@id='tDevDscr']")
        self.web_controller.wait_until_element_is_present(*input_field_details)
        input_field = self.web_controller.find_element(*input_field_details)
        input_field.clear()
        input_field.send_keys(description)
        apply_button_details = (By.XPATH, "//input[@id='btApply']")
        self.web_controller.find_element(*apply_button_details).click()
        return self.wait_for_success_alert()

    @ControlField.login_required
    def ip_settings(self) -> dict[str, str]:
        """
        Gets host settings. It shows host assigned to switch in network.
        :return: information about host, mask, gateway
        """
        ip_info = {}
        self.open_tab(self.MENU_SECTION, 'IP Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        ip_settings_artifacts_ids = {
            'DHCP Setting': {'id': 'check_dhcp', 'ele_type': 'select'},
            'IP Address': {'id': 'txt_addr', 'ele_type': 'input'},
            'Subnet Mask': {'id': 'txt_mask', 'ele_type': 'input'},
            'Default Gateway': {'id': 'txt_gateway', 'ele_type': 'input'},
        }
        for key, value in ip_settings_artifacts_ids.items():
            artifact_details = (By.XPATH, f"//{value['ele_type']}[@id='{value['id']}']")
            self.web_controller.wait_until_element_is_present(*artifact_details)
            artifact = self.web_controller.find_element(*artifact_details)
            ip_info[key] = artifact.get_attribute('value')
        return ip_info

    @ControlField.login_required
    def enable_dhcp_configuration(self) -> bool:
        """
        Enables the function of automatic host retrieval from dhcp server in the network.
        :return: True if settings was successfully enabled, otherwise False
        """
        return self._select_dhcp_option_in_ip_settings('Enable')

    @ControlField.login_required
    def disable_dhcp_configuration(self) -> bool:
        """
        Disables the function of automatic host retrieval from dhcp server in the network.
        User should configure host manually.
        :return: True if settings was successfully disabled, otherwise False
        """
        return self._select_dhcp_option_in_ip_settings('Disable')

    @ControlField.login_required
    def set_ip(self, ip_address: str, subnet_mask: str, default_gateway: str) -> bool:
        """
        Sets switch host, netmask, gateway. It works only if dhcp configuration is disabled.
        :param ip_address: switch host
        :param subnet_mask: mask dedicated for host
        :param default_gateway: gateway for switch network
        :return: True if host details was configured successfully, otherwise False
        """
        ipaddress.ip_address(ip_address)
        ipaddress.ip_address(subnet_mask)
        ipaddress.ip_address(default_gateway)
        ip_settings = self.ip_settings()
        if ip_settings['DHCP Setting'] != 'disable':
            raise DHCPSettingsEnabledException('DHCP settings are enabled. '
                                           'Disable it to set own host. Use "disable_dhcp_settings()" method.')
        self._enter_text_value_in_input_filed(ip_address, 'txt_addr')
        self._enter_text_value_in_input_filed(subnet_mask, 'txt_mask')
        self._enter_text_value_in_input_filed(default_gateway, 'txt_gateway')
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='submit']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=True)
        return self.wait_for_success_alert()

    @ControlField.login_required
    def led_on(self) -> bool:
        """
        Turns on led in front site switch panel.
        :return: True if led was turned on, otherwise False
        """
        return self._select_led_radio_in_led_settings('on')

    @ControlField.login_required
    def led_off(self) -> bool:
        """
        Turns off led in front site switch panel.
        :return: True if led was turned off, otherwise False
        """
        return self._select_led_radio_in_led_settings('off')

    @ControlField.login_required
    def user_account(self) -> dict[str, str]:
        """
        Returns username of admin account.
        :return: username
        """
        self.open_tab(self.MENU_SECTION, 'User Account')
        self.web_controller.switch_to_frame(Frame.MAIN)
        input_field_details = (By.XPATH, "//input[@id='txt_username']")
        self.web_controller.wait_until_element_is_present(*input_field_details)
        input_field = self.web_controller.find_element(*input_field_details)
        return {'Current Username': input_field.get_attribute('value')}

    @ControlField.login_required
    def set_user_account_details(self, username: str, current_password: str, new_password: str,
                                 confirm_password: str) -> bool:
        """
        Sets new username and password for admin account.
        :param username: current or new username
        :param current_password: old password
        :param new_password: new password
        :param confirm_password: new password (confirmation)
        :return: True if details was set successfully
        """
        self.open_tab(self.MENU_SECTION, 'User Account')
        self.web_controller.switch_to_frame(Frame.MAIN)
        self._enter_text_value_in_input_filed(str(username), 'txt_username')
        self._enter_text_value_in_input_filed(str(current_password), 'txt_oldpwd')
        self._enter_text_value_in_input_filed(str(new_password), 'txt_userpwd')
        self._enter_text_value_in_input_filed(str(confirm_password), 'txt_confirmpwd')
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=True)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise InvalidUserAccountDetailsException(
                f'Cannot set users details: username="{username}", current_password="****", new_password="****", '
                f'confirm_password="****" due to unknown error.'
            )
        if alert_info != 'Operation successful.':
            raise InvalidUserAccountDetailsException(f'Cannot set users details: {alert_info}')
        return True

    def _enter_text_value_in_input_filed(self, value: str, input_id: str) -> None:
        input_field_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*input_field_details)
        input_field = self.web_controller.find_element(*input_field_details)
        input_field.clear()
        input_field.send_keys(value)

    def _select_dhcp_option_in_ip_settings(self, action: str = 'Enable') -> bool:
        self.open_tab(self.MENU_SECTION, 'IP Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        dhcp_settings_select_details = (By.XPATH, "//select[@id='check_dhcp']")
        self.web_controller.wait_until_element_is_present(*dhcp_settings_select_details)
        dhcp_settings_select = Select(self.web_controller.find_element(*dhcp_settings_select_details))
        dhcp_settings_select.select_by_visible_text(action)
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='submit']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=True)
        return self.wait_for_success_alert()

    def _select_led_radio_in_led_settings(self, action: str = 'on') -> bool:
        self.open_tab(self.MENU_SECTION, 'LED On/Off')
        self.web_controller.switch_to_frame(Frame.MAIN)
        led_on_radio_details = (By.XPATH, f"//input[@id='led_{action}']")
        self.web_controller.wait_until_element_is_present(*led_on_radio_details)
        led_on_radio = self.web_controller.find_element(*led_on_radio_details)
        led_on_radio.click()
        apply_button_details = (By.XPATH, "//td/a[@class='BTN']/input[@name='led_cfg']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()
