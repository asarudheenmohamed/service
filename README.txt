1. Run and ihnstall the base packages

sudo apt-get install build-essential nginx python-dev python-pip python-sqlite sqlite

2. From the current directory, run the following 
   > pip install -r requirements.txt

3. To create the ncessary tables, create a database named "services"

mysql> CREATE DATABASE services;

4. Make sure the magento database name in correct in the following file

<PROJECT_DIR>/config/settings/local.py

5. Once done with 4&5 create the tables using the follwoing command
python manage.py migrate

6. Finally start the APP with the following
PROJECT_APP/tendercuts> python manage.py runserver --settings config.settings.local
