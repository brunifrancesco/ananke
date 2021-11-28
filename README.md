# Ananke: another poker planning application

A very simple application to do the poker planning.
This is a common approach to partecipate as a agile-scrum-team-member in a votation aimed to estimate the work requested for a specific User Story.

More stuff coming. Limits/bugs present.

## How it works

In order to set up the room as the *admin*, just to to */* page. A new room is automatically created.
Copy and paste the *voting link* clicking on the top-right button to let voters partecipate.
As soon as user connects to the room, you will be notified.
Once revelaead and until "resetted", no more vote will come. Reveal operation creates a summary: the admin will see how many votes for each unique value. Hovering to the vote number, you'll get the list of voters who gave that value.
To reset the votation, just click on *Reset* button.
If user leavers the room, you will be notified too.

As *user*, you need to be uniquely identified.
If you point to */vote*, a redirect will occur and a name will be generated and assigned to you.
The name follows the Docker approach and it will be composed by an adjective and a noun. But the noun would be a crypto, not a scientist as per Docker idea.
If *admin* reset the room, your vote will be notified.
To exit the room, simply close the page.

A clean up policy can delete the rooms. It's very aggressive: it simply deletes all the rooms. Just point your browser to */reset* page.
To get a summary, point to */summary* pace.

## Some tech stuff

The whole application is based on exachanging-events via websocket.
The list of supported events:

- connect, a new user has just connected to the room
- disconnect, a new user has just disconnected from the room
- reset, to reset all the votes
- reset all, to delete all the voters
- block, to block voters for submitting new votes
- reveal, to compute a summary

## How to deploy

The application can be deployed on Google App Engine platform. 
Make sure to configure your local environment, setting up the project and deploy it via Google Cloud SDK CLI.

## What's missing

- Multi team support with smarter cleanup of closed rooms
- Docstrings
- Some Tests
- Any UI improvement

## Install dependencies


Supposing you have python3.6 (or above) installed:
    
    $ python3.6 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

Before start working, have the virtual environment activated.


## Running locally


To run locally, you need to use gunicorn with the ``flask_socket`` worker:

    $ gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app

Point to *http://localhost:8080* to access to the main page.

## Running tests

    $ python tests.py
