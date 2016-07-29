RHEL6_DOCKRFILE = "Dockerfile.rhel6.products"
RHEL7_DOCKRFILE = "Dockerfile.rhel7.products"
SLES11SP3_DOCKRFILE = "Dockerfile.sles11sp3.products"
SLES11SP4_DOCKRFILE = "Dockerfile.sles11sp4.products"
SLES12_DOCKRFILE = "Dockerfile.sles12.products"
SLES12SP1_DOCKRFILE = "Dockerfile.sles12sp1.products"


default:
	honcho start

containers:
	honcho start -f Procfile.containers

dockerfiles:
	mkdir -p docker/
	wget -O docker/$(RHEL6_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/$(RHEL6_DOCKRFILE)
	wget -O docker/$(RHEL7_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/$(RHEL7_DOCKRFILE)
	wget -O docker/$(SLES11SP3_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/$(SLES11SP3_DOCKRFILE)
	wget -O docker/$(SLES11SP4_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/$(SLES11SP4_DOCKRFILE)
	wget -O docker/$(SLES12_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/$(SLES12_DOCKRFILE)
	wget -O docker/$(SLES12SP1_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/$(SLES12SP1_DOCKRFILE)

build:
	python -m onboarding.build --dockerfile docker/$(RHEL6_DOCKRFILE) --label rhel6
	python -m onboarding.build --dockerfile docker/$(RHEL7_DOCKRFILE) --label rhel7
	python -m onboarding.build --dockerfile docker/$(SLES11SP3_DOCKRFILE) --label sles11sp3
	python -m onboarding.build --dockerfile docker/$(SLES11SP4_DOCKRFILE) --label sles11sp4
	python -m onboarding.build --dockerfile docker/$(SLES12_DOCKRFILE) --label sles12
	python -m onboarding.build --dockerfile docker/$(SLES12SP1_DOCKRFILE) --label sles12sp1
