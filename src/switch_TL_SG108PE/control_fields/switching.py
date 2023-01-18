"""Contains code to manage switching section from menu tab."""

from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement

from .control_field import ControlField
from ..utils import Frame, get_port_label, get_lag_label, validate_port_id, validate_lag_id
from ..port import STATUS, SPEED, FLOW_CONTROL
from ..exceptions import (PortSettingsException, IgmpSnoopingSettings, ReportMessageSuppressionSettings,
                          LAGPortException, OptionDisabledException)


class SwitchingControlField(ControlField):
    """Creates object to control switching settings on switch."""

    _MENU_SECTION = 'Switching'

    @ControlField.login_required
    def ports_settings(self) -> Dict[str, Dict[str, str]]:
        """
        Returns settings of all ports.

        :return: settings
        """
        self.open_tab(self._MENU_SECTION, 'Port Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        ports_settings = {}
        ports_rows_details = (By.XPATH, "//table[@class='BORDER']/tbody/tr/td[@class='TABLE_HEAD_BOTTOM']")
        self.web_controller.wait_until_element_is_present(*ports_rows_details)
        ports_rows = self.web_controller.find_elements(*ports_rows_details)
        for i in range(0, 48, 6):
            ports_settings[f'Port {i // 6 + 1}'] = {
                'Status': ports_rows[i+1].text,
                'Speed/Duplex Config': ports_rows[i+2].text,
                'Speed/Duplex Actual': ports_rows[i+3].text,
                'Flow Control Config': ports_rows[i+4].text,
                'Flow Control Actual': ports_rows[i+5].text,
            }
        return ports_settings

    @ControlField.login_required
    def set_port_settings(self, port: int, status: STATUS, speed: SPEED, flow_control: FLOW_CONTROL) -> None:
        """
        Apply given settings for indicated port.

        :param port: number of port
        :param status: status of port (enable / disable)
        :param speed: speed of port (auto / 10MH / 10MF / 100MH / 100MF / 1000Mf)
        :param flow_control: flow control enabled or disabled (on / off)
        :raises PortIdException: if port ID is invalid
        :raises OptionDisabledException: if given port option is disabled in admin page
        :raises PortSettingsException: if port settings was not applied successfully
        :return: None
        """
        validate_port_id(port)
        port_label = get_port_label(port)
        self.open_tab(self._MENU_SECTION, 'Port Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        port_select_details = (By.XPATH, "//select[@id='portSel']")
        if not self._select_port_setting(*port_select_details, port_label.value):
            raise OptionDisabledException(f'Option {port_label} is disabled.')
        status_select_details = (By.XPATH, "//select[@name='state']")
        if not self._select_port_setting(*status_select_details, status.value):
            raise OptionDisabledException(f'Option {status} is disabled.')
        speed_select_details = (By.XPATH, "//select[@name='speed']")
        if not self._select_port_setting(*speed_select_details, speed.value):
            raise OptionDisabledException(f'Option {speed} is disabled.')
        flow_control_select_details = (By.XPATH, "//select[@name='flowcontrol']")
        if not self._select_port_setting(*flow_control_select_details, flow_control.value):
            raise OptionDisabledException(f'Option {flow_control} is disabled.')
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise PortSettingsException(f'Cannot set "{status}", "{speed}", "{flow_control}" options '
                                        f'for port NO {port} due to unknown error.')
        if alert_info != 'Operation successful.':
            raise PortSettingsException(alert_info)

    @ControlField.login_required
    def igmp_snooping(self) -> Dict[str, str]:
        """
        Returns settings of IGMP settings and Report Message Suppression.

        :return: current settings
        """
        self.open_tab(self._MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        igmp_snooping_settings = {}
        enable_input = self._find_igmp_snooping_input('igmpEn')
        igmp_snooping_settings['IGMP Snooping'] = 'Enable' \
            if enable_input.get_attribute('checked') else 'Disable'
        enable_input = self._find_igmp_snooping_input('reportSuEn')
        igmp_snooping_settings['Report Message Suppression'] = 'Enable' \
            if enable_input.get_attribute('checked') else 'Disable'
        return igmp_snooping_settings

    @ControlField.login_required
    def enable_igmp_snooping(self) -> None:
        """
        Enables IGMP settings.

        :raises IgmpSnoopingSettings: if igmp snooping was not enabled successfully
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        enable_input = self._find_igmp_snooping_input('igmpEn')
        enable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise IgmpSnoopingSettings('Cannot enable igmp snooping due to unknown error.')
        if alert_info != 'Operation successful.':
            raise IgmpSnoopingSettings(alert_info)

    @ControlField.login_required
    def disable_igmp_snooping(self) -> None:
        """
        Disables IGMP settings.

        :raises IgmpSnoopingSettings: if igmp snooping was not disabled successfully
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        disable_input = self._find_igmp_snooping_input('igmpDis')
        disable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise IgmpSnoopingSettings('Cannot disable igmp snooping due to unknown error.')
        if alert_info != 'Operation successful.':
            raise IgmpSnoopingSettings(alert_info)

    @ControlField.login_required
    def enable_report_message_suppression(self) -> None:
        """
        Enables Report Message Suppression.

        :raises ReportMessageSuppressionSettings: if igmp snooping was not enabled successfully
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        enable_input = self._find_igmp_snooping_input('reportSuEn')
        enable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise ReportMessageSuppressionSettings('Cannot enable Report Message Suppression due to unknown error.')
        if alert_info != 'Operation successful.':
            raise ReportMessageSuppressionSettings(alert_info)

    @ControlField.login_required
    def disable_report_message_suppression(self) -> None:
        """
        Disables Report Message Suppression.

        :raises ReportMessageSuppressionSettings: if igmp snooping was not disabled successfully
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        disable_input = self._find_igmp_snooping_input('reportSuDis')
        disable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise ReportMessageSuppressionSettings('Cannot disable Report Message Suppression due to unknown error.')
        if alert_info != 'Operation successful.':
            raise ReportMessageSuppressionSettings(alert_info)

    @ControlField.login_required
    def lag_settings(self) -> Dict[str, str]:
        """
        Returns information about LAG settings.

        :return: current settings
        """
        self.open_tab(self._MENU_SECTION, 'LAG')
        self.web_controller.switch_to_frame(Frame.MAIN)
        lag_settings = {}
        lag_td_details = (
            By.XPATH,
            "//form[@name='port_trunk_display']/table[@class='BORDER']/tbody/tr/td[not(@class='TD_FIRST_COL')]"
        )
        self.web_controller.wait_until_element_is_present(*lag_td_details)
        lag_tds = self.web_controller.find_elements(*lag_td_details)
        for i in range(0, 6, 3):
            lag_settings[lag_tds[i].text] = lag_tds[i+1].text
        return lag_settings

    @ControlField.login_required
    def set_lag_ports(self, lag_id: int, ports: List[int]) -> None:
        """
        Sets given LAG for indicated ports. At least two ports should be passed.
        Mirroring port cannot be a trunk member port. Mirroring and mirrored port cannot be added to a LAG group.

        :param lag_id: id of LAG
        :param ports: list of ports
        :raises LagIdException: if LAG ID is invalid
        :raises PortIdException: if port ID is invalid
        :raises LAGPortException: if user passed incorrect LAG ID or port assignment to LAG group failed
        :return: None
        """
        validate_lag_id(lag_id)
        for port in ports:
            validate_port_id(port)
        if not 2 <= len(ports) <= 4:
            raise LAGPortException('Each LAG group has up to 4 port members and has at least two port members.')
        if lag_id == 1 and not all(map(lambda p: p in [1, 2, 3, 4], ports)):
            raise LAGPortException('Port can not be selected, available ports of LAG 1: port 1 -- port 4')
        if lag_id == 2 and not all(map(lambda p: p in [5, 6, 7, 8], ports)):
            raise LAGPortException('Port can not be selected, available ports of LAG 1: port 5 -- port 8')
        self.open_tab(self._MENU_SECTION, 'LAG')
        self.web_controller.switch_to_frame(Frame.MAIN)
        self._fill_lag_settings_form(lag_id, ports)
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='setapply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise LAGPortException('Cannot add port to LAG group due to unknown error.')
        if alert_info != 'Operation successful.':
            raise LAGPortException(alert_info)

    @ControlField.login_required
    def unset_lag_ports(self, lag_id: int) -> None:
        """
        Delete all ports from given LAG group.

        :param lag_id: id of LAG
        :raises LagIdException: if LAG ID is invalid
        :raises LAGPortException: if deleting LAG group failed
        :return: None
        """
        validate_lag_id(lag_id)
        self.open_tab(self._MENU_SECTION, 'LAG')
        self.web_controller.switch_to_frame(Frame.MAIN)
        lag_label = get_lag_label(lag_id)
        input_checkbox_details = (By.XPATH, f"//input[@name='chk_trunk' and @id='chk{lag_label.value.split()[1]}']")
        self.web_controller.wait_until_element_is_present(*input_checkbox_details)
        input_checkbox = self.web_controller.find_element(*input_checkbox_details)
        input_checkbox.click()
        delete_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='setDelete']")
        self.apply_settings(*delete_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise LAGPortException('Cannot delete LAG group due to unknown error.')
        if alert_info != 'Operation successful.':
            raise LAGPortException(alert_info)

    def _find_igmp_snooping_input(self, input_id: str) -> WebElement:
        input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*input_details)
        return self.web_controller.find_element(*input_details)

    def _select_port_setting(self, method: str, query: str, value: str) -> bool:
        select_details = (method, query)
        self.web_controller.wait_until_element_is_present(*select_details)
        select = Select(self.web_controller.find_element(*select_details))
        try:
            select.select_by_visible_text(value)
        except NotImplementedError:
            return False
        return True

    def _fill_lag_settings_form(self, lag_id: int, ports: List[int]) -> None:
        lag_select_details = (By.XPATH, "//select[@id='trunkSel']")
        self.web_controller.wait_until_element_is_present(*lag_select_details)
        lag_select = Select(self.web_controller.find_element(*lag_select_details))
        lag_label = get_lag_label(lag_id)
        lag_select.select_by_visible_text(lag_label.value)
        port_select_details = (By.XPATH, "//select[@id='portSel']")
        self.web_controller.wait_until_element_is_present(*port_select_details)
        port_select = self.web_controller.find_element(*port_select_details)
        for port in ports:
            port_label = get_port_label(port)
            option_details = (By.XPATH, f"//option[contains(text(),'{port_label.value}')]")
            option = port_select.find_element(*option_details)
            self.web_controller.click_element_with_control_key_pressed(option)
