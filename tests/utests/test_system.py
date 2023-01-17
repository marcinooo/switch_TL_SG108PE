import os
import sys
import unittest
from unittest.mock import Mock, patch, DEFAULT
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.system import SystemControlField
from switch_TL_SG108PE.exceptions import (DeviceDescriptionException, DhcpSettingsException, IpSettingException,
                                          ChangeLedStateException, InvalidUserAccountDetailsException)


@ddt
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

    @data(
        {
            'description': '12345678901234567890123456789012',
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'description': '123456789012345678901234567890123',
            'error': DeviceDescriptionException,
            'alert_text': 'Operation successful.'
        },
        {
            'description': 'super-switch',
            'error': DeviceDescriptionException,
            'alert_text': '',
        },
        {
            'description': 'super-switch',
            'error': DeviceDescriptionException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SystemControlField, 'get_alert_text')
    def test_set_device_description(self, get_alert_text, description, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.system.set_device_description(description)
        else:
            self.assertRaises(error, lambda: self.system.set_device_description(description))

    def test_ip_settings(self):
        ip_settings = self.system.ip_settings()
        self.assertIsNotNone(ip_settings.get('DHCP Setting'))
        self.assertIsNotNone(ip_settings.get('IP Address'))
        self.assertIsNotNone(ip_settings.get('Subnet Mask'))
        self.assertIsNotNone(ip_settings.get('Default Gateway'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': DhcpSettingsException,
            'alert_text': '',
        },
        {
            'error': DhcpSettingsException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SystemControlField, 'get_alert_text')
    @patch('switch_TL_SG108PE.control_fields.system.Select', Mock())
    def test_enable_dhcp_configuration(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.system.enable_dhcp_configuration()
        else:
            self.assertRaises(error, lambda: self.system.enable_dhcp_configuration())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': DhcpSettingsException,
            'alert_text': '',
        },
        {
            'error': DhcpSettingsException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SystemControlField, 'get_alert_text')
    @patch('switch_TL_SG108PE.control_fields.system.Select', Mock())
    def test_disable_dhcp_configuration(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.system.disable_dhcp_configuration()
        else:
            self.assertRaises(error, lambda: self.system.disable_dhcp_configuration())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.',
            'ip_settings_value': {'DHCP Setting': 'disable'}
        },
        {
            'error': DhcpSettingsException,
            'alert_text': 'Operation successful.',
            'ip_settings_value': {'DHCP Setting': 'enabled'}
        },
        {
            'error': IpSettingException,
            'alert_text': '',
            'ip_settings_value': {'DHCP Setting': 'disable'}
        },
        {
            'error': IpSettingException,
            'alert_text': 'sth-other',
            'ip_settings_value': {'DHCP Setting': 'disable'}
        },
    )
    @unpack
    @patch.multiple(SystemControlField, get_alert_text=DEFAULT, ip_settings=DEFAULT)
    def test_set_ip(self, get_alert_text, ip_settings, error, alert_text, ip_settings_value):
        get_alert_text.return_value = alert_text
        ip_settings.return_value = ip_settings_value
        if error is None:
            self.system.set_ip(ip_address='0.0.0.0', subnet_mask='1.1.1.1', default_gateway='2.2.2.2')
        else:
            self.assertRaises(
                error,
                lambda: self.system.set_ip(ip_address='0.0.0.0', subnet_mask='1.1.1.1', default_gateway='2.2.2.2')
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': ChangeLedStateException,
            'alert_text': '',
        },
        {
            'error': ChangeLedStateException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SystemControlField, 'get_alert_text')
    def test_led_on(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.system.led_on()
        else:
            self.assertRaises(error, lambda: self.system.led_on())

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': ChangeLedStateException,
            'alert_text': '',
        },
        {
            'error': ChangeLedStateException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SystemControlField, 'get_alert_text')
    def test_led_off(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.system.led_off()
        else:
            self.assertRaises(error, lambda: self.system.led_off())

    def test_user_account(self):
        user_account = self.system.user_account()
        self.assertIsNotNone(user_account.get('Current Username'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': InvalidUserAccountDetailsException,
            'alert_text': '',
        },
        {
            'error': InvalidUserAccountDetailsException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SystemControlField, 'get_alert_text')
    def test_set_user_account_details(self, get_alert_text, error, alert_text):
        get_alert_text.return_value = alert_text
        if error is None:
            self.system.set_user_account_details('admin', 'old_admin', 'new_admin', 'new_admin')
        else:
            self.assertRaises(
                error,
                lambda: self.system.set_user_account_details('admin', 'old_admin', 'new_admin', 'new_admin')
            )
