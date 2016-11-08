# Personal-Finance-Django-App
Django application for tracking personal finances.
Tested with Python 3.5.2

##Dependancies
- django-polymorphic
- django-mathfilters

##Needed files
You will have to create a settings.json file in the /banking/banking folder and add your desired local settings.
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- DATABASES SETTINGS (DB_Engine, DB_Name, DB_Host, DB_User, DB_Password).

Example settings.json

    {
    "Filename": "settings.json",
    "Debug": "T",
    "Secret_Key": "putyoursecretkeyhere",
    "DB_Engine": "django.db.backends.sqlite3",
    "DB_Name": "C:\\srv\\www\\finance\\banking\\db.sqlite3",
    "DB_User": "",
    "DB_Password": "",
    "DB_Host": "",
    "Host": "127.0.0.1"
    }

##Note
**Accounts**'s and **Transaction Categories** have to be added through the django admin page.
