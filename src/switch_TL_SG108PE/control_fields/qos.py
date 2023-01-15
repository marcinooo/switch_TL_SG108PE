"""Contains code to manage QoS section from menu tab."""

from .control_field import ControlField


class QoSControlField(ControlField):
    """Creates object to control QoS settings on switch."""

    _MENU_SECTION = 'QoS'
