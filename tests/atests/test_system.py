import os
import unittest
import random
import string
from dotenv import load_dotenv

from switch_TL_SG108PE.switch_manager import SwitchManager


class TestSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(current_file_dir, '..', '..', 'environment', '.env.testing')
        load_dotenv(env_file)

    def setUp(self) -> None:
        self.switch_manager = SwitchManager()
        self.switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
        self.system = self.switch_manager.control('system')

    def tearDown(self) -> None:
        self.switch_manager.disconnect()

    def test_set_device_description(self):
        system_info = self.system.system_info()
        old_device_description = system_info['Device Description']

        new_device_description = self._random_alphanumeric_string()
        self.system.set_device_description(new_device_description)
        system_info = self.system.system_info()
        current_device_description = system_info['Device Description']
        self.assertEqual(current_device_description, new_device_description)

        self.system.set_device_description(old_device_description)

    def test_led_managing(self):
        self.assertIsNone(self.system.led_off())
        self.assertIsNone(self.system.led_on())

    @staticmethod
    def _random_alphanumeric_string(length=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


