"""Contains code to manage QoS section from menu tab."""

from typing import Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from .control_field import ControlField
from ..utils import Frame, validate_port_id
from ..port import PriorityQueue
from ..exceptions import QoSModeException, QoSPriorityQueueException


class QoSControlField(ControlField):
    """Creates object to control QoS settings on switch."""

    _MENU_SECTION = 'QoS'

    @ControlField.login_required
    def qos_mode(self) -> str:
        """
        Returns enabled QoS mode.

        :raise QoSModeException: if qos mode cannot be read
        :return: mode as string ('Port Based' or '802.1P Based' or 'DSCP/802.1P Based')
        """
        self.open_tab(self._MENU_SECTION, 'QoS Basic')
        self.web_controller.switch_to_frame(Frame.MAIN)
        input_ids = ['rd_portbase', 'rd_8021pbase', 'rx_dscp']
        for iid in input_ids:
            mode_input = self._find_qos_mode_input(iid)
            if mode_input.is_selected():
                td_details = (By.XPATH, '..')
                td_element = mode_input.find_element(*td_details)
                return td_element.text.strip()
        raise QoSModeException('Cannot get QoS mode.')

    @ControlField.login_required
    def set_port_base_qos_mode(self) -> None:
        """
        Sets Port Based QoS mode.

        :raise QoSModeException: if mode cannot be set
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'QoS Basic')
        self.web_controller.switch_to_frame(Frame.MAIN)
        self._select_and_apply_qos_mode('rd_portbase')
        alert_info = self.get_alert_text()
        if not alert_info:
            raise QoSModeException('Cannot activate Port Based	QoS mode due to unknown error.')
        if alert_info != 'Operation successful.':
            raise QoSModeException(alert_info)

    @ControlField.login_required
    def set_802_1p_based_qos_mode(self) -> None:
        """
        Sets 802.1P Based QoS mode.

        :raise QoSModeException: if mode cannot be set
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'QoS Basic')
        self.web_controller.switch_to_frame(Frame.MAIN)
        self._select_and_apply_qos_mode('rd_8021pbase')
        alert_info = self.get_alert_text()
        if not alert_info:
            raise QoSModeException('Cannot activate 802.1P Based QoS mode due to unknown error.')
        if alert_info != 'Operation successful.':
            raise QoSModeException(alert_info)

    @ControlField.login_required
    def set_dscp_802_1p_based_qos_mode(self) -> None:
        """
        Sets DSCP/802.1P Based QoS mode.

        :raise QoSModeException: if mode cannot be set
        :return: None
        """
        self.open_tab(self._MENU_SECTION, 'QoS Basic')
        self.web_controller.switch_to_frame(Frame.MAIN)
        self._select_and_apply_qos_mode('rx_dscp')
        alert_info = self.get_alert_text()
        if not alert_info:
            raise QoSModeException('Cannot activate DSCP/802.1P Based mode due to unknown error.')
        if alert_info != 'Operation successful.':
            raise QoSModeException(alert_info)

    @ControlField.login_required
    def priority_queue_port_settings(self) -> Dict[str, str]:
        """
        Return settings of port priorities in Port Base QoS mode.
        :raises QoSModeException: if QoS mode is not set to Port Base
        :return: port settings
        """
        mode = self.qos_mode()
        if mode != 'Port Based':
            raise QoSModeException(
                'Priority Queue settings can be read only in Port Base QoS mode. Enable this mode first.')
        settings = {}
        tds_details = (By.XPATH, "//form[@name='qos_port_priority_set']/table/tbody/tr[not(@class='TABLE_HEAD')]/td")
        self.web_controller.wait_until_element_is_present(*tds_details)
        tds = self.web_controller.find_elements(*tds_details)
        tds = tds[1:]
        for i in range(0, 24, 3):
            settings[tds[i].text] = tds[i+1].text
        return settings

    @ControlField.login_required
    def set_priority_queue_in_port_based_qos_mode(self, port: int, priority_queue: PriorityQueue) -> None:
        """
        Set given priority for passed port.
        :param port: port ID
        :param priority_queue: 	the port priorities
        :raises QoSModeException: if QoS mode is not set to Port Base
        :raises QoSPriorityQueueException: if port priority cannot be set
        :return: None
        """
        mode = self.qos_mode()
        if mode != 'Port Based':
            raise QoSModeException('Priority Queue can be set only in Port Base QoS mode. Enable this mode first.')
        validate_port_id(port)
        select_port_details = (By.XPATH, f"//td/input[@id='sel_{port}']")
        self.web_controller.wait_until_element_is_present(*select_port_details)
        select_port = self.web_controller.find_element(*select_port_details)
        select_port.click()
        priority_queue_details = (By.XPATH, "//tr[@class='TABLE_HEAD']/td/select[@name='port_queue']")
        self.web_controller.wait_until_element_is_present(*priority_queue_details)
        priority_queue_select = Select(self.web_controller.find_element(*priority_queue_details))
        priority_queue_select.select_by_visible_text(priority_queue.value)
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='apply']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)
        alert_info = self.get_alert_text()
        if not alert_info:
            raise QoSPriorityQueueException(f'Cannot set Priority Queue for {port} port due to unknown error.')
        if alert_info != 'Operation successful.':
            raise QoSPriorityQueueException(alert_info)

    def _select_and_apply_qos_mode(self, qos_input_id: str) -> None:
        mode_input = self._find_qos_mode_input(qos_input_id)
        mode_input.click()
        apply_button_details = (By.XPATH, "//a[@class='BTN']/input[@name='qosmode']")
        self.apply_settings(*apply_button_details, wait_for_confirmation_alert=False)

    def _find_qos_mode_input(self, qos_input_id: str) -> WebElement:
        input_details = (By.XPATH, f"//td/input[@id='{qos_input_id}']")
        self.web_controller.wait_until_element_is_present(*input_details)
        mode_input = self.web_controller.find_element(*input_details)
        return mode_input
