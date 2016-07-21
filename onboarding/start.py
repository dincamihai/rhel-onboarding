import os
import sys
import faker
import tempfile
import tarfile
import docker
import signal
import argparse
from functools import partial
from py.path import local
from saltcontainers.factories import MinionFactory


IMAGES = dict(
    rhel6='registry.mgr.suse.de/toaster-rhel6-products',
    rhel7='registry.mgr.suse.de/toaster-rhel7-products'
)


def create_minion(docker_client, image):
    salt_root = local(tempfile.mkdtemp())
    host_config = docker_client.create_host_config(network_mode='host')
    return MinionFactory(
        container__config__docker_client=docker_client,
        container__config__image=image,
        container__config__salt_config__tmpdir=salt_root,
        container__config__salt_config__conf_type='minion',
        container__config__salt_config__config={
            'base_config': {'master': os.environ['MASTER_IP']}
        },
        container__config__host_config=host_config
    )


def start(image):
    tmpdir = local(tempfile.mkdtemp())
    fake = faker.Faker()
    machineid = fake.sha1()
    try:
        client = docker.Client(base_url='unix://var/run/docker.sock')
        minion = create_minion(client, image)
        config = minion['container']['config']

        with (tmpdir / 'etc' / 'machine-id').open(mode='wb', ensure=True) as f:
            f.write(machineid)

        with tarfile.open((tmpdir / 'machine-id.tar').strpath, mode='w') as archive:
            archive.add((tmpdir / 'etc').strpath, arcname='etc')

        with open((tmpdir / 'machine-id.tar').strpath, 'rb') as f:
            config['docker_client'].put_archive(config['name'], '/', f.read())

        print 'generated machine id {0} stored in /etc/machine-id'.format(machineid)
        return minion
    finally:
        tmpdir.remove()


def handler(name, signum, frame):
    client = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        sys.stdout.write("removing container {0}".format(name))
        client.remove_container(name, force=True)
    except Exception as err:
        print 'cleanup command failed: docker rm -f {0}'.format(name)
        print err.message
    finally:
        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', choices=['rhel6', 'rhel7'])
    args = parser.parse_args()
    minion = start(IMAGES[args.version])
    name = minion['container']['config']['name']
    sys.stdout.write("minion id: {0}\n".format(minion['id']))
    sys.stdout.write("container id: {0}\n".format(name))
    sys.stdout.write(
        "shell command: 'docker exec -it {0} /bin/bash'\n".format(name))
    sys.stdout.flush()
    signal.signal(signal.SIGTERM, partial(handler, name))
    signal.pause()
