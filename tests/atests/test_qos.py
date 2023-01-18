import os
import unittest
from dotenv import load_dotenv

from switch_TL_SG108PE.switch_manager import SwitchManager
from switch_TL_SG108PE.port import PriorityQueue


class TestSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(current_file_dir, '..', '..', 'environment', '.env.testing')
        load_dotenv(env_file)

    def setUp(self) -> None:
        self.switch_manager = SwitchManager()
        self.switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
        self.qos = self.switch_manager.control('QoS')

    def tearDown(self) -> None:
        self.switch_manager.disconnect()

    def test_qos_mode_managing(self):
        mode = self.qos.qos_mode()
        self.assertEqual(mode, 'DSCP/802.1P Based')

        # Test to enable current enabled mode
        self.qos.set_dscp_802_1p_based_qos_mode()

        self.qos.set_802_1p_based_qos_mode()
        mode = self.qos.qos_mode()
        self.assertEqual(mode, '802.1P Based')

        self.qos.set_port_base_qos_mode()
        mode = self.qos.qos_mode()
        self.assertEqual(mode, 'Port Based')

        self.qos.set_priority_queue_in_port_based_qos_mode(1, PriorityQueue.HIGHEST_4)
        port_1_priority = self.qos.priority_queue_port_settings()['Port 1']
        self.assertEqual(port_1_priority, '4(Highest)')
        self.qos.set_priority_queue_in_port_based_qos_mode(3, PriorityQueue.LOWEST_1)
        port_3_priority = self.qos.priority_queue_port_settings()['Port 3']
        self.assertEqual(port_3_priority, '1(Lowest)')

        self.qos.set_dscp_802_1p_based_qos_mode()
