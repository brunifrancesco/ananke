# Ananke: another poker planning application

A very simple application to do the single-team poker planning.
This is a common approach to partecipate as a agile-scrum-team-member in a votation aimed to estimate the work requested for a specific User Story.

More stuff coming. Limits/bugs present. *How it works* section does not describe the current state of work.

## How it works

In order to set up the room as the *admin*, just to to */* page.
As soon as user connects to the room, you will be notified.
To reset the votation, just click on *Reset* button.
If user leavers the room, you will be notified too.

As *user*, you need to be uniquely identified.
If you point to */vote*, a redirect will occur and a name will be generated and assigned to you.
The name follows the Docker approach and it will be composed by an adjective and a noun. But the noun would be a crypto, not a scientist as per Docker idea.
If *admin* reset the room, your vote will be canceled.
To exit the room, please do not simply close the page. Click on *Disconnect* first.

## Install dependencies


Supposing you have python3.6 (or above) installed:
    
    $ python3.6 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Before start working, have the virtual environment activated.


## Running locally


To run locally, you need to use gunicorn with the ``flask_socket`` worker:

    $ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app
