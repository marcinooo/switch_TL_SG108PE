"""Contains artifacts common for library."""

from enum import Enum

from .port import PORT_LABEL, LAG_LABEL
from .exceptions import VlanIdException, PortIdException, LagIdException


class Frame(Enum):
    """Frames html ids."""

    MENU = 'bottomLeftFrame'
    MAIN = 'mainFrame'
    TOP = 'topFrame'


def get_port_label(port_id: int) -> PORT_LABEL:
    """
    Gets label for given port id. Label is string pattern visible in admin page.

    :param port_id: port number
    :return: port label
    """
    return getattr(PORT_LABEL, f'PORT_{port_id}')


def get_lag_label(lag_id: int) -> LAG_LABEL:
    """
    Gets label for given LAG id. Label is string pattern visible in admin page.

    :param lag_id: port number
    :return: lag label
    """
    return getattr(LAG_LABEL, f'LAG_{lag_id}')


def validate_vlan_id(vlan_id: int) -> None:
    """
    Validates id of vlan. If id is incorrect, exception will be raised.

    :param vlan_id:
    :return: None
    """
    if not isinstance(vlan_id, int):
        raise VlanIdException('VLAN ID should be an integer')


def validate_port_id(port_id: int) -> None:
    """
    Validates id of port. If id is incorrect, exception will be raised.

    :param port_id:
    :return: None
    """
    if not isinstance(port_id, int):
        raise PortIdException('Port ID should be an integer')
    if not 1 <= port_id <= 8:
        raise PortIdException('Port ID must be in range of 1-8.')


def validate_lag_id(lag_id: int) -> None:
    """
    Validates id of LAG. If id is incorrect, exception will be raised.

    :param lag_id:
    :return: None
    """
    if not isinstance(lag_id, int):
        raise LagIdException('LAG ID should be an integer')
    if not 1 <= lag_id <= 2:
        raise LagIdException('LAG ID must be in range of 1-2.')
