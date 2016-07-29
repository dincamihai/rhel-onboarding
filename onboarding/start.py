import os
import sys
import faker
import tempfile
import tarfile
import docker
import signal
import argparse
import py.error
from functools import partial
from py.path import local
from saltcontainers.factories import (
    ContainerConfigFactory, ContainerFactory, MinionFactory
)
from onboarding.config import IMAGES


def create_container_config(image):
    client = docker.Client(base_url='unix://var/run/docker.sock')
    salt_root = local(tempfile.mkdtemp())
    host_config = client.create_host_config(network_mode='host')
    return ContainerConfigFactory(
        docker_client=client,
        image=image,
        salt_config__tmpdir=salt_root,
        salt_config__conf_type='minion',
        salt_config__config={
            'base_config': {'master': os.environ['MASTER_IP']}
        },
        host_config=host_config
    )


def create_container(config):
    return ContainerFactory(config=config)


def set_machine_id(config):
    tmpdir = local(tempfile.mkdtemp())
    fake = faker.Faker()
    machineid = fake.sha1()
    with (tmpdir / 'etc' / 'machine-id').open(mode='wb', ensure=True) as f:
        f.write(machineid)

    with tarfile.open((tmpdir / 'machine-id.tar').strpath, mode='w') as archive:
        archive.add((tmpdir / 'etc').strpath, arcname='etc')

    with open((tmpdir / 'machine-id.tar').strpath, 'rb') as f:
        config['docker_client'].put_archive(config['name'], '/', f.read())
    return machineid, tmpdir


def handler(name, tmpdir, signum, frame):
    client = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        sys.stdout.write("removing container {0}\n".format(name))
        client.remove_container(name, force=True)
        tmpdir.remove()
    except py.error.ENOENT as err:
        pattern = 'removing {0} failed with message: {1}\n'
        sys.stdout.write(pattern.format(tmpdir, err.message))
    except Exception as err:
        sys.stdout.write(
            'cleanup command failed: docker rm -f {0}\n'.format(name))
        sys.stdout.write(err.message)
    finally:
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=IMAGES.keys())
    parser.add_argument('--nosalt', action='store_true', default=False)
    args = parser.parse_args()

    config = create_container_config(IMAGES[args.label])

    if args.nosalt:
        ContainerFactory(config=config)
    else:
        minion = MinionFactory(container__config=config)
        sys.stdout.write("minion id: {0}\n".format(minion['id']))

    machineid, tmpdir = set_machine_id(config)
    name = config['name']

    sys.stdout.write("container id: {0}\n".format(name))
    sys.stdout.write(
        "shell command: 'docker exec -it {0} /bin/bash'\n".format(name))
    sys.stdout.write(
        "generated machine id {0} stored in /etc/machine-id\n".format(machineid))

    sys.stdout.flush()
    signal.signal(signal.SIGTERM, partial(handler, name, tmpdir))
    signal.pause()


if __name__ == '__main__':
    main()
