#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLACK='\033[0;30m'

#Make sure Python 2.7 is installed.
function python_check() {
	python_version=$(python --version 2>&1)
	if [[ "$python_version" == *"Python 2.7."* ]]; then
		echo -e "${GREEN}Python Check OK${BLACK}"
	else
		echo -e "${RED}Please install Python 2.7${BLACK}"
		exit 1
	fi

}

function postgres_check() {
	postgres_installed=$(which psql)
	if [[ "$postgres_installed" == "" ]]; then
		echo -e "${RED}Please install Postgres${BLACK}"
		exit 1
	else
		echo -e "${GREEN}Postgres Check OK ${BLACK}"
	fi
}

python_check
postgres_check

echo -e "${GREEN}Installing Django Dependencies...${BLACK}"
pip install Django
pip install Djangorestframework
pip install Django_facebook
pip install django-cors-headers
pip install Pillow
pip install psycopg2

echo -e "${GREEN}Installing ML Dependencies...${BLACK}"
pip install tensorflow
pip install sklearn
pip install matplotlib
pip install scipy
pip install numpy
pip install BeautifulSoup
