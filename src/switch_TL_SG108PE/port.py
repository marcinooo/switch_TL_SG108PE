"""Contains constants value of port settings."""

from enum import Enum
from typing import Optional
from dataclasses import dataclass


class PORT_LABEL(Enum):  # pylint: disable=invalid-name
    """Labels of ports."""
    PORT_1 = 'Port 1'
    PORT_2 = 'Port 2'
    PORT_3 = 'Port 3'
    PORT_4 = 'Port 4'
    PORT_5 = 'Port 5'
    PORT_6 = 'Port 6'
    PORT_7 = 'Port 7'
    PORT_8 = 'Port 8'


class LAG_LABEL(Enum):  # pylint: disable=invalid-name
    """Labels of LAG."""
    LAG_1 = 'LAG 1'
    LAG_2 = 'LAG 2'


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


class FLOW_CONTROL(Enum):  # pylint: disable=invalid-name
    """Status of flow control for given port."""
    ON = 'On'
    OFF = 'Off'


class PriorityQueue(Enum):
    """QoS Priority Queue for given port."""
    LOWEST_1 = '1(Lowest)'
    NORMAL_2 = '2(Normal)'
    MEDIUM_3 = '3(Medium)'
    HIGHEST_4 = '4(Highest)'


@dataclass
class IEEE8021QPort:
    """Port object with required artifacts for VLAN 802.1Q settings."""
    port_id: int
    tagged: Optional[bool]

    def __post_init__(self):
        if self.tagged is None:
            self.tagged = False
