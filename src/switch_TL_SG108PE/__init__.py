"""Package to control tp-link switch TL-SG108PE."""   # pylint: disable=invalid-name


__author__ = "marcinooo"
__maintainer__ = "marcinooo"
__version__ = "0.0.0"


from .switch_manager import SwitchManager
from . import exceptions, port, control_fields


__all__ = [
    'exceptions',
    'port',
    'control_fields'
]
