# rhel-onboarding

This tool makes it easy for you to start a rhel6 and rhel7 salt minions in 2 docker containers in order to test the onboarding on SuSE Manager.

## How to

```bash
git clone git@github.com:dincamihai/rhel-onboarding.git
cd rhel-onboarding
cp .env-example .env
```

change `MASTER_IP` in `.env` to point to a SuSE Manager instance reacheble from your machine.

make sure docker service is running:
```bash
systemctl start docker
```


if you have `tox` installed you can run:
```bash
tox
```

if you don't have tox:
```bash
virtualenv sandbox
echo "*" > sandbox/.gitignore
source sandbox/bin/activate
pip install tox
```

This starts two salt minions in docker containers, one running rhel6 and the other rhel7.
You should now be able to see the minions in your SuSE Manager's web-UI.

To shut-down the minions and remove the docker containers press `CTRL-c`
