import os
import pprint
from dotenv import load_dotenv
from switch_TL_SG108PE.switch_manager import SwitchManager


def load_environment_variables():
    """Loads environment variables from file."""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(current_file_dir, '..', 'environment', '.env.testing')
    load_dotenv(env_file)


def main():
    """Enables traffic mirroring (redirects traffic from port 1 to port 2)."""

    load_environment_variables()

    switch_manager = SwitchManager()
    print('Connecting... ', end='')
    switch_manager.connect(os.environ['ADMIN_IP'], os.environ['ADMIN_USERNAME'], os.environ['ADMIN_PASSWORD'])
    print('OK')
    monitoring = switch_manager.control('monitoring')

    mirrored_ports = [1]
    mirroring_port = 2
    print('Setting port mirroring... ', end='')
    monitoring.enable_port_mirroring(mirrored_ports, mirroring_port)
    print('OK')
    print()

    info = monitoring.mirrored_ports()
    print(f'Mirrored ports:')
    pprint.pprint(info)
    print()

    info = monitoring.mirroring_port()
    print(f'Mirroring port:')
    pprint.pprint(info)
    print()

    switch_manager.disconnect()


if __name__ == '__main__':
    main()
