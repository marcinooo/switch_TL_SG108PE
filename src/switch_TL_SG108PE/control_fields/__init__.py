"""Contains code to control given sections on switch admin page."""

from .control_field import ControlField
from . import system, switching, monitoring, vlan, qos, poe


__all__ = [
    'ControlField',
    'system',
    'switching',
    'monitoring',
    'vlan',
    'qos',
    'poe'
]
