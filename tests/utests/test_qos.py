import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch, DEFAULT
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.qos import QoSControlField
from switch_TL_SG108PE.exceptions import QoSModeException, PortIdException, QoSPriorityQueueException
from switch_TL_SG108PE.port import PriorityQueue


@ddt
class TestQoS(unittest.TestCase):

    def setUp(self) -> None:
        self.qos = QoSControlField(web_controller=MagicMock())

    def test_qos_mode(self):
        self.assertTrue(self.qos.qos_mode())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': QoSModeException,
            'alert_text': '',
        },
        {
            'error': QoSModeException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(QoSControlField, 'get_alert_text')
    def test_set_port_base_qos_mode(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.qos.set_port_base_qos_mode()
        else:
            self.assertRaises(error, lambda: self.qos.set_port_base_qos_mode())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': QoSModeException,
            'alert_text': '',
        },
        {
            'error': QoSModeException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(QoSControlField, 'get_alert_text')
    def test_set_802_1p_based_qos_mode(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.qos.set_802_1p_based_qos_mode()
        else:
            self.assertRaises(error, lambda: self.qos.set_802_1p_based_qos_mode())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': QoSModeException,
            'alert_text': '',
        },
        {
            'error': QoSModeException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(QoSControlField, 'get_alert_text')
    def test_set_dscp_802_1p_based_qos_mode(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.qos.set_dscp_802_1p_based_qos_mode()
        else:
            self.assertRaises(error, lambda: self.qos.set_dscp_802_1p_based_qos_mode())

    @data(
        {
            'error': None,
            'qos_mode_value': 'Port Based'
        },
        {
            'error': QoSModeException,
            'qos_mode_value': 'sth-other'
        },
    )
    @unpack
    @patch.object(QoSControlField, 'qos_mode')
    def test_priority_queue_port_settings(self, qos_mode, qos_mode_value, error):
        qos_mode.return_value = qos_mode_value
        if error is None:
            settings = self.qos.priority_queue_port_settings()
            self.assertTrue(settings.keys())
        else:
            self.assertRaises(error, lambda: self.qos.priority_queue_port_settings())

    @data(
        {
            'port': 1,
            'priority_queue': PriorityQueue.LOWEST_1,
            'error': None,
            'alert_text': 'Operation successful.',
            'qos_mode_value': 'Port Based'
        },
        {
            'port': -1,
            'priority_queue': PriorityQueue.HIGHEST_4,
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            'qos_mode_value': 'Port Based'
        },
        {
            'port': 2,
            'priority_queue': PriorityQueue.HIGHEST_4,
            'error': QoSModeException,
            'alert_text': 'Operation successful.',
            'qos_mode_value': 'sth-other'
        },
        {
            'port': 2,
            'priority_queue': PriorityQueue.LOWEST_1,
            'error': QoSPriorityQueueException,
            'alert_text': '',
            'qos_mode_value': 'Port Based'
        },
        {
            'port': 3,
            'priority_queue': PriorityQueue.LOWEST_1,
            'error': QoSPriorityQueueException,
            'alert_text': 'sth-other',
            'qos_mode_value': 'Port Based'
        },
    )
    @unpack
    @patch.multiple(QoSControlField,
                    get_alert_text=DEFAULT,
                    qos_mode=DEFAULT)
    @patch('switch_TL_SG108PE.control_fields.qos.Select', Mock())
    def test_set_priority_queue_in_port_based_qos_mode(self, get_alert_text, qos_mode, port, priority_queue,
                                                       alert_text, error, qos_mode_value):
        get_alert_text.return_value = alert_text
        qos_mode.return_value = qos_mode_value
        if error is None:
            self.qos.set_priority_queue_in_port_based_qos_mode(port, priority_queue)
        else:
            self.assertRaises(error, lambda: self.qos.set_priority_queue_in_port_based_qos_mode(port, priority_queue))
