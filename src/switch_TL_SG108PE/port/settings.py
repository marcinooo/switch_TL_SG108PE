"""Contains constants value of port settings."""

from enum import Enum


class NO(Enum):
    """Number (labels) of ports."""
    PORT_1 = 'Port 1'
    PORT_2 = 'Port 2'
    PORT_3 = 'Port 3'
    PORT_4 = 'Port 4'
    PORT_5 = 'Port 5'
    PORT_6 = 'Port 6'
    PORT_7 = 'Port 7'
    PORT_8 = 'Port 8'


class STATUS(Enum):
    """Port statuses."""
    ENABLE = 'Enable'
    DISABLE = 'Disable'


class SPEED(Enum):
    """Port speed."""
    AUTO = 'Auto'
    S10MH = '10MH'
    S10MF = '10MF'
    S100MH = '100MH'
    S100MF = '100MF'
    S1000MF = '1000MF'


class FLOW_CONTROL(Enum):
    """Status of flow control for given port."""
    ON = 'On'
    OFF = 'Off'


class GROUP_ID(Enum):
    """Lag group id (label)."""
    LAG1 = 'LAG 1'
    LAG2 = 'LAG 2'
