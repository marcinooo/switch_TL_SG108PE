

class TpLinkSwitchError(Exception):
    pass


class SwitchManagerNotConnectedException(TpLinkSwitchError):
    """Thrown when SwitchManager was not connected with switch admin page."""


class LoginException(TpLinkSwitchError):
    """Thrown when login failed."""


class LogoutException(TpLinkSwitchError):
    """Thrown when logout failed."""


class InvalidDescriptionException(TpLinkSwitchError):
    """Thrown when settings device description failed."""


class InvalidUserAccountDetailsException(TpLinkSwitchError):
    """Thrown when setting new user account details failed."""


class DHCPSettingsEnabledError(TpLinkSwitchError):
    pass


class LAGPortError(TpLinkSwitchError):
    pass


class UnknownControlFieldError(TpLinkSwitchError):
    pass


class PortIsNotAvailableError(TpLinkSwitchError):
    pass


class MtuVlanIsNotEnabled(TpLinkSwitchError):
    pass


class VlanConfigurationIsNotEnabledError(TpLinkSwitchError):
    pass


class WrongNumberOfPortsError(TpLinkSwitchError):
    pass


class VLANdoesNotExist(TpLinkSwitchError):
    pass


class WrongVlanIdError(TpLinkSwitchError):
    pass


class VlanIdError(TpLinkSwitchError):  # TODO: merge witch above
    pass


class PortIdError(TpLinkSwitchError):
    pass


class LagIdError(TpLinkSwitchError):
    pass


class OptionDisabled(TpLinkSwitchError):  # TODO: Change name
    pass
