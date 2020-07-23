# OC-home-credit-default-risk-API

API for model prediction.

### Usage:

  * Create a virtualenv
    ```python -m virtualenv env```
  * Activate it ```source env/bin/activate```
  * Install dependencies ```pip install -r -requirements.txt```
  * You will need to copy the model and preprocessing pipeline in the models directory.
      *see OC-home-credit-default-risk repository*
  * Run test server ```python manage.py migrate``` & ```python manage.py runserver```

### Note:

  In order to run the project in production, I recommend to create a ```production.py``` module and
  override settings like DEBUG, ALLOWED_HOST, DATABASE and HTTPS management. Then you can run the project with
  this settings module using ```DJANGO_SETTINGS_MODULE``` environment variable. I also recommend to use
  gunicorn as webserver behind NGinx as reverse proxy.
