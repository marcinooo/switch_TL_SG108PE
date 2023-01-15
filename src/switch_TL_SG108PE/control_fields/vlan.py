"""Contains code to manage vlan section from menu tab."""

from typing import List, Dict, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .control_field import ControlField
from ..utils import Frame, validate_vlan_id, validate_port_id, get_port_label
from ..port import IEEE8021QPort
from ..exceptions import (MtuVlanIsNotEnabled, VlanConfigurationIsNotEnabledException, WrongNumberOfPortsException,
                          VlanIdException, PortIdException)


class VLANControlField(ControlField):
    """Creates object to control VLAN settings on switch."""

    MENU_SECTION = 'VLAN'

    @ControlField.login_required
    def mtu_vlan_configuration(self) -> Dict[str, str]:
        """
        Returns mtu VLAN configuration status and current uplink port.
        :return: downloaded details
        """
        self.open_tab(self.MENU_SECTION, 'MTU VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        mtu_vlan = {
            'MTU VLAN Configuration': 'Enable' if self._is_vlan_configuration_enabled('mtu_en') else 'Disable',
            'Current Uplink Port': self._get_current_uplink_port()
        }
        return mtu_vlan

    @ControlField.login_required
    def enable_mtu_vlan_configuration(self) -> bool:
        """
        Enables mtu VLAN configuration.
        :return: Ture if configuration was enabled successfully, otherwise False
        """
        return self._select_mtu_vlan_configuration('Enable')

    @ControlField.login_required
    def disable_mtu_vlan_configuration(self) -> bool:
        """
        Disables mtu VLAN configuration.
        :return: Ture if configuration was disabled successfully, otherwise False
        """
        return self._select_mtu_vlan_configuration('Disable')

    @ControlField.login_required
    def change_mtu_vlan_uplink_port(self, port: int) -> bool:
        """
        Select a port as uplink port.
        MTU VLAN (Multi-Tenant Unit VLAN) defines an uplink port which will build up several VLANs with each of
        the other ports. Each VLAN contains two ports, the uplink port and one of the other ports in the switch,
        so the uplink port can communicate with any other port but other ports cannot communicate with each other.
        :param port: port id
        :return: True if port was set successful, otherwise False
        """
        validate_port_id(port)
        port = get_port_label(port_id=port)
        self.open_tab(self.MENU_SECTION, 'MTU VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        is_mtu_vlan_configuration_enabled = self._is_vlan_configuration_enabled('mtu_en')
        if not is_mtu_vlan_configuration_enabled:
            raise MtuVlanIsNotEnabled('MTU VLAN should be enabled before setting uplink port.')
        select_port_details = (By.XPATH, "//div[@id='div_sec_title']//select[@name='uplinkPort']")
        self.web_controller.wait_until_element_is_present(*select_port_details)
        select_port = Select(self.web_controller.find_element(*select_port_details))
        select_port.select_by_visible_text(port.value)
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='mtu_uplink']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.login_required
    def port_based_vlan_configuration(self) -> Dict[str, Union[List[str], str]]:
        """
        Returns information about port based VLANs.
        :return: downloaded configuration info
        """
        self.open_tab(self.MENU_SECTION, 'Port Based VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        configuration_enabled = self._is_vlan_configuration_enabled('pvlan_en')
        port_based_vlan_configuration = {
            'Port Based VLAN Configuration': 'Enable' if configuration_enabled else 'Disable',
            'VLANs': []
        }
        if not configuration_enabled:
            return port_based_vlan_configuration
        vlan_ports_tds_details = (By.XPATH,
                                  "//div[not(@id='div_sec_title')]/form/table/tbody/tr[not(@class='TABLE_HEAD')]/td")
        self.web_controller.wait_until_element_is_present(*vlan_ports_tds_details)
        vlan_ports_tds = self.web_controller.find_elements(*vlan_ports_tds_details)
        vlan_ports_tds = vlan_ports_tds[18:-3]
        for i in range(0, len(vlan_ports_tds), 3):
            port_based_vlan_configuration['VLANs'].append({'VLAN ID': vlan_ports_tds[i].text,
                                                           'VLAN Member Port': vlan_ports_tds[i+1].text})
        return port_based_vlan_configuration

    @ControlField.login_required
    def enable_port_based_vlan_configuration(self) -> bool:
        """
        Enables port based VLAN configuration management.
        :return: Ture if configuration was enabled successfully, otherwise False
        """
        return self._select_port_based_vlan_configuration('Enable')

    @ControlField.login_required
    def disable_port_based_vlan_configuration(self) -> bool:
        """
        Disables port based VLAN configuration management.
        :return: Ture if configuration was disabled successfully, otherwise False
        """
        return self._select_port_based_vlan_configuration('Disable')

    @ControlField.login_required
    def add_port_based_vlan(self, vlan_id: int, ports: List[int]) -> bool:
        """
        Add new port based VLAN.
        :param vlan_id: id of VLAN (2-8)
        :param ports: list of ports IDs to add (up to 7 ports we can add)
        :return: True if VLAN was created successfully, otherwise False
        """
        validate_vlan_id(vlan_id)
        for port in ports:
            validate_port_id(port)
        if not 2 <= vlan_id <= 8:
            raise VlanIdException('VLAN ID must be in range of 2-8!')
        if len(ports) > 7:
            raise WrongNumberOfPortsException("Can't remove all ports from VLAN 1.")
        self.open_tab(self.MENU_SECTION, 'Port Based VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        if not self._is_vlan_configuration_enabled('pvlan_en'):
            raise VlanConfigurationIsNotEnabledException(
                'Port VLAN configuration should be enabled before reading vlan details.')
        self._fill_add_port_base_vlan_form(vlan_id, ports)
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='pvlan_add']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.login_required
    def remove_port_based_vlan(self, vlan_id: int) -> bool:
        """
        Removes given port based VLAN by id.
        :param vlan_id: VLAN ID
        :return: True if VLAN was deleted successfully, otherwise False
        """
        validate_vlan_id(vlan_id)
        self.open_tab(self.MENU_SECTION, 'Port Based VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        if not self._is_vlan_configuration_enabled('pvlan_en'):
            raise VlanConfigurationIsNotEnabledException('Port VLAN should be enabled before reading vlan details.')
        if not any(vlan['VLAN ID'] == str(vlan_id) for vlan in self.port_based_vlan_configuration()['VLANs']):
            raise VlanIdException(f'VLAN {vlan_id} is not added in configuration.')
        delete_vlan_checkbox_details = (By.XPATH, f"//input[@id='vlan_{vlan_id}']")
        self.web_controller.wait_until_element_is_present(*delete_vlan_checkbox_details)
        delete_vlan_checkbox = self.web_controller.find_element(*delete_vlan_checkbox_details)
        delete_vlan_checkbox.click()
        delete_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='pvlan_del']")
        self.apply_settings(*delete_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.login_required
    def ieee_802_1q_vlan_configuration(self) -> Dict[str, str]:
        """
        Returns information about 802.1Q VLANs.
        :return: downloaded configuration info
        """
        self.open_tab(self.MENU_SECTION, '802.1Q VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        configuration_enabled = self._is_vlan_configuration_enabled('qvlan_en')
        ieee_802_1q_vlan_configuration = {
            '802.1Q VLAN Configuration': 'Enable' if configuration_enabled else 'Disable',
            'VLANs': []
        }
        if not configuration_enabled:
            return ieee_802_1q_vlan_configuration
        vlan_ports_tds_details = (By.XPATH, "//form/table/tbody/tr[not(@class='TABLE_HEAD')]/td")
        self.web_controller.wait_until_element_is_present(*vlan_ports_tds_details)
        vlan_ports_tds = self.web_controller.find_elements(*vlan_ports_tds_details)
        vlan_ports_tds = vlan_ports_tds[35:-3]
        for i in range(0, len(vlan_ports_tds), 6):
            ieee_802_1q_vlan_configuration['VLANs'].append({
                'VLAN ID': vlan_ports_tds[i].text,
                'VLAN Name': vlan_ports_tds[i+1].text,
                'Member Ports': vlan_ports_tds[i+2].text,
                'Tagged Ports': vlan_ports_tds[i+3].text,
                'Untagged Ports': vlan_ports_tds[i+4].text,
            })
        return ieee_802_1q_vlan_configuration

    @ControlField.login_required
    def enable_ieee_802_1q_vlan_configuration(self) -> bool:
        """
        Enables 802.1Q VLAN configuration management.
        :return: Ture if configuration was enabled successfully, otherwise False
        """
        return self._select_ieee_802_1q_vlan_configuration('Enable')

    @ControlField.login_required
    def disable_ieee_802_1q_vlan_configuration(self) -> bool:
        """
        Disables 802.1Q VLAN configuration management.
        :return: Ture if configuration was disabled successfully, otherwise False
        """
        return self._select_ieee_802_1q_vlan_configuration('Disable')

    @ControlField.login_required
    def add_ieee_802_1q_vlan(self, vlan_id: int, ports: List[IEEE8021QPort], vlan_name: str = '') -> bool:
        """
        Add new 802.1Q VLAN.
        :param vlan_id: VLAN ID
        :param ports: ports to add to given VLAN
        :param vlan_name: name of VLAN
        :return: True if VLAN was created successfully, otherwise False
        """
        validate_vlan_id(vlan_id)
        for port in ports:
            if not isinstance(port, IEEE8021QPort):
                raise PortIdException('Port should be an IEEE8021QPort object')
        if not 1 <= vlan_id <= 4094:
            raise VlanIdException('VLAN ID must be in range of 1-4094!')
        if len(ports) > 8:
            raise WrongNumberOfPortsException("Current switch has only 8 ports.")
        self.open_tab(self.MENU_SECTION, '802.1Q VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        if not self._is_vlan_configuration_enabled('qvlan_en'):
            raise VlanConfigurationIsNotEnabledException(
                '802.1Q VLAN configuration should be enabled before reading vlan details.')
        self._enter_value_in_vlan_input('t_vid', str(vlan_id))
        if vlan_name:
            self._enter_value_in_vlan_input('t_vname', vlan_name)
        selected_port_ids = []
        for port in ports:
            selected_port_ids.append(port.port_id)
            self._select_tagged_or_untagged_port(port)
        for port_id in range(1, 9):
            if port_id not in selected_port_ids:
                self._select_not_member_port(port_id)
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='qvlan_add']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.login_required
    def remove_ieee_802_1q_vlan(self, vlan_id: int) -> bool:
        """
        Removes given 802.1Q VLAN by id.
        :param vlan_id: VLAN ID
        :return: True if VLAN was deleted successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'Port Based VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        vlan_configuration = self.ieee_802_1q_vlan_configuration()
        if vlan_configuration['802.1Q VLAN Configuration'] != 'Enable':
            raise VlanConfigurationIsNotEnabledException(
                '802.1Q VLAN configuration should be enabled before deleting vlan.')
        if not any(vlan['VLAN ID'] == str(vlan_id) for vlan in vlan_configuration['VLANs']):
            raise VlanIdException(f'VLAN {vlan_id} is not added in configuration.')
        delete_vlan_checkbox_details = (By.XPATH, f"//input[@id='vlan_{vlan_id}']")
        self.web_controller.wait_until_element_is_present(*delete_vlan_checkbox_details)
        delete_vlan_checkbox = self.web_controller.find_element(*delete_vlan_checkbox_details)
        delete_vlan_checkbox.click()
        delete_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='qvlan_del']")
        self.apply_settings(*delete_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    def _fill_add_port_base_vlan_form(self, vlan_id: int, ports: List[int]) -> None:
        self._enter_value_in_vlan_input('t_vid', str(vlan_id))
        for i in range(1, 9):
            port_checkbox_details = (By.XPATH, f"//input[@id='port_{i}']")
            self.web_controller.wait_until_element_is_present(*port_checkbox_details)
            port_checkbox = self.web_controller.find_element(*port_checkbox_details)
            if port_checkbox.is_selected() and i not in ports or not port_checkbox.is_selected() and i in ports:
                port_checkbox.click()

    def _enter_value_in_vlan_input(self, input_id: str, value: str) -> None:
        vlan_id_input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*vlan_id_input_details)
        vlan_id_input = self.web_controller.find_element(*vlan_id_input_details)
        vlan_id_input.clear()
        vlan_id_input.send_keys(value)

    def _is_vlan_configuration_enabled(self, input_id: str) -> bool:
        enable_input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*enable_input_details)
        enable_input = self.web_controller.find_element(*enable_input_details)
        return enable_input.is_selected()

    def _get_current_uplink_port(self) -> str:
        current_uplink_port_div_details = (By.XPATH, "//div[@id='div_sec_title']//td/div")
        self.web_controller.wait_until_element_is_present(*current_uplink_port_div_details)
        current_uplink_port_div = self.web_controller.find_element(*current_uplink_port_div_details)
        return current_uplink_port_div.text

    def _select_tagged_or_untagged_port(self, port: IEEE8021QPort) -> None:
        tagged_input_id = f'tagSel_{port.port_id}' if port.tagged else f'untagSel_{port.port_id}'
        port_radio_details = (By.XPATH, f"//input[@id='{tagged_input_id}']")
        self.web_controller.wait_until_element_is_present(*port_radio_details)
        port_radio = self.web_controller.find_element(*port_radio_details)
        port_radio.click()

    def _select_not_member_port(self, port_id: int) -> None:
        not_member_radio_details = (By.XPATH, f"//input[@id='nonSel_{port_id}']")
        self.web_controller.wait_until_element_is_present(*not_member_radio_details)
        not_member_radio = self.web_controller.find_element(*not_member_radio_details)
        not_member_radio.click()

    def _select_mtu_vlan_configuration(self, action: str = 'Enable') -> bool:
        self.open_tab(self.MENU_SECTION, 'MTU VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        is_mtu_vlan_configuration_enabled = self._is_vlan_configuration_enabled('mtu_en')
        if is_mtu_vlan_configuration_enabled and action == 'Enable' or \
                not is_mtu_vlan_configuration_enabled and action == 'Disable':
            return True
        input_id = dict(Enable='mtu_en', Disable='mtu_dis').get(action)
        input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*input_details)
        input_ = self.web_controller.find_element(*input_details)
        input_.click()
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='mtu_mode']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=True)
        return self.wait_for_success_alert()

    def _select_port_based_vlan_configuration(self, action: str = 'Enable') -> bool:
        self.open_tab(self.MENU_SECTION, 'Port Based VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        configuration_enabled = self._is_vlan_configuration_enabled('pvlan_en')
        if configuration_enabled and action == 'Enable' or not configuration_enabled and action == 'Disable':
            return True
        input_id = dict(Enable='pvlan_en', Disable='pvlan_dis').get(action)
        input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*input_details)
        input_ = self.web_controller.find_element(*input_details)
        input_.click()
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='pvlan_mode']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=True)
        return self.wait_for_success_alert()

    def _select_ieee_802_1q_vlan_configuration(self, action: str = 'Enable') -> bool:
        self.open_tab(self.MENU_SECTION, '802.1Q VLAN')
        self.web_controller.switch_to_frame(Frame.MAIN)
        configuration_enabled = self._is_vlan_configuration_enabled('qvlan_en')
        if configuration_enabled and action == 'Enable' or not configuration_enabled and action == 'Disable':
            return True
        input_id = dict(Enable='qvlan_en', Disable='qvlan_dis').get(action)
        input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*input_details)
        input_ = self.web_controller.find_element(*input_details)
        input_.click()
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='qvlan_mode']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=True)
        return self.wait_for_success_alert()
