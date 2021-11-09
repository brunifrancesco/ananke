# Ananke: another poker planning application

A very simple application to do the single-team poker planning.
More stuff coming. Limits/bugs present.

## Install dependencies


Supposing you have python3.6 (or above) installed:
    
    $ python3.6 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Before start working, have the virtual environment activated.


## Running locally


To run locally, you need to use gunicorn with the ``flask_socket`` worker:

    $ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app
