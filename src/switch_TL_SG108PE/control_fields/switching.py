"""Contains code to manage given section from menu tab."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from switch_TL_SG108PE.control_fields.control_field import ControlField
from switch_TL_SG108PE.utils import Frame
from switch_TL_SG108PE.port import settings
from switch_TL_SG108PE.errors import LAGPortError


class SwitchingControlField(ControlField):
    """Creates object to control switching settings on switch."""

    MENU_SECTION = 'Switching'

    @ControlField.require_login
    def ports_settings(self) -> dict[str, dict[str, str]]:
        """
        Returns settings of all ports.
        :return: settings
        """
        self.open_tab(self.MENU_SECTION, 'Port Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        ports_settings = {}
        ports_rows_details = (By.XPATH, f"//table[@class='BORDER']/tbody/tr/td[@class='TABLE_HEAD_BOTTOM']")
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

    def set_port_settings(self, port_number: settings.NO, status: settings.STATUS, speed: settings.SPEED,
                          flow_control: settings.FLOW_CONTROL) -> bool:
        """
        Apply given settings for indicated port.
        :param port_number: number of port
        :param status: status of port (enable / disable)
        :param speed: speed of port (auto / 10MH / 10MF / 100MH / 100MF / 1000Mf)
        :param flow_control: flow control enabled or disabled (on / off)
        :return: True if port settings was applied successfully, otherwise False
        """
        if not isinstance(port_number, settings.NO):
            raise TypeError(f'port_number argument must be an instance of switch_TL_SG108PE.port.settings.NO')
        self.open_tab(self.MENU_SECTION, 'Port Setting')
        self.web_controller.switch_to_frame(Frame.MAIN)
        port_select_details = (By.XPATH, "//select[@id='portSel']")
        self.web_controller.wait_until_element_is_present(*port_select_details)
        port_select = Select(self.web_controller.find_element(*port_select_details))
        port_select.select_by_visible_text(port_number.value)
        status_select_details = (By.XPATH, "//select[@name='state']")
        self.web_controller.wait_until_element_is_present(*status_select_details)
        status_select = Select(self.web_controller.find_element(*status_select_details))
        status_select.select_by_visible_text(status.value)
        speed_select_details = (By.XPATH, "//select[@name='speed']")
        self.web_controller.wait_until_element_is_present(*speed_select_details)
        speed_select = Select(self.web_controller.find_element(*speed_select_details))
        speed_select.select_by_visible_text(speed.value)
        flow_control_select_details = (By.XPATH, "//select[@name='flowcontrol']")
        self.web_controller.wait_until_element_is_present(*flow_control_select_details)
        flow_control_select = Select(self.web_controller.find_element(*flow_control_select_details))
        flow_control_select.select_by_visible_text(flow_control.value)
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.require_login
    def igmp_snooping(self) -> dict[str, str]:
        """
        Returns settings of IGMP settings and Report Message Suppression.
        :return: current settings
        """
        self.open_tab(self.MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        igmp_snooping_settings = {}
        enable_input = self._find_igmp_snooping_input('igmpEn')
        igmp_snooping_settings['IGMP Snooping'] = 'Enable' \
            if enable_input.get_attribute('checked') else 'Disable'
        enable_input = self._find_igmp_snooping_input('reportSuEn')
        igmp_snooping_settings['Report Message Suppression'] = 'Enable' \
            if enable_input.get_attribute('checked') else 'Disable'
        return igmp_snooping_settings

    @ControlField.require_login
    def enable_igmp_snooping(self) -> bool:
        """
        Enables IGMP settings.
        :return: True if IGMP settings was enabled successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        enable_input = self._find_igmp_snooping_input('igmpEn')
        enable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.require_login
    def disable_igmp_snooping(self) -> bool:
        """
        Disables IGMP settings.
        :return: True if IGMP settings was disabled successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        disable_input = self._find_igmp_snooping_input('igmpDis')
        disable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.require_login
    def enable_report_message_suppression(self) -> bool:
        """
        Enables Report Message Suppression.
        :return: True if Report Message Suppression was enabled successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        enable_input = self._find_igmp_snooping_input('reportSuEn')
        enable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.require_login
    def disable_report_message_suppression(self) -> bool:
        """
        Disables Report Message Suppression.
        :return: True if Report Message Suppression was disabled successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'IGMP Snooping')
        self.web_controller.switch_to_frame(Frame.MAIN)
        disable_input = self._find_igmp_snooping_input('reportSuDis')
        disable_input.click()
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='Apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.require_login
    def lag_settings(self):
        """
        Returns information about LAG settings.
        :return: current settings
        """
        self.open_tab(self.MENU_SECTION, 'LAG')
        self.web_controller.switch_to_frame(Frame.MAIN)
        lag_settings = {}
        lag_td_details = (
            By.XPATH,
            f"//form[@name='port_trunk_display']/table[@class='BORDER']/tbody/tr/td[not(@class='TD_FIRST_COL')]"
        )
        self.web_controller.wait_until_element_is_present(*lag_td_details)
        lag_tds = self.web_controller.find_elements(*lag_td_details)
        for i in range(0, 6, 3):
            lag_settings[lag_tds[i].text] = lag_tds[i+1].text
        return lag_settings

    @ControlField.require_login
    def set_lag_ports(self, group_id, *ports):
        """
        Sets given LAG for indicated ports. At least two ports should be passed.
        :param group_id: id of LAG
        :param ports: list of ports
        :return: True if ports were added to LAG group successfully, otherwise False
        """
        if len(ports) < 2:
            # TODO: Add webdriver quite
            raise LAGPortError('At least two ports should be added.')
        self.open_tab(self.MENU_SECTION, 'LAG')
        self.web_controller.switch_to_frame(Frame.MAIN)
        lag_select_details = (By.XPATH, "//select[@id='trunkSel']")
        self.web_controller.wait_until_element_is_present(*lag_select_details)
        lag_select = Select(self.web_controller.find_element(*lag_select_details))
        lag_select.select_by_visible_text(group_id.value)
        port_select_details = (By.XPATH, "//select[@id='portSel']")
        self.web_controller.wait_until_element_is_present(*port_select_details)
        port_select = self.web_controller.find_element(*port_select_details)
        for port in ports:
            option_details = (By.XPATH, f"//option[contains(text(),'{port.value}')]")
            option = port_select.find_element(*option_details)
            self.web_controller.click_element_with_control_key_pressed(option)
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='setapply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.require_login
    def unset_lag_ports(self, group_id):
        """
        Delete all ports from given LAG group.
        :param group_id: id of LAG
        :return: True if ports were deleted successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'LAG')
        self.web_controller.switch_to_frame(Frame.MAIN)
        input_checkbox_details = (By.XPATH, f"//input[@name='chk_trunk' and @id='chk{group_id.value.split()[1]}']")
        self.web_controller.wait_until_element_is_present(*input_checkbox_details)
        input_checkbox = self.web_controller.find_element(*input_checkbox_details)
        input_checkbox.click()
        delete_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='setDelete']")
        self.apply_settings(*delete_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    def _find_igmp_snooping_input(self, input_id):
        input_details = (By.XPATH, f"//input[@id='{input_id}']")
        self.web_controller.wait_until_element_is_present(*input_details)
        return self.web_controller.find_element(*input_details)


