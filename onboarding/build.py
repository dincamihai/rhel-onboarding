import re
import argparse
from py.path import local
from docker import Client
from onboarding.config import IMAGES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nocache', action='store_true', default=False)
    parser.add_argument('--dockerfile', type=local)
    parser.add_argument('--label', choices=IMAGES.keys())
    arguments = parser.parse_args()
    content = ''

    client = Client(base_url='unix://var/run/docker.sock')

    stream = client.build(
        tag=IMAGES[arguments.label],
        dockerfile=arguments.dockerfile.basename,
        path=arguments.dockerfile.dirname,
        pull=True,
        decode=True,
        forcerm=True,
        nocache=arguments.nocache
    )

    for item in stream:
        buff = item.get('stream', item.get('status', ''))

        if not content or re.search('.+\[[. ]*$', content):
            content += buff

        if not re.search('.+\[[. ]*$', content):
            print(content)
            content = ''


if __name__ == '__main__':
    main()
