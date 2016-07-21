import os
import sys
import faker
import tempfile
import tarfile
import docker
from py.path import local
from saltcontainers.factories import MinionFactory


def create_minion(docker_client, label):
    fake = faker.Faker()
    salt_root = local(tempfile.mkdtemp())
    host_config = docker_client.create_host_config(network_mode='host')
    name = 'minion_{0}_{1}_{2}'.format(label, fake.word(), fake.word())
    return MinionFactory(
        container__config__name=name,
        container__config__docker_client=docker_client,
        container__config__image='registry.mgr.suse.de/toaster-{0}-products'.format(label),
        container__config__salt_config__id='{0}_{1}'.format(label, fake.word()),
        container__config__salt_config__tmpdir=salt_root,
        container__config__salt_config__conf_type='minion',
        container__config__salt_config__config={
            'base_config': {'master': os.environ['MASTER_IP']}
        },
        container__config__host_config=host_config
    )


def start(label):
    tmpdir = local(tempfile.mkdtemp())
    try:
        client = docker.Client(base_url='unix://var/run/docker.sock')

        minion = create_minion(client, label)

        fake = faker.Faker()
        with (tmpdir / label / 'etc' / 'machine-id').open(mode='wb', ensure=True) as f:
            f.write(fake.sha1())

        with tarfile.open((tmpdir / label / 'machine-id.tar').strpath, mode='w') as archive:
            archive.add((tmpdir / label / 'etc').strpath, arcname='etc')

        with open((tmpdir / label / 'machine-id.tar').strpath, 'rb') as f:
            minion['container']['config']['docker_client'].put_archive(
                minion['container']['config']['name'], '/', f.read())
        return minion
    finally:
        tmpdir.remove()


def handler(name, signum, frame):
    client = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        client.remove_container(name, force=True)
    except docker.errors.APIError as err:
        print 'Cleanup command failed: docker rm -f {0}'.format(name)
        print err.message
    finally:
        sys.exit(0)
