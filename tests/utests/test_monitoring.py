import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.monitoring import MonitoringControlField
from switch_TL_SG108PE.exceptions import PortIdError

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

    def test_refresh_port_statistics(self):
        self.assertTrue(self.monitoring.refresh_port_statistics())

    def test_mirrored_ports(self):
        status = self.monitoring.mirrored_ports()
        self.assertEqual(len(status['Mirrored Ports'].keys()), 8)
        for value in status['Mirrored Ports'].values():
            self.assertIsNotNone(value.get('Ingress'))
            self.assertIsNotNone(value.get('Egress'))

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_mirroring_port(self):
        status = self.monitoring.mirroring_port()
        self.assertIsNotNone(status.get('Mirroring Port'))

    @data(
        {
            'mirrored_ports': [8],
            'mirroring_port': 1,
            'error': None,
        },
        {
            'mirrored_ports': [2, 3],
            'mirroring_port': 5,
            'error': None,
        },
        {
            'mirrored_ports': [],
            'mirroring_port': 6,
            'error': None,
        },
        {
            'mirrored_ports': ['1'],
            'mirroring_port': 3,
            'error': PortIdError,
        },
        {
            'mirrored_ports': [0],
            'mirroring_port': 1,
            'error': PortIdError,
        },
        {
            'mirrored_ports': [1],
            'mirroring_port': '4',
            'error': PortIdError,
        },
        {
            'mirrored_ports': [1],
            'mirroring_port': 9,
            'error': PortIdError,
        }
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_enable_port_mirroring(self, mirrored_ports, mirroring_port, error):
        if error is None:
            self.assertTrue(self.monitoring.enable_port_mirroring(mirrored_ports, mirroring_port))
        else:
            self.assertRaises(
                error,
                lambda: self.monitoring.enable_port_mirroring(mirrored_ports, mirroring_port)
            )

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_loop_prevention(self):
        status = self.monitoring.loop_prevention()
        self.assertIsNotNone(status.get('Loop Prevention'))

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_enable_loop_prevention(self):
        self.assertTrue(self.monitoring.enable_loop_prevention())

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_disable_loop_prevention(self):
        self.assertTrue(self.monitoring.disable_loop_prevention())
