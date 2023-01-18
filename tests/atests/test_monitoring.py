import os
import unittest
import time

from tests.atests.utils import set_up_environment_variables

from switch_TL_SG108PE.switch_manager import SwitchManager


class TestMonitoring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        set_up_environment_variables()

    def setUp(self) -> None:
        self.switch_manager = SwitchManager()
        self.switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
        self.monitoring = self.switch_manager.control('monitoring')

    def tearDown(self) -> None:
        self.switch_manager.disconnect()

    def test_getting_port_statistics(self):
        port_statistics_1 = self.monitoring.port_statistics()
        time.sleep(1)
        port_statistics_2 = self.monitoring.port_statistics(refresh=True)
        self.assertNotEqual(port_statistics_1, port_statistics_2)

    def test_port_mirror_managing(self):
        mirrored_ports = self.monitoring.mirrored_ports()['Mirrored Ports']
        for value in mirrored_ports.values():
            self.assertTrue(value['Ingress'])
            self.assertTrue(value['Egress'])

        self.monitoring.enable_port_mirroring([1, 2], 4, ingress=True, egress=False)
        self.assertEqual(self.monitoring.mirroring_port().get('Mirroring Port'), 'Port 4')
        mirrored_ports = self.monitoring.mirrored_ports()['Mirrored Ports']
        self.assertEqual(mirrored_ports['Port 1']['Ingress'], 'Enable')
        self.assertEqual(mirrored_ports['Port 1']['Egress'], 'Disable')
        self.assertEqual(mirrored_ports['Port 2']['Ingress'], 'Enable')
        self.assertEqual(mirrored_ports['Port 2']['Egress'], 'Disable')

        self.monitoring.enable_port_mirroring([3], 4, ingress=False, egress=True)
        self.assertEqual(self.monitoring.mirroring_port().get('Mirroring Port'), 'Port 4')
        mirrored_ports = self.monitoring.mirrored_ports()['Mirrored Ports']
        self.assertEqual(mirrored_ports['Port 3']['Ingress'], 'Disable')
        self.assertEqual(mirrored_ports['Port 3']['Egress'], 'Enable')

        self.monitoring.disable_port_mirroring()
        self.assertEqual(self.monitoring.mirroring_port().get('Mirroring Port'), '')

    def test_loop_prevention_managing(self):
        self.assertEqual(self.monitoring.loop_prevention().get('Loop Prevention'), 'Enable')
        self.monitoring.disable_loop_prevention()
        self.assertEqual(self.monitoring.loop_prevention().get('Loop Prevention'), 'Disable')
        self.monitoring.enable_loop_prevention()
        self.assertEqual(self.monitoring.loop_prevention().get('Loop Prevention'), 'Enable')
