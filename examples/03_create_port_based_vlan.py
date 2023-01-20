import os
from dotenv import load_dotenv
from switch_TL_SG108PE.switch_manager import SwitchManager


PORTS = [1, 2]
VLAN_ID = 2


def load_environment_variables():
    """Loads environment variables from file."""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(current_file_dir, '..', 'environment', '.env.testing')
    load_dotenv(env_file)


def main():
    """Creates Port Based VLAN 2 with ports 1 and 2."""

    load_environment_variables()

    switch_manager = SwitchManager()
    switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
    vlan = switch_manager.control('VLAN')

    vlan.enable_port_based_vlan_configuration()
    vlan.add_port_based_vlan(vlan_id=VLAN_ID, ports=PORTS)
    vlan_configuration = vlan.port_based_vlan_configuration()
    print(vlan_configuration)

    switch_manager.disconnect()


if __name__ == '__main__':
    main()
