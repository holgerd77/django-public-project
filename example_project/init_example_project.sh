#!/bin/bash
while true; do
    read -p "Warning! This will reset the DB and delete modified example data. Proceed?" yn
    case $yn in
        [Yy]* )
            rm -f example_project/sqlite3.db;
            rm -Rf media/;
            rm -Rf static/;
            python manage.py migrate;
            echo "Creating superuser with username 'admin'...";
            python manage.py createsuperuser --username=admin --email=d@d.de;
            echo "Creating example project data...";
				python manage.py createexampledata;
            python manage.py collectstatic --noinput;
            break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes (Y/y) or no (N/n).";;
    esac
done
