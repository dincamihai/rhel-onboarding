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
from saltcontainers.factories import MinionFactory
from onboarding.config import IMAGES


def create_minion(image):
    client = docker.Client(base_url='unix://var/run/docker.sock')
    salt_root = local(tempfile.mkdtemp())
    host_config = client.create_host_config(network_mode='host')
    return MinionFactory(
        container__config__docker_client=client,
        container__config__image=image,
        container__config__salt_config__tmpdir=salt_root,
        container__config__salt_config__conf_type='minion',
        container__config__salt_config__config={
            'base_config': {'master': os.environ['MASTER_IP']}
        },
        container__config__host_config=host_config
    )


def set_machine_id(minion):
    tmpdir = local(tempfile.mkdtemp())
    fake = faker.Faker()
    machineid = fake.sha1()
    config = minion['container']['config']
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
    parser.add_argument('--label', choices=['rhel6', 'rhel7'])
    args = parser.parse_args()

    minion = create_minion(IMAGES[args.label])
    name = minion['container']['config']['name']

    sys.stdout.write("minion id: {0}\n".format(minion['id']))
    sys.stdout.write("container id: {0}\n".format(name))
    sys.stdout.write(
        "shell command: 'docker exec -it {0} /bin/bash'\n".format(name))

    machineid, tmpdir = set_machine_id(minion)
    sys.stdout.write(
        "generated machine id {0} stored in /etc/machine-id\n".format(machineid))

    sys.stdout.flush()
    signal.signal(signal.SIGTERM, partial(handler, name, tmpdir))
    signal.pause()


if __name__ == '__main__':
    main()
