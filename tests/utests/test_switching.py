import os
import sys
import unittest
from unittest.mock import Mock, MagicMock, patch
from ddt import ddt, data, unpack

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src'))

from switch_TL_SG108PE.control_fields.switching import SwitchingControlField
from switch_TL_SG108PE.port import STATUS, SPEED, FLOW_CONTROL
from switch_TL_SG108PE.exceptions import (PortSettingsException, IgmpSnoopingSettings, ReportMessageSuppressionSettings,
                                          LAGPortException, PortIdException, LagIdException)


@ddt
class TestSwitching(unittest.TestCase):

    def setUp(self) -> None:
        self.switching = SwitchingControlField(web_controller=MagicMock())

    def test_ports_settings(self):
        ports_settings = self.switching.ports_settings()
        self.assertEqual(len(ports_settings.keys()), 8)
        for value in ports_settings.values():
            self.assertIsNotNone(value.get('Status'))
            self.assertIsNotNone(value.get('Speed/Duplex Config'))
            self.assertIsNotNone(value.get('Speed/Duplex Actual'))
            self.assertIsNotNone(value.get('Flow Control Config'))
            self.assertIsNotNone(value.get('Flow Control Actual'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': PortSettingsException,
            'alert_text': '',
        },
        {
            'error': PortSettingsException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.switching.Select', Mock())
    @patch.object(SwitchingControlField, 'get_alert_text')
    def test_set_port_settings(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.switching.set_port_settings(port=1, status=STATUS.ENABLE, speed=SPEED.AUTO,
                                             flow_control=FLOW_CONTROL.OFF)
        else:
            self.assertRaises(
                error,
                lambda: self.switching.set_port_settings(port=1, status=STATUS.ENABLE, speed=SPEED.AUTO,
                                                         flow_control=FLOW_CONTROL.OFF)
            )

    def test_igmp_snooping(self):
        igmp_snooping = self.switching.igmp_snooping()
        self.assertIsNotNone(igmp_snooping.get('IGMP Snooping'))
        self.assertIsNotNone(igmp_snooping.get('Report Message Suppression'))

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': IgmpSnoopingSettings,
            'alert_text': '',
        },
        {
            'error': IgmpSnoopingSettings,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SwitchingControlField, 'get_alert_text')
    def test_enable_igmp_snooping(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.switching.enable_igmp_snooping()
        else:
            self.assertRaises(
                error,
                lambda: self.switching.enable_igmp_snooping()
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': IgmpSnoopingSettings,
            'alert_text': '',
        },
        {
            'error': IgmpSnoopingSettings,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SwitchingControlField, 'get_alert_text')
    def test_disable_igmp_snooping(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.switching.disable_igmp_snooping()
        else:
            self.assertRaises(
                error,
                lambda: self.switching.disable_igmp_snooping()
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': ReportMessageSuppressionSettings,
            'alert_text': '',
        },
        {
            'error': ReportMessageSuppressionSettings,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SwitchingControlField, 'get_alert_text')
    def test_enable_report_message_suppression(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.switching.enable_report_message_suppression()
        else:
            self.assertRaises(
                error,
                lambda: self.switching.enable_report_message_suppression()
            )

    @data(
        {
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'error': ReportMessageSuppressionSettings,
            'alert_text': '',
        },
        {
            'error': ReportMessageSuppressionSettings,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch.object(SwitchingControlField, 'get_alert_text')
    def test_disable_report_message_suppression(self, get_alert_text, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.switching.disable_report_message_suppression()
        else:
            self.assertRaises(
                error,
                lambda: self.switching.disable_report_message_suppression()
            )

    def test_lag_settings(self):
        self.assertTrue(self.switching.lag_settings())  # TODO: Consider better checking

    @data(
        {
            'lag_id': 1,
            'ports': [1, 2],
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'lag_id': 2,
            'ports': [5, 6],
            'error': None,
            'alert_text': 'Operation successful.'
        },
        {
            'lag_id': 0,
            'ports': [1, 2],
            'error': LagIdException,
            'alert_text': 'Operation successful.'
        },
        {
            'lag_id': 3,
            'ports': [1, 2],
            'error': LagIdException,
            'alert_text': 'Operation successful.'
        },
        {
            'lag_id': 1,
            'ports': [-1, 2],
            'error': PortIdException,
            'alert_text': 'Operation successful.'
        },
        {
            'lag_id': 1,
            'ports': [1, 2],
            'error': LAGPortException,
            'alert_text': '',
        },
        {
            'lag_id': 1,
            'ports': [1, 2],
            'error': LAGPortException,
            'alert_text': 'sth-other',
        },
    )
    @unpack
    @patch('switch_TL_SG108PE.control_fields.switching.Select', Mock())
    @patch.object(SwitchingControlField, 'get_alert_text')
    def test_set_lag_ports(self, get_alert_text, lag_id, ports, alert_text, error):
        get_alert_text.return_value = alert_text
        if error is None:
            self.switching.set_lag_ports(lag_id, ports)
        else:
            self.assertRaises(
                error,
                lambda: self.switching.set_lag_ports(lag_id, ports)
            )



    # @patch('switch_TL_SG108PE.control_fields.switching.Select', Mock())
    # def test_set_lag_ports(self):
    #     self.assertTrue(self.switching.set_lag_ports(1, [1, 2]))
    #
    # def test_unset_lag_ports(self):
    #     self.assertTrue(self.switching.unset_lag_ports(1))
