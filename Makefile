default:
	honcho start


build:
	python -m onboarding.build --version rhel6 --flavor products
	python -m onboarding.build --version rhel7 --flavor products
