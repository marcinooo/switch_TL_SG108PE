import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from switch_TL_SG108PE.switch_manager import SwitchManager


def main():
    switch_manager = SwitchManager()
    switch_manager.connect('192.168.1.42', 'admin', 's_witch_M1W')
    ### SYSTEM
    system = switch_manager.control('system')
    # switch_manager.get('switching')
    # switch_manager.get('monitoring')
    # switch_manager.get('VLAN')
    # switch_manager.get('QoS')
    # switch_manager.get('PoE')

    # user_account = system.user_account()
    # print(user_account)
    system.set_user_account_details('admin', 's_witch_M1W', 's_witch_M1W', 's_witch_M1W')
    # print(system.set_device_description('TL-SG108PE'))
    # ip_settings = system.ip_settings()
    # print(ip_settings)
    # system.led_on()
    # system.led_off()
    # system.disable_dhcp_settings()
    # system.set_ip('192.168.1.42', '255.255.255.0', '192.168.1.1')

    ### SWITCHING
    # switching = switch_manager.control('switching')
    # print(switching.ports_settings())
    switch_manager.disconnect()


if __name__ == '__main__':
    main()
