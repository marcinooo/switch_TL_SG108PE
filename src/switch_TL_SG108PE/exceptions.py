"""Contains exceptions."""


class TpLinkSwitchException(Exception):
    """Base library exception."""


class SwitchManagerNotConnectedException(TpLinkSwitchException):
    """Thrown when SwitchManager was not connected with switch admin page."""


class LoginException(TpLinkSwitchException):
    """Thrown when login failed."""


class LogoutException(TpLinkSwitchException):
    """Thrown when logout failed."""


class InvalidDescriptionException(TpLinkSwitchException):
    """Thrown when settings device description failed."""


class InvalidUserAccountDetailsException(TpLinkSwitchException):
    """Thrown when setting new user account details failed."""


class DHCPSettingsEnabledException(TpLinkSwitchException):
    """Thrown when getting host from DHCP is enabled and user try set own host."""


class LAGPortException(TpLinkSwitchException):
    """Thrown when port is invalid to add to LAG group."""


class UnknownControlFieldException(TpLinkSwitchException):
    """Thrown when user entered wrong control field."""


class PortIsNotAvailableError(TpLinkSwitchException):
    """Thrown when port is not available to select."""


class MtuVlanIsNotEnabled(TpLinkSwitchException):
    """Thrown when mtu configuration is not enabled."""


class VlanConfigurationIsNotEnabledException(TpLinkSwitchException):
    """Thrown when configuration of VLAN is not enabled in given section."""


class WrongNumberOfPortsException(TpLinkSwitchException):
    """Thrown when user passed incorrect number of ports."""


class VlanIdException(TpLinkSwitchException):
    """Thrown when user passed wrong VLAN id."""


class PortIdException(TpLinkSwitchException):
    """Thrown when user passed wrong port id."""


class LagIdException(TpLinkSwitchException):
    """Thrown when user passed wrong lag id."""


class OptionDisabledException(TpLinkSwitchException):
    """Thrown when option to select is disabled."""
