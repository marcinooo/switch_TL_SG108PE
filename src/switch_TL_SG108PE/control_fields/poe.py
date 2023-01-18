"""Contains code to manage PoE section from menu tab."""

from .control_field import ControlField


class PoEControlField(ControlField):
    """Creates object to control PoE settings on switch."""

    _MENU_SECTION = 'PoE'
