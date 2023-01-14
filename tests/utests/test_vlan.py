import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.vlan import VLANControlField
from switch_TL_SG108PE.exceptions import WrongNumberOfPortsException, VlanIdException, PortIdException


@ddt
class TestVLAN(unittest.TestCase):

    def setUp(self) -> None:
        self.vlan = VLANControlField(web_controller=MagicMock())

    def test_mtu_vlan_configuration(self):
        mtu_vlan_configuration = self.vlan.mtu_vlan_configuration()
        self.assertIsNotNone(mtu_vlan_configuration.get('MTU VLAN Configuration'))
        self.assertIsNotNone(mtu_vlan_configuration.get('Current Uplink Port'))

    def test_enable_mtu_vlan_configuration(self):
        self.assertTrue(self.vlan.enable_mtu_vlan_configuration())

    def test_disable_mtu_vlan_configuration(self):
        self.assertTrue(self.vlan.disable_mtu_vlan_configuration())

    @data(
        {'port_id': 1, 'error': None},
        {'port_id': 9, 'error': PortIdException},
        {'port_id': 0, 'error': PortIdException},
        {'port_id': '3', 'error': PortIdException}
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.vlan.Select', Mock())
    def test_change_mtu_vlan_uplink_port(self, port_id, error):
        if error is None:
            self.assertTrue(self.vlan.change_mtu_vlan_uplink_port(port_id))
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.change_mtu_vlan_uplink_port(port_id)
            )

    def test_port_based_vlan_configuration(self):
        port_based_vlan_configuration = self.vlan.port_based_vlan_configuration()
        self.assertIsNotNone(port_based_vlan_configuration.get('Port Based VLAN Configuration'))
        self.assertIsNotNone(port_based_vlan_configuration.get('VLANs'))

    def test_enable_port_based_vlan_configuration(self):
        self.assertTrue(self.vlan.enable_port_based_vlan_configuration())

    def test_disable_port_based_vlan_configuration(self):
        self.assertTrue(self.vlan.disable_port_based_vlan_configuration())

    @data(
        {'vlan_id': 2, 'ports': [1, 2, 3], 'error': None},
        {'vlan_id': 1, 'ports': [], 'error': VlanIdException},
        {'vlan_id': 9, 'ports': [], 'error': VlanIdException},
        {'vlan_id': 4, 'ports': [1, 2, 3, 4, 5, 6, 7, 8], 'error': WrongNumberOfPortsException},
        {'vlan_id': '4', 'ports': [3], 'error': VlanIdException},
        {'vlan_id': 6, 'ports': [-1], 'error': PortIdException},
        {'vlan_id': 7, 'ports': ['1'], 'error': PortIdException},
    )
    @unpack
    def test_add_port_based_vlan(self, vlan_id, ports, error):
        if error is None:
            self.assertTrue(self.vlan.add_port_based_vlan(vlan_id, ports))
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.add_port_based_vlan(vlan_id, ports)
            )

    @data(
        {
            'vlan_id': 2,
            'error': None,
            'port_based_vlan_configuration': {'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '2'}]}
        },
        {
            'vlan_id': '4',
            'error': VlanIdException,
            'port_based_vlan_configuration': None
        }
    )
    @unpack
    @patch.object(VLANControlField, 'port_based_vlan_configuration')
    def test_remove_port_based_vlan(self, port_based_vlan_configuration_mock, vlan_id, error,
                                    port_based_vlan_configuration):
        port_based_vlan_configuration_mock.return_value = port_based_vlan_configuration
        if error is None:
            self.assertTrue(self.vlan.remove_port_based_vlan(vlan_id))
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.remove_port_based_vlan(vlan_id)
            )

    def test_ieee_802_1q_vlan_configuration(self):
        ieee_802_1q_vlan_configuration = self.vlan.ieee_802_1q_vlan_configuration()
        self.assertIsNotNone(ieee_802_1q_vlan_configuration.get('802.1Q VLAN Configuration'))
        self.assertIsNotNone(ieee_802_1q_vlan_configuration.get('VLANs'))

    def test_enable_ieee_802_1q_vlan_configuration(self):
        self.assertTrue(self.vlan.enable_ieee_802_1q_vlan_configuration())

    def test_disable_ieee_802_1q_vlan_configuration(self):
        self.assertTrue(self.vlan.disable_ieee_802_1q_vlan_configuration())


