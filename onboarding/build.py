import os
import re
import argparse
from docker import Client


def build_docker_image(version, flavor, nocache=False):
    docker_client = Client(base_url='unix://var/run/docker.sock')

    return docker_client.build(
        tag='registry.mgr.suse.de/toaster-{0}-{1}'.format(version, flavor),
        dockerfile='Dockerfile.{0}.{1}'.format(version, flavor),
        path='./onboarding/docker/',
        pull=True,
        decode=True,
        forcerm=True,
        nocache=nocache
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nocache', action='store_true', default=False)
    parser.add_argument('--version')
    parser.add_argument('--flavor')
    args = parser.parse_args()
    content = ''
    stream = build_docker_image(args.version, args.flavor, nocache=args.nocache)
    for item in stream:
        buff = item.get('stream', item.get('status', ''))

        if not content or re.search('.+\[[. ]*$', content):
            content += buff

        if not re.search('.+\[[. ]*$', content):
            print(content)
            content = ''


if __name__ == '__main__':
    main()
