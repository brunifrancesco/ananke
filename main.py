from __future__ import print_function

from flask import Flask, render_template, redirect, request
from flask_sockets import Sockets
import json
import random


app = Flask(__name__)
sockets = Sockets(app)


class Room:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Room, cls).__new__(cls)
            cls._instance.votes = dict()
        return cls._instance

    def __add_user(self, user):
        self.votes[user] = None
        return self.votes

    def __add_vote(self, user, vote):
        self.votes[user] = vote.strip()
        return self.votes

    def __reset(self):
        return self.votes.fromkeys(self.votes, None)

    def __reset_all(self):
        self.votes = dict()

    def __disconnect_user(self, user):
       return  self.votes.pop(user)

    def handle_message(self, value):
        data = json.loads(value)
        print("----------------")
        print(data)
        print("----------------")
        
        # add user to room
        if 'status' in data and data['status'] == 'connect':
            self.__add_user(data['user'])
            return [json.dumps({'status': 'users', 'value':self.users, 'user': data['user']})]
        
        # reset votes
        if 'status' in data and data['status'] == 'reset':
            self.__reset()
            return [json.dumps({'status': 'reset', 'value': None, 'user': data['user']})]

        # reset all
        if 'status' in data and data['status'] == 'reset_all':
            self.__reset_all()
            return [json.dumps({'status': 'reset', 'value': 'all', 'user': data['user']})]
        
        # add vote
        if 'status' in data and data['status'] == 'vote':
            self.__add_vote(data['user'], data['value'])
            return []
        
        # user disconnect
        if 'status' in data and data['status'] == 'disconnect':
            self.__disconnect_user(data['user'])
            return [
                json.dumps({'status': 'disconnect', 'value':data['user'], 'user': data['user']}),
                json.dumps({'status': 'users', 'value':self.users, 'user': data['user']})
            ]

        if 'status' in data and data['status'] == 'block':
            return [
                json.dumps({'status': 'block', 'value':None, 'user': None}),
            ] 

    @property
    def sum(self):
        if self.votes:
            digits = filter(lambda item: item.isdigit(), self.votes.values)
            return sum(map(int, digits))
        return 0

    @property
    def avg(self):
        if self.sum:
            return self.sum/len(self.votes)
        return None

    @property
    def grades(self):
        return list(self.votes.keys())
    
    @property
    def users(self):
        return list(self.votes.values())

@sockets.route('/exchange')
def chat_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        result = Room().handle_message(message)
        
        clients = ws.handler.server.clients.values()
        user = json.loads(message)['user']
        for client in clients:
            client.ws.send(message)
            for action in result:
                client.ws.send(action)


@app.route('/')
def index():
    room = Room()
    return render_template('index.html', host=request.host)

@app.route('/2')
def index2():
    room = Room()
    return render_template('index2.html')

@app.route('/vote/<user>')
def vote(user):
    return render_template('vote.html', user=user)


@app.route('/vote')
def landing():
    cryptos = ['Dash', 'Chainlink', 'Enjin', 'Omisego', 'Basic', 'Gnosis', 'Komodo', 'Aelf', 'diamond', 'Litecoin', '(ZRX)', 'Nxt', 'Factom', 'Dent', 'MaidSafeCoin', 'Gemini', 'Nebulas', 'Digixdao', 'Binance', 'Electroneum', 'Metal', 'Digibyte', 'Enigma', 'Quant', 'ledger', 'Dogecoin', 'Ignis', 'Qash', 'Bancor', 'classicEthereum', 'Golem', 'Bitshares', 'Holochain', 'logo', 'Aurora', 'Iota', 'logos', 'Aragon', 'Ethereum', 'PivX', 'Decentraland', 'Populous', 'Quarkchain', 'Iostoken', 'Nexo', 'Reddcoin', 'Aeternity', 'Ravencoin', 'Polymath', 'BitTorrent', 'Maker', 'Decred', 'Ardor']
    adjs = ['adorable', 'adventurous', 'aggressive', 'agreeable', 'alert', 'alive', 'amused', 'angry', 'annoyed', 'annoying', 'anxious', 'arrogant', 'ashamed', 'attractive', 'average', 'awful', 'bad', 'beautiful', 'better', 'bewildered', 'black', 'bloody', 'blue', 'blue-eyed', 'blushing', 'bored', 'brainy', 'brave', 'breakable', 'bright', 'busy', 'calm', 'careful', 'cautious', 'charming', 'cheerful', 'clean', 'clear', 'clever', 'cloudy', 'clumsy', 'colorful', 'combative', 'comfortable', 'concerned', 'condemned', 'confused', 'cooperative', 'courageous', 'crazy', 'creepy', 'crowded', 'cruel', 'curious', 'cute', 'dangerous', 'dark', 'dead', 'defeated', 'defiant', 'delightful', 'depressed', 'determined', 'different', 'difficult', 'disgusted', 'distinct', 'disturbed', 'dizzy', 'doubtful', 'drab', 'dull', 'eager', 'easy', 'elated', 'elegant', 'embarrassed', 'enchanting', 'encouraging', 'energetic', 'enthusiastic', 'envious', 'evil', 'excited', 'expensive', 'exuberant', 'fair', 'faithful', 'famous', 'fancy', 'fantastic', 'fierce', 'filthy', 'fine', 'foolish', 'fragile', 'frail', 'frantic', 'friendly', 'frightened', 'funny', 'gentle', 'gifted', 'glamorous', 'gleaming', 'glorious', 'good', 'gorgeous', 'graceful', 'grieving', 'grotesque', 'grumpy', 'handsome', 'happy', 'healthy', 'helpful', 'helpless', 'hilarious', 'homeless', 'homely', 'horrible', 'hungry', 'hurt', 'ill', 'important', 'impossible', 'inexpensive', 'innocent', 'inquisitive', 'itchy', 'jealous', 'jittery', 'jolly', 'joyous', 'kind', 'azy', 'light', 'lively', 'lonely', 'long', 'lovely', 'lucky', 'magnificent', 'misty', 'modern', 'motionless', 'muddy', 'mushy', 'mysterious', 'nasty', 'naughty', 'nervous', 'nice', 'nutty', 'obedient', 'obnoxious', 'odd', 'old-fashioned', 'open', 'outrageous', 'outstanding', 'panicky', 'perfect', 'plain', 'pleasant', 'poised', 'poor', 'powerful', 'precious', 'prickly', 'proud', 'putrid', 'puzzled', 'quaint', 'real', 'relieved', 'repulsive', 'rich', 'scary', 'selfish', 'shiny', 'shy', 'silly', 'sleepy', 'smiling', 'smoggy', 'sore', 'sparkling', 'splendid', 'spotless', 'stormy', 'strange', 'stupid', 'successful', 'super', 'talented', 'tame', 'tasty', 'tender', 'tense', 'terrible', 'thankful', 'thoughtful', 'thoughtless', 'tired', 'tough', 'troubled', 'ugliest', 'ugly', 'uninterested', 'unsightly', 'unusual', 'upset', 'uptight', 'vast', 'victorious', 'vivacious', 'wandering', 'weary', 'wicked', 'wide-eyed', 'wild', 'witty', 'worried', 'worrisome', 'wrong', 'zany', 'zealous']
    user = " ".join([random.choice(adjs), random.choice(cryptos)])
    return redirect("/vote/%s" %user, code=302)