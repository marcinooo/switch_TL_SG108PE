import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.system import SystemControlField
from switch_TL_SG108PE.exceptions import DHCPSettingsEnabledException


class TestSystem(unittest.TestCase):

    def setUp(self) -> None:
        self.system = SystemControlField(web_controller=Mock())

    def test_system_info(self):
        system_info = self.system.system_info()
        self.assertIsNotNone(system_info.get('Device Description'))
        self.assertIsNotNone(system_info.get('MAC Address'))
        self.assertIsNotNone(system_info.get('IP Address'))
        self.assertIsNotNone(system_info.get('Subnet Mask'))
        self.assertIsNotNone(system_info.get('Default Gateway'))
        self.assertIsNotNone(system_info.get('Firmware Version'))
        self.assertIsNotNone(system_info.get('Hardware Version'))

    def test_set_device_description(self):
        self.assertTrue(self.system.set_device_description('switch001'))

    def test_ip_settings(self):
        ip_settings = self.system.ip_settings()
        self.assertIsNotNone(ip_settings.get('DHCP Setting'))
        self.assertIsNotNone(ip_settings.get('IP Address'))
        self.assertIsNotNone(ip_settings.get('Subnet Mask'))
        self.assertIsNotNone(ip_settings.get('Default Gateway'))

    @patch('switch_TL_SG108PE.control_fields.system.Select', Mock())
    def test_enable_dhcp_configuration(self,):
        self.assertTrue(self.system.enable_dhcp_configuration())

    @patch('switch_TL_SG108PE.control_fields.system.Select', Mock())
    def test_disable_dhcp_configuration(self):
        self.assertTrue(self.system.disable_dhcp_configuration())

    def test_set_ip_fails_when_dhcp_configuration_is_enabled(self):
        self.assertRaises(
            DHCPSettingsEnabledException,
            lambda: self.system.set_ip(ip_address='0.0.0.0', subnet_mask='1.1.1.1', default_gateway='2.2.2.2')
        )

    @patch.object(SystemControlField, 'ip_settings')
    def test_set_ip_works_fine(self, ip_settings):
        ip_settings.return_value = {'DHCP Setting': 'disable'}
        self.assertTrue(self.system.set_ip(ip_address='0.0.0.0', subnet_mask='1.1.1.1', default_gateway='2.2.2.2'))

    def test_led_on(self):
        self.assertTrue(self.system.led_on())

    def test_led_off(self):
        self.assertTrue(self.system.led_off())

    def test_user_account(self):
        user_account = self.system.user_account()
        self.assertIsNotNone(user_account.get('Current Username'))

    @patch.object(SystemControlField, 'get_alert_text')
    def test_set_user_account_details(self, get_alert_text):
        get_alert_text.return_value = 'Operation successful.'
        self.assertTrue(self.system.set_user_account_details('admin', 'old_admin', 'new_admin', 'new_admin'))  # ;)
