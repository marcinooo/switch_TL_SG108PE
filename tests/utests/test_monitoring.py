import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.monitoring import MonitoringControlField
from switch_TL_SG108PE.exceptions import (PortIdException, MirroringPortException, MirroredPortException,
                                          LoopPreventionException)

@ddt
class TestMonitoring(unittest.TestCase):

    def setUp(self) -> None:
        self.monitoring = MonitoringControlField(web_controller=MagicMock())

    def test_port_statistics(self):
        port_statistics = self.monitoring.port_statistics()
        self.assertEqual(len(port_statistics.keys()), 8)
        for value in port_statistics.values():
            self.assertIsNotNone(value.get('Status'))
            self.assertIsNotNone(value.get('Link Status'))
            self.assertIsNotNone(value.get('TxGoodPkt'))
            self.assertIsNotNone(value.get('TxBadPkt'))
            self.assertIsNotNone(value.get('RxGoodPkt'))
            self.assertIsNotNone(value.get('RxBadPkt'))

    def test_mirrored_ports(self):
        status = self.monitoring.mirrored_ports()
        self.assertEqual(len(status['Mirrored Ports'].keys()), 8)
        for value in status['Mirrored Ports'].values():
            self.assertIsNotNone(value.get('Ingress'))
            self.assertIsNotNone(value.get('Egress'))

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', MagicMock())
    def test_mirroring_port(self):
        status = self.monitoring.mirroring_port()
        self.assertIsNotNone(status.get('Mirroring Port'))
        self.assertTrue(status['Mirroring Port'])

    @data(
        {
            'mirrored_ports': [8],
            'mirroring_port': 1,
            'error': None,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [2, 3],
            'mirroring_port': 5,
            'error': None,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [],
            'mirroring_port': 6,
            'error': None,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [1, 2],
            'mirroring_port': 7,
            'error': MirroringPortException,
            'alert_text': '',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [3, 4],
            'mirroring_port': 8,
            'error': MirroringPortException,
            'alert_text': 'sth-other',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [1, 2],
            'mirroring_port': 7,
            'error': MirroredPortException,
            'alert_text': '',
            '_select_mirroring_port_method_mock': MagicMock()
        },
        {
            'mirrored_ports': [3, 4],
            'mirroring_port': 8,
            'error': MirroredPortException,
            'alert_text': 'sth-other',
            '_select_mirroring_port_method_mock': MagicMock()
        },
        {
            'mirrored_ports': ['1'],
            'mirroring_port': 3,
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [0],
            'mirroring_port': 1,
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [1],
            'mirroring_port': '4',
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        },
        {
            'mirrored_ports': [1],
            'mirroring_port': 9,
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            '_select_mirroring_port_method_mock': None
        }
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    @patch.object(MonitoringControlField, 'get_alert_text')
    def test_enable_port_mirroring(self, get_alert_text, mirrored_ports, mirroring_port, error, alert_text,
                                   _select_mirroring_port_method_mock):
        if _select_mirroring_port_method_mock is not None:
            MonitoringControlField._select_mirroring_port = _select_mirroring_port_method_mock
        get_alert_text.return_value = alert_text
        if error is None:
            self.monitoring.enable_port_mirroring(mirrored_ports, mirroring_port)
        else:
            self.assertRaises(
                error,
                lambda: self.monitoring.enable_port_mirroring(mirrored_ports, mirroring_port)
            )

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_loop_prevention(self):
        status = self.monitoring.loop_prevention()
        self.assertIsNotNone(status.get('Loop Prevention'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': LoopPreventionException,
            'alert_text': '',
        },
        {
            'error': LoopPreventionException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    @patch.object(MonitoringControlField, 'get_alert_text')
    def test_enable_loop_prevention(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.monitoring.enable_loop_prevention()
        else:
            self.assertRaises(error, lambda: self.monitoring.enable_loop_prevention())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': LoopPreventionException,
            'alert_text': '',
        },
        {
            'error': LoopPreventionException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    @patch.object(MonitoringControlField, 'get_alert_text')
    def test_disable_loop_prevention(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.monitoring.disable_loop_prevention()
        else:
            self.assertRaises(error, lambda: self.monitoring.disable_loop_prevention())
