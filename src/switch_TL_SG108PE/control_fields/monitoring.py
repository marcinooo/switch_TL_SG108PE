"""Contains code to manage monitoring section from menu tab."""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from .control_field import ControlField
from ..utils import Frame, get_port_label, validate_port_id
from ..exceptions import PortIsNotAvailableError


class MonitoringControlField(ControlField):
    """Creates object to control monitoring settings on switch."""

    MENU_SECTION = 'Monitoring'

    @ControlField.login_required
    def port_statistics(self, refresh: bool = True) -> dict[str, dict[str, str]]:
        """
        Displays the traffic information of each port,
        which facilitates you to monitor the traffic and analyze the network abnormity.
        :param refresh: indicates if statistics should be refreshed before requesting
        :return: statistics information
        """
        self.open_tab(self.MENU_SECTION, 'Port Statistics')
        self.web_controller.switch_to_frame(Frame.MAIN)
        if refresh:
            self.refresh_port_statistics()
        port_statistics = {}
        ports_rows_details = (
            By.XPATH, "//table[@class='BORDER']/tbody/tr[not(@class='TD_FIRST_ROW')]/td[@class='TABLE_HEAD_BOTTOM']"
        )
        self.web_controller.wait_until_element_is_present(*ports_rows_details)
        ports_rows = self.web_controller.find_elements(*ports_rows_details)
        for i in range(0, 56, 7):
            port_statistics[f'Port {i // 7 + 1}'] = {
                'Status': ports_rows[i+1].text,
                'Link Status': ports_rows[i+2].text,
                'TxGoodPkt': ports_rows[i+3].text,
                'TxBadPkt': ports_rows[i+4].text,
                'RxGoodPkt': ports_rows[i+5].text,
                'RxBadPkt': ports_rows[i+5].text,
            }
        return port_statistics

    @ControlField.login_required
    def refresh_port_statistics(self) -> bool:
        """
        Refreshes statistics of ports.
        :return: True
        """
        self.open_tab(self.MENU_SECTION, 'Port Statistics')
        self.web_controller.switch_to_frame(Frame.MAIN)
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='refresh']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return True

    @ControlField.login_required
    def mirrored_ports(self) -> dict[str, dict[str, str]]:
        """
        Returns information about enabling of ingress and egress feature for each mirrored port.
        :return: information of mirrored ports
        """
        self.open_tab(self.MENU_SECTION, 'Port Mirror')
        self.web_controller.switch_to_frame(Frame.MAIN)
        mirrored_ports = {'Mirrored Ports': {}}
        tds_mirrored_port_details = (By.XPATH, "//form[@name='mirrored_port_set']//table[@class='BORDER']//td")
        self.web_controller.wait_until_element_is_present(*tds_mirrored_port_details)
        tds_mirrored_port = self.web_controller.find_elements(*tds_mirrored_port_details)
        tds_mirrored_port = tds_mirrored_port[9:]
        for i in range(0, 24, 3):
            mirrored_ports['Mirrored Ports'][f'Port {i // 3 + 1}'] = {
                'Ingress': tds_mirrored_port[i+1].text,
                'Egress': tds_mirrored_port[i+2].text
            }
        return mirrored_ports

    @ControlField.login_required
    def mirroring_port(self) -> dict[str, str]:
        """
        Returns information about mirroring port. If mirroring port is not enabled it returns empty value.
        :return: information of mirroring ports
        """
        self.open_tab(self.MENU_SECTION, 'Port Mirror')
        self.web_controller.switch_to_frame(Frame.MAIN)
        select_mirroring_port_details = (By.XPATH, "//form[@name='mirror_enabled_set']//select[@name='mirroringport']")
        self.web_controller.wait_until_element_is_present(*select_mirroring_port_details)
        select_state = Select(self.web_controller.find_element(*select_mirroring_port_details))
        try:
            return {'Mirroring Port': select_state.first_selected_option.text}
        except NoSuchElementException:
            return {'Mirroring Port': ''}

    @ControlField.login_required
    def enable_port_mirroring(self, mirrored_ports: List[int], mirroring_port: int, ingress: bool = True,
                              egress: bool = True) -> bool:
        """
        Enables port mirroring for given port combination. It duplicates the datagram transmitted through
        Mirrored Ports to Mirroring Port.
        :param mirrored_ports: ports which will be source of datagrams (observed ports)
        :param mirroring_port: port where datagrams will be passed (destination port)
        :param ingress: if True, traffic entering the port will be monitored
        :param egress: if True, outgoing traffic the port will be monitored
        :return: True if mirroring was successfully set, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'Port Mirror')
        self.web_controller.switch_to_frame(Frame.MAIN)
        validate_port_id(mirroring_port)
        for port in mirrored_ports:
            validate_port_id(port)
        if not self._select_mirroring_port(mirroring_port):
            return False
        if not self._select_mirrored_port(mirrored_ports, ingress, egress):
            return False
        return True

    @ControlField.login_required
    def disable_port_mirroring(self) -> bool:
        """
        Disables port mirroring.
        :return: True if port mirroring was deleted successfully, otherwise False
        """
        self.open_tab(self.MENU_SECTION, 'Port Mirror')
        self.web_controller.switch_to_frame(Frame.MAIN)
        self._manage_status_of_mirroring_port('Disable')
        apply_mirroring_port_button_details = (By.XPATH, "//table/tbody/tr/td/a/input[@name='mirrorenable']")
        self.apply_settings(*apply_mirroring_port_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    @ControlField.login_required
    def loop_prevention(self) -> dict[str, str]:
        """
        Returns status of enabling loop prevention.
        :return: info about loop prevention (Enable / Disable)
        """
        self.open_tab(self.MENU_SECTION, 'Loop Prevention')
        self.web_controller.switch_to_frame(Frame.MAIN)
        select_loop_prevention = self._get_loop_prevention_select()
        return {'Loop Prevention': select_loop_prevention.first_selected_option.text.strip()}

    @ControlField.login_required
    def enable_loop_prevention(self) -> bool:
        """
        Enables loop prevention.
        :return: True if loop prevention was enabled successfully, otherwise False
        """
        return self._select_loop_prevention('Enable')

    @ControlField.login_required
    def disable_loop_prevention(self) -> bool:
        """
        Disables loop prevention.
        :return: True if loop prevention was disabled successfully, otherwise False
        """
        return self._select_loop_prevention('Disable')

    def _select_loop_prevention(self, action: str = 'Enable') -> bool:
        self.open_tab(self.MENU_SECTION, 'Loop Prevention')
        self.web_controller.switch_to_frame(Frame.MAIN)
        select_loop_prevention = self._get_loop_prevention_select()
        option_value = dict(Enable='1', Disable='0').get(action)
        select_loop_prevention.select_by_value(option_value)
        apply_button_details = (By.XPATH, "//td[@class='BTN_WRAPPER']/a/input[@name='apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    def _get_loop_prevention_select(self) -> Select:
        select_loop_prevention_details = (By.XPATH, "//select[@id='lpState']")
        self.web_controller.wait_until_element_is_present(*select_loop_prevention_details)
        select_loop_prevention = Select(self.web_controller.find_element(*select_loop_prevention_details))
        return select_loop_prevention

    def _select_mirroring_port(self, mirroring_port: int) -> bool:
        mirroring_port_label = get_port_label(mirroring_port)
        self._manage_status_of_mirroring_port('Enable')
        select_mirroring_port_details = (By.XPATH, "//form[@name='mirror_enabled_set']//select[@name='mirroringport']")
        self.web_controller.wait_until_element_is_present(*select_mirroring_port_details)
        select_state_element = self.web_controller.find_element(*select_mirroring_port_details)
        state_option_details = (By.XPATH, f"//option[contains(text(), '{mirroring_port_label.value}')]")
        state_option = select_state_element.find_element(*state_option_details)
        if not state_option.is_enabled():
            raise PortIsNotAvailableError(f'"{mirroring_port_label.value}" is not available to set as Mirroring Port.')
        state_option.click()
        apply_mirroring_port_button_details = (By.XPATH, "//table/tbody/tr/td/a/input[@name='mirrorenable']")
        self.apply_settings(*apply_mirroring_port_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()

    def _manage_status_of_mirroring_port(self, action: str) -> None:
        option_value = dict(Enable='1', Disable='0').get(action)
        select_state_details = (By.XPATH, "//form[@name='mirror_enabled_set']//select[@name='state']")
        self.web_controller.wait_until_element_is_present(*select_state_details)
        select_state = Select(self.web_controller.find_element(*select_state_details))
        select_state.select_by_value(option_value)

    def _select_mirrored_port(self, mirrored_ports: List[int], ingress: bool = True, egress: bool = True) -> bool:
        select_port_details = (By.XPATH, "//table[@class='BORDER']/tbody/tr/td/select[@id='portSel']")
        self.web_controller.wait_until_element_is_present(*select_port_details)
        select_port_element = self.web_controller.find_element(*select_port_details)
        for port in mirrored_ports:
            port_label = get_port_label(port)
            port_option_details = (By.XPATH, f"//select[@id='portSel']//option[contains(text(), '{port_label.value}')]")
            port_option = select_port_element.find_element(*port_option_details)
            if not port_option.is_enabled():
                raise PortIsNotAvailableError(f'"{port_label.value}" is not available to set as Mirrored Port.')
            self.web_controller.click_element_with_control_key_pressed(port_option)
        select_ingress_details = (By.XPATH, "//table[@class='BORDER']/tbody/tr/td/select[@name='ingressState']")
        self.web_controller.wait_until_element_is_present(*select_ingress_details)
        select_ingress = Select(self.web_controller.find_element(*select_ingress_details))
        select_ingress.select_by_value('1' if ingress else '0')
        select_egress_details = (By.XPATH, "//table[@class='BORDER']/tbody/tr/td/select[@name='egressState']")
        self.web_controller.wait_until_element_is_present(*select_egress_details)
        select_egress = Select(self.web_controller.find_element(*select_egress_details))
        select_egress.select_by_value('1' if egress else '0')
        apply_mirrored_port_button_details = (By.XPATH, "//table/tbody/tr/td/a/input[@name='mirrored_submit']")
        self.apply_settings(*apply_mirrored_port_button_details, wait_for_confirmation_alert=False)
        return self.wait_for_success_alert()
