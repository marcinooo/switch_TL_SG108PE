import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.monitoring import MonitoringControlField
from switch_TL_SG108PE.port.settings import NO


@ddt
class TestMonitoring(unittest.TestCase):

    def setUp(self) -> None:
        self.monitoring = MonitoringControlField(web_controller=MagicMock())

    def test_port_statistics(self):
        port_statistics = self.monitoring.port_statistics()
        self.assertEqual(len(port_statistics.keys()), 8)
        for value in port_statistics.values():
            self.assertEqual(len(value.keys()), 6)

    def test_refresh_port_statistics(self):
        self.assertTrue(self.monitoring.refresh_port_statistics())

    def test_mirrored_ports(self):
        status = self.monitoring.mirrored_ports()
        self.assertEqual(len(status['Mirrored Ports'].keys()), 8)
        for value in status['Mirrored Ports'].values():
            self.assertEqual(len(value.keys()), 2)

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_mirroring_port(self):
        self.assertIsNotNone(self.monitoring.mirroring_port().get('Mirroring Port'))

    @data(
        {
            'mirrored_ports': [NO.PORT_8],
            'mirroring_port': NO.PORT_1
        },
        {
            'mirrored_ports': [NO.PORT_2, NO.PORT_3],
            'mirroring_port': NO.PORT_1
        },
        {
            'mirrored_ports': [],
            'mirroring_port': NO.PORT_1
        }
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_enable_port_mirroring(self, mirrored_ports, mirroring_port):
        self.assertTrue(self.monitoring.enable_port_mirroring(mirrored_ports, mirroring_port))

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_loop_prevention(self):
        self.assertTrue(self.monitoring.loop_prevention())

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_enable_loop_prevention(self):
        self.assertTrue(self.monitoring.enable_loop_prevention())

    @patch('switch_TL_SG108PE.control_fields.monitoring.Select', Mock())
    def test_disable_loop_prevention(self):
        self.assertTrue(self.monitoring.disable_loop_prevention())
