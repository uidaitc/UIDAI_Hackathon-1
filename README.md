# UIDAI_Hackathon

This is an appointment booking webapp made with django.

### Live Demo : [![UIDAI Hackathon](./core/static/images/favicon.ico)](https://github.com/Rajarshi07/UIDAI_Hackathon)


## Technology Stack

1. HTML5
2. CSS3
3. JS
4. Django
5. Python 3.8


## Dependencies

- asgiref==3.4.1
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.7
- cryptography==35.0.0
- Django==3.2.8
- http-ece==1.1.0
- idna==3.3
- pycparser==2.20
- python-dateutil==2.8.2
- pytz==2021.3
- requests==2.26.0
- six==1.16.0
- sqlparse==0.4.2
- urllib3==1.26.7

## Setup

**Run the following commands to get up and running**

1. `python3 -m pip install virtualenv`
2. `python3 -m virtualenv venv -p python3.8`
3. `source venv/bin/activate`
3. `cd core`
4. `python3 -m pip install -r requirements.txt`
5. `python3 manage.py collectstatic`
6. `python3 manage.py makemigrations`
7. `python3 manage.py migrate`
8. `python3 manage.py createsuperuser`
9. `python3 manage.py runserver`