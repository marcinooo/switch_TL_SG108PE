import os
from switch_TL_SG108PE.switch_manager import SwitchManager


# set required system variables before running script (example for Linux system)
# $ export ADMIN_IP=<switch ip>
# $ export ADMIN_USERNAME=<admin username>
# $ export ADMIN_PASSWORD=<admin password>

switch_manager = SwitchManager()
switch_manager.connect(os.environ['ADMIN_IP'],
                       os.environ['ADMIN_USERNAME'],
                       os.environ['ADMIN_PASSWORD'])
system = switch_manager.control('system')
info = system.system_info()
print(info)
switch_manager.disconnect()
