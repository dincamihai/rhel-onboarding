RHEL6_DOCKRFILE = "Dockerfile.rhel6.products"
RHEL7_DOCKRFILE = "Dockerfile.rhel7.products"


default:
	honcho start

dockerfiles:
	wget -O docker/$(RHEL6_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/Dockerfile.rhel6.products
	wget -O docker/$(RHEL7_DOCKRFILE) https://raw.githubusercontent.com/dincamihai/dockerfiles/master/Dockerfile.rhel7.products

build:
	python -m onboarding.build --dockerfile docker/$(RHEL6_DOCKRFILE) --label rhel6
	python -m onboarding.build --dockerfile docker/$(RHEL7_DOCKRFILE) --label rhel7
