from __future__ import print_function


from flask import Flask, render_template, redirect, request
from flask_sockets import Sockets
import json

import random
import string
import json
from slugify import slugify

from room import RoomContainers, RoomNotExistingException


app = Flask(__name__)
sockets = Sockets(app)


@app.route('/summary')
def summary():

    return json.dumps([{key_room: value.votes, 'start_time': value.start_time.strftime("%m/%d/%Y, %H:%M:%S")} for key_room, value in RoomContainers().get_rooms()])

@app.route('/reset')
def reset():
    RoomContainers().delete_rooms()
    return "Done"

@app.route('/')
def index():
    room = RoomContainers().add_room()
    return redirect("/rooms/%s" %room.container_key, code=302)

@app.route('/rooms/<room_key>')
def rooms(room_key):
    return render_template('index.html', host=request.host, scheme=request.scheme, room_key=room_key)

@app.route('/rooms/<room_key>/users/<user>/')
def vote(room_key, user):
    try:
        RoomContainers().get_room(room_key)
    except RoomNotExistingException:
        return render_template('noroom.html')
    return render_template('vote.html', user=user, room_key=room_key)


@app.route('/rooms/<room_key>/users')
def landing(room_key):
    try:
        RoomContainers().get_room(room_key)
    except RoomNotExistingException:
        return render_template('noroom.html')
    cryptos = ['Dash', 'Chainlink', 'Enjin', 'Omisego', 'Basic', 'Gnosis', 'Komodo', 'Aelf', 'diamond', 'Litecoin', 'Nxt', 'Factom', 'Dent', 'MaidSafeCoin', 'Gemini', 'Nebulas', 'Digixdao', 'Binance', 'Electroneum', 'Metal', 'Digibyte', 'Enigma', 'Quant', 'ledger', 'Dogecoin', 'Ignis', 'Qash', 'Bancor', 'classicEthereum', 'Golem', 'Bitshares', 'Holochain', 'logo', 'Aurora', 'Iota', 'logos', 'Aragon', 'Ethereum', 'PivX', 'Decentraland', 'Populous', 'Quarkchain', 'Iostoken', 'Nexo', 'Reddcoin', 'Aeternity', 'Ravencoin', 'Polymath', 'BitTorrent', 'Maker', 'Decred', 'Ardor']
    adjs = ['adorable', 'adventurous', 'aggressive', 'agreeable', 'alert', 'alive', 'amused', 'angry', 'annoyed', 'annoying', 'anxious', 'arrogant', 'ashamed', 'attractive', 'average', 'awful', 'bad', 'beautiful', 'better', 'bewildered', 'black', 'bloody', 'blue', 'blue-eyed', 'blushing', 'bored', 'brainy', 'brave', 'breakable', 'bright', 'busy', 'calm', 'careful', 'cautious', 'charming', 'cheerful', 'clean', 'clear', 'clever', 'cloudy', 'clumsy', 'colorful', 'combative', 'comfortable', 'concerned', 'condemned', 'confused', 'cooperative', 'courageous', 'crazy', 'creepy', 'crowded', 'cruel', 'curious', 'cute', 'dangerous', 'dark', 'dead', 'defeated', 'defiant', 'delightful', 'depressed', 'determined', 'different', 'difficult', 'disgusted', 'distinct', 'disturbed', 'dizzy', 'doubtful', 'drab', 'dull', 'eager', 'easy', 'elated', 'elegant', 'embarrassed', 'enchanting', 'encouraging', 'energetic', 'enthusiastic', 'envious', 'evil', 'excited', 'expensive', 'exuberant', 'fair', 'faithful', 'famous', 'fancy', 'fantastic', 'fierce', 'filthy', 'fine', 'foolish', 'fragile', 'frail', 'frantic', 'friendly', 'frightened', 'funny', 'gentle', 'gifted', 'glamorous', 'gleaming', 'glorious', 'good', 'gorgeous', 'graceful', 'grieving', 'grotesque', 'grumpy', 'handsome', 'happy', 'healthy', 'helpful', 'helpless', 'hilarious', 'homeless', 'homely', 'horrible', 'hungry', 'hurt', 'ill', 'important', 'impossible', 'inexpensive', 'innocent', 'inquisitive', 'itchy', 'jealous', 'jittery', 'jolly', 'joyous', 'kind', 'azy', 'light', 'lively', 'lonely', 'long', 'lovely', 'lucky', 'magnificent', 'misty', 'modern', 'motionless', 'muddy', 'mushy', 'mysterious', 'nasty', 'naughty', 'nervous', 'nice', 'nutty', 'obedient', 'obnoxious', 'odd', 'old-fashioned', 'open', 'outrageous', 'outstanding', 'panicky', 'perfect', 'plain', 'pleasant', 'poised', 'poor', 'powerful', 'precious', 'prickly', 'proud', 'putrid', 'puzzled', 'quaint', 'real', 'relieved', 'repulsive', 'rich', 'scary', 'selfish', 'shiny', 'shy', 'silly', 'sleepy', 'smiling', 'smoggy', 'sore', 'sparkling', 'splendid', 'spotless', 'stormy', 'strange', 'stupid', 'successful', 'super', 'talented', 'tame', 'tasty', 'tender', 'tense', 'terrible', 'thankful', 'thoughtful', 'thoughtless', 'tired', 'tough', 'troubled', 'ugliest', 'ugly', 'uninterested', 'unsightly', 'unusual', 'upset', 'uptight', 'vast', 'victorious', 'vivacious', 'wandering', 'weary', 'wicked', 'wide-eyed', 'wild', 'witty', 'worried', 'worrisome', 'wrong', 'zany', 'zealous']
    user = slugify(" ".join([random.choice(adjs), random.choice(cryptos)]))
    return redirect("/rooms/%s/users/%s" %(room_key, user), code=302)


@sockets.route('/exchange')
def chat_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        print(message)
        result = RoomContainers().handle_message(message)
        
        clients = ws.handler.server.clients.values()
        for client in clients:
            client.ws.send(message)
            for action in result:
                client.ws.send(action)