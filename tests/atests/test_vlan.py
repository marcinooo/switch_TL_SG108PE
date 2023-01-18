import os
import unittest

from tests.atests.utils import set_up_environment_variables

from switch_TL_SG108PE.switch_manager import SwitchManager
from switch_TL_SG108PE.exceptions import MtuVlanException, VlanConfigurationIsNotEnabledException
from switch_TL_SG108PE.port import IEEE8021QPort


class TestVLAN(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        set_up_environment_variables()

    def setUp(self) -> None:
        self.switch_manager = SwitchManager()
        self.switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
        self.vlan = self.switch_manager.control('VLAN')

    def tearDown(self) -> None:
        self.switch_manager.disconnect()

    def test_mtu_vlan_managing(self):
        mtu_vlan_status = self.vlan.mtu_vlan_configuration()['MTU VLAN Configuration']
        self.assertEqual(mtu_vlan_status, 'Disable')

        self.vlan.enable_mtu_vlan_configuration()
        mtu_vlan_status = self.vlan.mtu_vlan_configuration()['MTU VLAN Configuration']
        self.assertEqual(mtu_vlan_status, 'Enable')

        # Test valid changing
        self.vlan.change_mtu_vlan_uplink_port(1)
        mtu_vlan_uplink_port = self.vlan.mtu_vlan_configuration()['Current Uplink Port']
        self.assertEqual(mtu_vlan_uplink_port, '1')

        self.vlan.disable_mtu_vlan_configuration()
        mtu_vlan_status = self.vlan.mtu_vlan_configuration()['MTU VLAN Configuration']
        self.assertEqual(mtu_vlan_status, 'Disable')

        # Test invalid changing
        self.assertRaises(
            MtuVlanException,
            lambda: self.vlan.change_mtu_vlan_uplink_port(7)
        )

    def test_port_based_vlan_managing(self):
        port_based_vlan_status = self.vlan.port_based_vlan_configuration()['Port Based VLAN Configuration']
        self.assertEqual(port_based_vlan_status, 'Disable')

        self.vlan.enable_port_based_vlan_configuration()
        port_based_vlan_status = self.vlan.port_based_vlan_configuration()['Port Based VLAN Configuration']
        self.assertEqual(port_based_vlan_status, 'Enable')

        # Test valid adding
        self.vlan.add_port_based_vlan(2, [2, 3, 4])
        vlans = self.vlan.port_based_vlan_configuration()['VLANs']
        added_vlan = next(filter(lambda v: v['VLAN ID'] == '2', vlans), None)
        self.assertIsNotNone(added_vlan)
        self.assertEqual(added_vlan['VLAN Member Port'], '2-4')

        self.vlan.remove_port_based_vlan(2)
        vlans = self.vlan.port_based_vlan_configuration()['VLANs']
        vlan = next(filter(lambda v: v['VLAN ID'] == 6, vlans), None)
        self.assertIsNone(vlan)

        self.vlan.disable_port_based_vlan_configuration()
        port_based_vlan_status = self.vlan.port_based_vlan_configuration()['Port Based VLAN Configuration']
        self.assertEqual(port_based_vlan_status, 'Disable')

        # Test invalid adding
        self.assertRaises(
            VlanConfigurationIsNotEnabledException,
            lambda: self.vlan.add_port_based_vlan(3, [8])
        )

    def test_ieee_802_1Q_vlan_managing(self):
        ieee_802_1q_vlan_status = self.vlan.ieee_802_1q_vlan_configuration()['802.1Q VLAN Configuration']
        self.assertEqual(ieee_802_1q_vlan_status, 'Disable')

        self.vlan.enable_ieee_802_1q_vlan_configuration()
        ieee_802_1q_vlan_status = self.vlan.ieee_802_1q_vlan_configuration()['802.1Q VLAN Configuration']
        self.assertEqual(ieee_802_1q_vlan_status, 'Enable')

        # Test valid adding
        self.vlan.add_ieee_802_1q_vlan(6, [IEEE8021QPort(port_id=1, tagged=False),
                                           IEEE8021QPort(port_id=2, tagged=True)], vlan_name='ole')
        vlans = self.vlan.ieee_802_1q_vlan_configuration()['VLANs']
        added_vlan = next(filter(lambda v: v['VLAN ID'] == '6', vlans), None)
        self.assertIsNotNone(added_vlan)
        self.assertEqual(added_vlan['Member Ports'], '1-2')
        self.assertEqual(added_vlan['Tagged Ports'], '2')
        self.assertEqual(added_vlan['Untagged Ports'], '1')
        self.vlan.add_ieee_802_1q_vlan(7, [IEEE8021QPort(port_id=1, tagged=False)])
        for i in range(6, 8):
            vlans = self.vlan.ieee_802_1q_vlan_configuration()['VLANs']
            added_vlan = next(filter(lambda v: v['VLAN ID'] == str(i), vlans), None)
            self.assertIsNotNone(added_vlan)
            self.assertIn('1', added_vlan['Member Ports'])

        self.vlan.remove_ieee_802_1q_vlan(6)
        vlans = self.vlan.ieee_802_1q_vlan_configuration()['VLANs']
        vlan = next(filter(lambda v: v['VLAN ID'] == 6, vlans), None)
        self.assertIsNone(vlan)

        self.vlan.disable_ieee_802_1q_vlan_configuration()
        ieee_802_1q_vlan_status = self.vlan.ieee_802_1q_vlan_configuration()['802.1Q VLAN Configuration']
        self.assertEqual(ieee_802_1q_vlan_status, 'Disable')

        # Test invalid adding
        self.assertRaises(
            VlanConfigurationIsNotEnabledException,
            lambda: self.vlan.add_ieee_802_1q_vlan(4, [IEEE8021QPort(port_id=8, tagged=False)])
        )
