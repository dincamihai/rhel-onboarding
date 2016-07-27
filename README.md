# rhel-onboarding

This tool makes it easy for you to start a rhel6 and rhel7 salt minions in 2 docker containers in order to test the onboarding on SuSE Manager.

## How to

- install python-docker-py linux package (eg: with sudo zypper in python-docker-py)

- ```bash
git clone git@github.com:dincamihai/rhel-onboarding.git
cd rhel-onboarding
virtualenv sandbox --system-site-packages
source sandbox/bin/activate
pip install -e .
cp .env-example .env
```

change `MASTER_IP` in `.env` to point to a SuSE Manager instance reachable from your machine.

make sure docker service is running:
```bash
systemctl start docker
```

obtain the dockerfiles:
```bash
make dockerfiles
```

build docker images:
```bash
make build
```

start rhel6 and rhel7 minions:
```bash
make
```

The output looks like this:
```bash
13:18:59 system  | rhel7.1 started (pid=7061)
13:18:59 system  | rhel6.1 started (pid=7062)
13:19:02 rhel6.1 | minion id: id_nzinu
13:19:02 rhel6.1 | container id: container_qIXax
13:19:02 rhel6.1 | shell command: 'docker exec -it container_qIXax /bin/bash'
13:19:02 rhel6.1 | generated machine id 3736cdcf1be6ffe6932e82eaef822ce963b98f4e stored in /etc/machine-id
13:19:03 rhel7.1 | minion id: id_DTjnb
13:19:03 rhel7.1 | container id: container_IjmHb
13:19:03 rhel7.1 | shell command: 'docker exec -it container_IjmHb /bin/bash'
13:19:03 rhel7.1 | generated machine id a64b4e7ca8e85b25541f1aef6c37ae014410ac10 stored in /etc/machine-id
```

This starts two salt minions in docker containers, one running rhel6 and the other rhel7.
You should now be able to see the minions in your SuSE Manager's web-UI.

To shut-down the minions and remove the docker containers press `CTRL-c`
```bash
^C13:27:16 system  | SIGINT received
13:27:16 system  | sending SIGTERM to rhel7.1 (pid 7061)
13:27:16 system  | sending SIGTERM to rhel6.1 (pid 7062)
13:27:18 rhel7.1 | removing container container_IjmHb
13:27:18 system  | rhel7.1 stopped (rc=0)
13:27:19 rhel6.1 | removing container container_qIXax
13:27:19 system  | rhel6.1 stopped (rc=0)
make: *** [Makefile:6: default] Error 130
```
