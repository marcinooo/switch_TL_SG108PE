"""Contains exceptions divided in different sections."""


class TpLinkSwitchException(Exception):
    """Base library exception."""


class SwitchManagerNotConnectedException(TpLinkSwitchException):
    """Thrown when SwitchManager was not connected with switch admin page."""


class LoginException(TpLinkSwitchException):
    """Thrown when login failed."""


class LogoutException(TpLinkSwitchException):
    """Thrown when logout failed."""


class UnknownControlFieldException(TpLinkSwitchException):
    """Thrown when user entered wrong control field."""


class VlanIdException(TpLinkSwitchException):
    """Thrown when user passed wrong VLAN id."""


class PortIdException(TpLinkSwitchException):
    """Thrown when user passed wrong port id."""


class LagIdException(TpLinkSwitchException):
    """Thrown when user passed wrong lag id."""


class PortIsNotAvailableError(TpLinkSwitchException):
    """Thrown when port is not available to select."""


# <=><=><=><=><=><=><=> SYSTEM <=><=><=><=><=><=><=>


class DeviceDescriptionException(TpLinkSwitchException):
    """Thrown when setting the device description failed."""


class DhcpSettingsException(TpLinkSwitchException):
    """Thrown when user manage dhcp settings in incorrect way."""


class IpSettingException(TpLinkSwitchException):
    """Thrown when given ip cannot be applied."""


class ChangeLedStateException(TpLinkSwitchException):
    """Thrown when changing the state of LED failed."""


class InvalidUserAccountDetailsException(TpLinkSwitchException):
    """Thrown when setting new user account details failed."""


# <=><=><=><=><=><=><=> SWITCHING <=><=><=><=><=><=><=>


class OptionDisabledException(TpLinkSwitchException):
    """Thrown when option to select is disabled."""


class PortSettingsException(TpLinkSwitchException):
    """Thrown when given settings cannot be applied for given port."""


class IgmpSnoopingSettings(TpLinkSwitchException):
    """Thrown when user manage igmp snooping settings in incorrect way."""


class ReportMessageSuppressionSettings(TpLinkSwitchException):
    """Thrown when user manage Report Message Suppression settings in incorrect way."""


class LAGPortException(TpLinkSwitchException):
    """Thrown when user manage LAG group in incorrect way."""


# <=><=><=><=><=><=><=> MONITORING <=><=><=><=><=><=><=>


class MirroringPortException(TpLinkSwitchException):
    """Thrown when given mirroring port cannot be set."""


class MirroredPortException(TpLinkSwitchException):
    """Thrown when given mirrored port cannot be set."""


class PortMirroringSettingsException(TpLinkSwitchException):
    """Thrown when disable of port mirroring failed."""


class LoopPreventionException(TpLinkSwitchException):
    """Thrown when user manage loop prevention settings in incorrect way."""


# <=><=><=><=><=><=><=> VLAN <=><=><=><=><=><=><=>


class MtuVlanException(TpLinkSwitchException):
    """Thrown when mtu configuration is not enabled."""


class MtuVlanUplinkPort(TpLinkSwitchException):
    """Thrown when given port cannot be set as mtu uplink port."""


class PortBaseVlanException(TpLinkSwitchException):
    """Thrown when user manage port base vlan in incorrect way."""


class WrongNumberOfPortsException(TpLinkSwitchException):
    """Thrown when user passed incorrect number of ports."""


class VlanConfigurationIsNotEnabledException(TpLinkSwitchException):
    """Thrown when configuration of VLAN is not enabled in given section."""


class IEEE8021QVlanException(TpLinkSwitchException):
    """Thrown when user manage 802.1Q vlan in incorrect way."""


# <=><=><=><=><=><=><=> QOS <=><=><=><=><=><=><=>


class QoSModeException(TpLinkSwitchException):
    """Thrown when given QoS mode cannot be set."""


class QoSPriorityQueueException(TpLinkSwitchException):
    """Thrown when Priority Queue cannot be set."""
