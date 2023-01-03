import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from switch_TL_SG108PE.switch_manager import SwitchManager


def main():
    switch_manager = SwitchManager()
    switch_manager.connect('192.168.1.42', 'admin', 's_witch_M1W')
    ### SYSTEM
    # system = switch_manager.get('system')
    # switch_manager.get('switching')
    # switch_manager.get('monitoring')
    # switch_manager.get('VLAN')
    # switch_manager.get('QoS')
    # switch_manager.get('PoE')

    # system_info = system.system_info()
    # print(system_info)
    # print(system.set_device_description('TL-SG108PE'))
    # ip_settings = system.ip_settings()
    # print(ip_settings)
    # system.led_on()
    # system.led_off()
    # system.disable_dhcp_settings()
    # system.set_ip('192.168.1.42', '255.255.255.0', '192.168.1.1')

    ### SWITCHING
    switching = switch_manager.get('switching')
    print(switching.ports_settings())
    switch_manager.disconnect()


if __name__ == '__main__':
    main()
