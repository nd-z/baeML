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

echo -e "${GREEN}Updating pip...${BLACK}"
pip install --upgrade pip

echo -e "${GREEN}Installing Django Dependencies...${BLACK}"
pip install --upgrade Django
pip install --upgrade Djangorestframework
pip install --upgrade Django_facebook
pip install --upgrade django-cors-headers
pip install --upgrade Pillow
pip install --upgrade psycopg2
pip install --upgrade requests
pip install --upgrade django-picklefield 

echo -e "${GREEN}Installing ML Dependencies...${BLACK}"
pip install --upgrade tensorflow
pip install --upgrade sklearn
pip install --upgrade scipy
pip install --upgrade numpy
pip install --upgrade BeautifulSoup
pip install --upgrade urllib3
pip install --upgrade six
