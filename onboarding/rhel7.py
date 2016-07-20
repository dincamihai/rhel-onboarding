import signal
from functools import partial

from onboarding.common import start, handler


if __name__ == '__main__':
    minion = start('rhel7')
    signal.signal(
        signal.SIGTERM,
        partial(handler, minion['container']['config']['name']))
    while True:
        pass
