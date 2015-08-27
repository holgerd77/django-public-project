#!/bin/bash
while true; do
	 echo "INFO: This script has to be run before running the tests since some tests access "
	 echo "the test server via http and needs a normal Django setup with updated DB data."
    read -p "Warning! This will reset the DB and delete modified test data. Proceed?" yn
    case $yn in
        [Yy]* )
            rm -f bpw_tests/sqlite3.db;
            rm -Rf media/;
            rm -Rf static/;
            python manage.py migrate;
            echo "Creating superuser with username 'admin'...";
            python manage.py createsuperuser --username=admin --email=d@d.de;
            echo "Creating test project data...";
				python manage.py createtestdata;
				python manage.py collectstatic --noinput;
            break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes (Y/y) or no (N/n).";;
    esac
done
