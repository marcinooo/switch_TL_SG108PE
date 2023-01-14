import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.switching import SwitchingControlField
from switch_TL_SG108PE.port import STATUS, SPEED, FLOW_CONTROL


class TestSwitching(unittest.TestCase):

    def setUp(self) -> None:
        self.switching = SwitchingControlField(web_controller=MagicMock())

    def test_ports_settings(self):
        ports_settings = self.switching.ports_settings()
        self.assertEqual(len(ports_settings.keys()), 8)
        for value in ports_settings.values():
            self.assertEqual(len(value.keys()), 5)

    @patch('switch_TL_SG108PE.control_fields.switching.Select', Mock())
    def test_set_port_settings(self):
        status = self.switching.set_port_settings(port=1, status=STATUS.ENABLE, speed=SPEED.AUTO,
                                                  flow_control=FLOW_CONTROL.OFF)
        self.assertTrue(status)

    def test_igmp_snooping(self):
        igmp_snooping = self.switching.igmp_snooping()
        self.assertIsNotNone(igmp_snooping.get('IGMP Snooping'))
        self.assertIsNotNone(igmp_snooping.get('Report Message Suppression'))

    def test_enable_igmp_snooping(self):
        self.assertTrue(self.switching.enable_igmp_snooping())

    def test_disable_igmp_snooping(self):
        self.assertTrue(self.switching.disable_igmp_snooping())

    def test_enable_report_message_suppression(self):
        self.assertTrue(self.switching.enable_report_message_suppression())

    def test_disable_report_message_suppression(self):
        self.assertTrue(self.switching.disable_report_message_suppression())

    def test_lag_settings(self):
        self.assertTrue(self.switching.lag_settings())  # TODO: Consider better checking

    @patch('switch_TL_SG108PE.control_fields.switching.Select', Mock())
    def test_set_lag_ports(self):
        self.assertTrue(self.switching.set_lag_ports(1, [1, 2]))

    def test_unset_lag_ports(self):
        self.assertTrue(self.switching.unset_lag_ports(1))
