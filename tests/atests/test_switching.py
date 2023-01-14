import os
import unittest

from tests.atests.utils import set_up_environment_variables

from switch_TL_SG108PE.switch_manager import SwitchManager
from switch_TL_SG108PE.port import STATUS, SPEED, FLOW_CONTROL


class TestSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        set_up_environment_variables()

    def setUp(self) -> None:
        self.switch_manager = SwitchManager()
        self.switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
        self.switching = self.switch_manager.control('switching')

    def tearDown(self) -> None:
        self.switch_manager.disconnect()

    def test_ports_settings_management(self):
        ports_settings = self.switching.ports_settings()['Port 1']
        port_1_status = ports_settings.get('Status')
        port_1_flow_control = ports_settings.get('Flow Control Config')
        port_1_speed = ports_settings.get('Speed/Duplex Config')
        self.assertEqual(port_1_status, 'Enabled')
        self.assertEqual(port_1_flow_control, 'Off')
        self.assertNotEqual(port_1_speed, '10MF')

        self.switching.set_port_settings(port=1, status=STATUS.DISABLE, speed=SPEED.S10MF,
                                         flow_control=FLOW_CONTROL.OFF)

        ports_settings = self.switching.ports_settings()
        self.assertEqual(ports_settings['Port 1']['Status'], 'Disabled')
        self.assertEqual(ports_settings['Port 1']['Speed/Duplex Config'], '10MF')
        self.assertEqual(ports_settings['Port 1']['Flow Control Config'], 'Off')

        self.switching.set_port_settings(port=1, status=STATUS.ENABLE, speed=SPEED.AUTO, flow_control=FLOW_CONTROL.OFF)

    def test_igmp_snooping_management(self):
        status = self.switching.igmp_snooping()
        self.assertEqual(status.get('IGMP Snooping'), 'Enable')
        self.assertEqual(status.get('Report Message Suppression'), 'Disable')

        self.switching.disable_igmp_snooping()
        status = self.switching.igmp_snooping()
        self.assertEqual(status.get('IGMP Snooping'), 'Disable')
        self.switching.enable_igmp_snooping()

    def test_report_message_suppression_management(self):
        self.switching.enable_report_message_suppression()
        status = self.switching.igmp_snooping()
        self.assertEqual(status.get('Report Message Suppression'), 'Enable')
        self.switching.disable_report_message_suppression()

    def test_lag_settings_management(self):
        status = self.switching.lag_settings()
        self.assertEqual(status.get('LAG 1'), '----')
        self.assertEqual(status.get('LAG 2'), '----')

        self.switching.set_lag_ports(1, [1, 2, 3, 4])
        self.switching.set_lag_ports(2, [5, 6, 7, 8])
        status = self.switching.lag_settings()
        self.assertEqual(status.get('LAG 1'), '1,2,3,4')
        self.assertEqual(status.get('LAG 2'), '5,6,7,8')

        self.switching.unset_lag_ports(1)
        self.switching.unset_lag_ports(2)
        status = self.switching.lag_settings()
        self.assertEqual(status.get('LAG 1'), '----')
        self.assertEqual(status.get('LAG 2'), '----')
