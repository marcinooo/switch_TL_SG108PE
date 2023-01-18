import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch, DEFAULT
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.vlan import VLANControlField
from switch_TL_SG108PE.port import IEEE8021QPort
from switch_TL_SG108PE.exceptions import (MtuVlanException, MtuVlanUplinkPort, PortBaseVlanException,
                                          IEEE8021QVlanException, WrongNumberOfPortsException,
                                          VlanConfigurationIsNotEnabledException, VlanIdException, PortIdException)


@ddt
class TestVLAN(unittest.TestCase):

    def setUp(self) -> None:
        self.vlan = VLANControlField(web_controller=MagicMock())

    def test_mtu_vlan_configuration(self):
        mtu_vlan_configuration = self.vlan.mtu_vlan_configuration()
        self.assertIsNotNone(mtu_vlan_configuration.get('MTU VLAN Configuration'))
        self.assertIsNotNone(mtu_vlan_configuration.get('Current Uplink Port'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': MtuVlanException,
            'alert_text': '',
        },
        {
            'error': MtuVlanException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_enable_mtu_vlan_configuration(self, get_alert_text, _is_vlan_configuration_enabled, alert_text, error):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = False
        if error is None:
            self.vlan.enable_mtu_vlan_configuration()
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.enable_mtu_vlan_configuration()
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': MtuVlanException,
            'alert_text': '',
        },
        {
            'error': MtuVlanException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_disable_mtu_vlan_configuration(self, get_alert_text, _is_vlan_configuration_enabled, alert_text, error):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = True
        if error is None:
            self.vlan.disable_mtu_vlan_configuration()
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.disable_mtu_vlan_configuration()
            )

    @data(
        {
            'port_id': 1,
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'port_id': 2,
            'error': MtuVlanUplinkPort,
            'alert_text': ''
        },
        {
            'port_id': 3,
            'error': MtuVlanUplinkPort,
            'alert_text': 'sth-other'
        },
        {
            'port_id': 9,
            'error': PortIdException,
            'alert_text': 'Operation successful.'
        },
        {
            'port_id': 0,
            'error': PortIdException,
            'alert_text': 'Operation successful.'
        },
        {
            'port_id': '3',
            'error': PortIdException,
            'alert_text': 'Operation successful.'
        }
    )
    @unpack
    @patch.object(VLANControlField, 'get_alert_text')
    @patch('switch_TL_SG108PE.control_fields.vlan.Select', Mock())
    def test_change_mtu_vlan_uplink_port(self, get_alert_text, port_id, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.vlan.change_mtu_vlan_uplink_port(port_id)
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.change_mtu_vlan_uplink_port(port_id)
            )

    def test_port_based_vlan_configuration(self):
        port_based_vlan_configuration = self.vlan.port_based_vlan_configuration()
        self.assertIsNotNone(port_based_vlan_configuration.get('Port Based VLAN Configuration'))
        self.assertIsNotNone(port_based_vlan_configuration.get('VLANs'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': PortBaseVlanException,
            'alert_text': '',
        },
        {
            'error': PortBaseVlanException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_enable_port_based_vlan_configuration(self, get_alert_text, _is_vlan_configuration_enabled, alert_text,
                                                  error):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = False
        if error is None:
            self.vlan.enable_port_based_vlan_configuration()
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.enable_port_based_vlan_configuration()
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': PortBaseVlanException,
            'alert_text': '',
        },
        {
            'error': PortBaseVlanException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_disable_port_based_vlan_configuration(self, get_alert_text, _is_vlan_configuration_enabled, alert_text,
                                                   error):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = True
        if error is None:
            self.vlan.disable_port_based_vlan_configuration()
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.disable_port_based_vlan_configuration()
            )

    @data(
        {
            'vlan_id': 2,
            'ports': [1, 2, 3],
            'error': None,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 5,
            'ports': [6, 7, 8],
            'error': PortBaseVlanException,
            'alert_text': '',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 3,
            'ports': [4, 5, 6],
            'error': PortBaseVlanException,
            'alert_text': 'sth-other.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 4,
            'ports': [5, 6, 7],
            'error': VlanConfigurationIsNotEnabledException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': False,
        },
        {
            'vlan_id': 1,
            'ports': [],
            'error': VlanIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 9,
            'ports': [],
            'error': VlanIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 4,
            'ports': [1, 2, 3, 4, 5, 6, 7, 8],
            'error': WrongNumberOfPortsException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': '4',
            'ports': [3],
            'error': VlanIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 6,
            'ports': [-1],
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 7,
            'ports': ['1'],
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_add_port_based_vlan(self, get_alert_text, _is_vlan_configuration_enabled, vlan_id, ports, error,
                                 alert_text, is_configuration_enabled):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = is_configuration_enabled
        if error is None:
            self.vlan.add_port_based_vlan(vlan_id, ports)
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.add_port_based_vlan(vlan_id, ports)
            )

    @data(
        {
            'vlan_id': 2,
            'error': None,
            'port_based_vlan_configuration_value': {
                'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '2'}]
            },
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 3,
            'error': PortBaseVlanException,
            'port_based_vlan_configuration_value': {
                'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '3'}]
            },
            'alert_text': '',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 4,
            'error': PortBaseVlanException,
            'port_based_vlan_configuration_value': {
                'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '4'}]
            },
            'alert_text': 'sth-other',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 3,
            'error': VlanConfigurationIsNotEnabledException,
            'port_based_vlan_configuration_value': {
                'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '3'}]
            },
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': False,
        },
        {
            'vlan_id': 1,
            'error': VlanIdException,
            'port_based_vlan_configuration_value': {
                'Port Based VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '1'}]
            },
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': '4',
            'error': VlanIdException,
            'port_based_vlan_configuration_value': None,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        }
    )
    @unpack
    @patch.multiple(VLANControlField,
                    get_alert_text=DEFAULT,
                    _is_vlan_configuration_enabled=DEFAULT,
                    port_based_vlan_configuration=DEFAULT)
    def test_remove_port_based_vlan(self, get_alert_text, _is_vlan_configuration_enabled,
                                    port_based_vlan_configuration, vlan_id, error, alert_text,
                                    is_configuration_enabled, port_based_vlan_configuration_value):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = is_configuration_enabled
        port_based_vlan_configuration.return_value = port_based_vlan_configuration_value
        if error is None:
            self.vlan.remove_port_based_vlan(vlan_id)
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.remove_port_based_vlan(vlan_id)
            )

    def test_ieee_802_1q_vlan_configuration(self):
        ieee_802_1q_vlan_configuration = self.vlan.ieee_802_1q_vlan_configuration()
        self.assertIsNotNone(ieee_802_1q_vlan_configuration.get('802.1Q VLAN Configuration'))
        self.assertIsNotNone(ieee_802_1q_vlan_configuration.get('VLANs'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': IEEE8021QVlanException,
            'alert_text': '',
        },
        {
            'error': IEEE8021QVlanException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_enable_ieee_802_1q_vlan_configuration(self, get_alert_text, _is_vlan_configuration_enabled, alert_text,
                                                   error):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = False
        if error is None:
            self.vlan.enable_ieee_802_1q_vlan_configuration()
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.enable_ieee_802_1q_vlan_configuration()
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': IEEE8021QVlanException,
            'alert_text': '',
        },
        {
            'error': IEEE8021QVlanException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_disable_ieee_802_1q_vlan_configuration(self, get_alert_text, _is_vlan_configuration_enabled, alert_text,
                                                    error):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = True
        if error is None:
            self.vlan.disable_ieee_802_1q_vlan_configuration()
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.disable_ieee_802_1q_vlan_configuration()
            )

    @data(
        {
            'vlan_id': 201,
            'ports': [
                IEEE8021QPort(1, tagged=True),
                IEEE8021QPort(2, tagged=False),
                IEEE8021QPort(3, tagged=True)
            ],
            'error': None,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 4000,
            'ports': [
                IEEE8021QPort(6, tagged=True),
                IEEE8021QPort(7, tagged=True),
                IEEE8021QPort(8, tagged=True)
            ],
            'error': IEEE8021QVlanException,
            'alert_text': '',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 333,
            'ports': [
                IEEE8021QPort(4, tagged=True),
                IEEE8021QPort(5, tagged=True),
                IEEE8021QPort(6, tagged=True)
            ],
            'error': IEEE8021QVlanException,
            'alert_text': 'sth-other.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 40,
            'ports': [
                IEEE8021QPort(5, tagged=True),
                IEEE8021QPort(6, tagged=True),
                IEEE8021QPort(7, tagged=True)
            ],
            'error': VlanConfigurationIsNotEnabledException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': False,
        },
        {
            'vlan_id': 10000,
            'ports': [],
            'error': VlanIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 0,
            'ports': [],
            'error': VlanIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 4,
            'ports': [
                IEEE8021QPort(1, tagged=True),
                IEEE8021QPort(2, tagged=True),
                IEEE8021QPort(3, tagged=True),
                IEEE8021QPort(4, tagged=True),
                IEEE8021QPort(5, tagged=True),
                IEEE8021QPort(6, tagged=True),
                IEEE8021QPort(7, tagged=True),
                IEEE8021QPort(8, tagged=True),
                IEEE8021QPort(9, tagged=True),
            ],
            'error': WrongNumberOfPortsException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': '4',
            'ports': [IEEE8021QPort(3, tagged=True),],
            'error': VlanIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 6,
            'ports': [-1],
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
        {
            'vlan_id': 7,
            'ports': ['1'],
            'error': PortIdException,
            'alert_text': 'Operation successful.',
            'is_configuration_enabled': True,
        },
    )
    @unpack
    @patch.multiple(VLANControlField, get_alert_text=DEFAULT, _is_vlan_configuration_enabled=DEFAULT)
    def test_add_ieee_802_1q_vlan(self, get_alert_text, _is_vlan_configuration_enabled, vlan_id, ports, error,
                                  alert_text, is_configuration_enabled):
        get_alert_text.return_value = alert_text
        _is_vlan_configuration_enabled.return_value = is_configuration_enabled
        if error is None:
            self.vlan.add_ieee_802_1q_vlan(vlan_id, ports)
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.add_ieee_802_1q_vlan(vlan_id, ports)
            )

    @data(
        {
            'vlan_id': 2,
            'error': None,
            'ieee_802_1q_vlan_configuration_value': {
                '802.1Q VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '2'}]
            },
            'alert_text': 'Operation successful.',
        },
        {
            'vlan_id': 3,
            'error': IEEE8021QVlanException,
            'ieee_802_1q_vlan_configuration_value': {
                '802.1Q VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '3'}]
            },
            'alert_text': '',
        },
        {
            'vlan_id': 4,
            'error': IEEE8021QVlanException,
            'ieee_802_1q_vlan_configuration_value': {
                '802.1Q VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '4'}]
            },
            'alert_text': 'sth-other',
        },
        {
            'vlan_id': 3,
            'error': VlanConfigurationIsNotEnabledException,
            'ieee_802_1q_vlan_configuration_value': {
                '802.1Q VLAN Configuration': 'Disable', 'VLANs': [{'VLAN ID': '3'}]
            },
            'alert_text': 'Operation successful.',
        },
        {
            'vlan_id': '4',
            'error': VlanIdException,
            'ieee_802_1q_vlan_configuration_value': {
                '802.1Q VLAN Configuration': 'Enable', 'VLANs': [{'VLAN ID': '1'}]
            },
            'alert_text': 'Operation successful.',
        }
    )
    @unpack
    @patch.multiple(VLANControlField,
                    get_alert_text=DEFAULT,
                    ieee_802_1q_vlan_configuration=DEFAULT)
    def test_remove_ieee_802_1q_vlan(self, get_alert_text, ieee_802_1q_vlan_configuration, vlan_id, error, alert_text,
                                     ieee_802_1q_vlan_configuration_value):
        get_alert_text.return_value = alert_text
        ieee_802_1q_vlan_configuration.return_value = ieee_802_1q_vlan_configuration_value
        if error is None:
            self.vlan.remove_ieee_802_1q_vlan(vlan_id)
        else:
            self.assertRaises(
                error,
                lambda: self.vlan.remove_ieee_802_1q_vlan(vlan_id)
            )
