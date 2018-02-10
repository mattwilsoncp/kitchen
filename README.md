# iotprojects
Python/Django IOT Code
I develop on a Windows 10 machine.  The production server is Ubuntu 16 LTS.

On server (Ubuntu 16):
* sudo apt-get update
* sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3

Apache2 Setup:
* vi /etc/apache2/sites-available/000-default.conf

```
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /source/django/iotprojects/iot>
          <Files wsgi.py>
            Require all granted
          </Files>
        </Directory>

        WSGIDaemonProcess iot python-home=/source/django/iotprojects/env python-path=/source/django/iotprojects
        WSGIProcessGroup iot
        WSGIScriptAlias / /source/django/iotprojects/iot/wsgi.py
</VirtualHost>
```

Change to your source directory:
* virutalenv -p python3 env
* source env/bin/activate
* pip install django
* pip install social-auth-app-django
* pip install django-widget-tweaks
* pip install psycopg2
* pip install --upgrade google-api-python-client
* pip install gspread
