import signal
import argparse
from functools import partial

from onboarding.common import start, handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', choices=['rhel6', 'rhel7'])
    args = parser.parse_args()
    minion = start(args.version)
    signal.signal(
        signal.SIGTERM,
        partial(handler, minion['container']['config']['name']))
    while True:
        pass
