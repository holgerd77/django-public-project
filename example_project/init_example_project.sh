#!/bin/bash
while true; do
    read -p "Warning! This will reset the DB and delete modified example data. Proceed?" yn
    case $yn in
        [Yy]* )
            rm -f example_project/sqlite3.db;
            rm -Rf media/;
            rm -Rf static/;
            echo "Don't create a superuser yet on syncdb (type 'no')!";
            python manage.py syncdb;
            python manage.py migrate;
            echo "Now you can create a superuser!";
            python manage.py createsuperuser;
            echo "Creating example project data...";
            python manage.py createexampledata;
            echo "Finished. You're good to go! :-)";
            break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes (Y/y) or no (N/n).";;
    esac
done
