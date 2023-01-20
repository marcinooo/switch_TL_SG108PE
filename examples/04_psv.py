import sys
import argparse
from switch_TL_SG108PE.switch_manager import SwitchManager
from switch_TL_SG108PE.exceptions import LoginException, TpLinkSwitchException, LogoutException


def argument_parser():
    """Parses user arguments."""
    parser = argparse.ArgumentParser(
        prog='psv',
        description='Port Statistics Viewer (PSV) returns statistics for given port.'
    )
    parser.add_argument('-i', '--ip',  help='IP address of switch admin page.',
                        type=str, required=True)
    parser.add_argument('-l', '--login', help='Username to authenticate.',
                        type=str, required=True)
    parser.add_argument('-p', '--password', help='Password to authenticate.',
                        type=str, required=True)
    parser.add_argument('-s', '--switch-port', help='Port number.',
                        type=int, required=True)
    args = parser.parse_args()
    return args


def show(statistics, port):
    """Shows port statistics."""
    label = f'Port {port}'
    info = statistics[label]
    print('[*]', label)
    print('Status:       ', info['Status'])
    print('Link Status:  ', info['Link Status'])
    print('TxGoodPkt:    ', info['TxGoodPkt'])
    print('TxBadPkt:     ', info['TxBadPkt'])
    print('RxGoodPkt:    ', info['RxGoodPkt'])
    print('RxBadPkt:     ', info['RxBadPkt'])


def main():
    """Gets port statistics."""
    args = argument_parser()
    switch_manager = SwitchManager()

    try:
        switch_manager.connect(args.ip, args.login, args.password)
    except LoginException:  # Catch errors raise by given function (check them in method docs)
        print('Unable to connect to the switch management page. Check credentials.')
        sys.exit(1)

    monitoring = switch_manager.control('monitoring')

    try:
        port_statistics = monitoring.port_statistics()
        show(port_statistics, args.switch_port)
    except TpLinkSwitchException as err:  # If method doesn't raise any errors, catch base library error
        print(f'Unable to read port statistics: {err}')
        sys.exit(1)

    try:
        switch_manager.disconnect()
    except LogoutException:
        print('Unable to disconnect from the switch management page.')
        sys.exit(1)


if __name__ == '__main__':
    main()
