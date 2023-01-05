

class TpLinkSwitchError(Exception):
    pass


class SwitchManagerNotConnectedError(TpLinkSwitchError):
    pass


class LoginError(TpLinkSwitchError):
    pass


class LogoutError(TpLinkSwitchError):
    pass


class InvalidDescription(TpLinkSwitchError):
    pass


class DHCPSettingsEnabledError(TpLinkSwitchError):
    pass
