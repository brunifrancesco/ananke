# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

# [START gae_flex_websockets_app]
from flask import Flask, render_template, redirect
from flask_sockets import Sockets
import json
import random


app = Flask(__name__)
sockets = Sockets(app)

class Report:

    def __init__(self):
        self.votes = dict()

    def reset(self):
        self.votes = dict()

    def add_vote(self, value):
        data = json.loads(value)
        if 'status' in data and data['status'] == 'connection':
            self.votes[data['user']] = None
            return 
        user=data['user']
        vote=data['value'].strip()
        self.votes[user] = vote

    @property
    def sum(self):
        if self.votes:
            return sum(map(lambda item: int(item), self.votes.values()))
        return 0

    @property
    def avg(self):
        if self.sum:
            return self.sum/len(self.votes)
        return None

    @property
    def users(self):
        return list(self.votes.keys())
    
report = Report()

@sockets.route('/chat')
def chat_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        report.add_vote(message)
        # Send the message to all clients connected to this webserver
        # process. (To support multiple processes or instances, an
        # extra-instance storage or messaging system would be required.)
        clients = ws.handler.server.clients.values()
        user = json.loads(message)['user']
        for client in clients:
            client.ws.send(message)
            client.ws.send(json.dumps({'status': 'users', 'value':report.users, 'user': user}))
# [END gae_flex_websockets_app]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote/<user>')
def vote(user):
    return render_template('vote.html', user=user)


@app.route('/vote')
def landing():
    cryptos = ['Dash', 'Chainlink', 'Enjin', 'Omisego', 'Basic', 'Gnosis', 'Komodo', 'Aelf', 'diamond', 'Litecoin', '(ZRX)', 'Nxt', 'Factom', 'Dent', 'MaidSafeCoin', 'Gemini', 'Nebulas', 'Digixdao', 'Binance', 'Electroneum', 'Metal', 'Digibyte', 'Enigma', 'Quant', 'ledger', 'Dogecoin', 'Ignis', 'Qash', 'Bancor', 'classicEthereum', 'Golem', 'Bitshares', 'Holochain', 'logo', 'Aurora', 'Iota', 'logos', 'Aragon', 'Ethereum', 'PivX', 'Decentraland', 'Populous', 'Quarkchain', 'Iostoken', 'Nexo', 'Reddcoin', 'Aeternity', 'Ravencoin', 'Polymath', 'BitTorrent', 'Maker', 'Decred', 'Ardor']
    adjs = ['adorable', 'adventurous', 'aggressive', 'agreeable', 'alert', 'alive', 'amused', 'angry', 'annoyed', 'annoying', 'anxious', 'arrogant', 'ashamed', 'attractive', 'average', 'awful', 'bad', 'beautiful', 'better', 'bewildered', 'black', 'bloody', 'blue', 'blue-eyed', 'blushing', 'bored', 'brainy', 'brave', 'breakable', 'bright', 'busy', 'calm', 'careful', 'cautious', 'charming', 'cheerful', 'clean', 'clear', 'clever', 'cloudy', 'clumsy', 'colorful', 'combative', 'comfortable', 'concerned', 'condemned', 'confused', 'cooperative', 'courageous', 'crazy', 'creepy', 'crowded', 'cruel', 'curious', 'cute', 'dangerous', 'dark', 'dead', 'defeated', 'defiant', 'delightful', 'depressed', 'determined', 'different', 'difficult', 'disgusted', 'distinct', 'disturbed', 'dizzy', 'doubtful', 'drab', 'dull', 'E-K Adjectives List', 'There are plenty more often-used adjectives that start with letters in the next part of the alphabet. Review these adjective words that begin with the letters “e” through “k.”', 'eager', 'easy', 'elated', 'elegant', 'embarrassed', 'enchanting', 'encouraging', 'energetic', 'enthusiastic', 'envious', 'evil', 'excited', 'expensive', 'exuberant', 'fair', 'faithful', 'famous', 'fancy', 'fantastic', 'fierce', 'filthy', 'fine', 'foolish', 'fragile', 'frail', 'frantic', 'friendly', 'frightened', 'funny', 'gentle', 'gifted', 'glamorous', 'gleaming', 'glorious', 'good', 'gorgeous', 'graceful', 'grieving', 'grotesque', 'grumpy', 'handsome', 'happy', 'healthy', 'helpful', 'helpless', 'hilarious', 'homeless', 'homely', 'horrible', 'hungry', 'hurt', 'ill', 'important', 'impossible', 'inexpensive', 'innocent', 'inquisitive', 'itchy', 'jealous', 'jittery', 'jolly', 'joyous', 'kind', 'azy', 'light', 'lively', 'lonely', 'long', 'lovely', 'lucky', 'magnificent', 'misty', 'modern', 'motionless', 'muddy', 'mushy', 'mysterious', 'nasty', 'naughty', 'nervous', 'nice', 'nutty', 'obedient', 'obnoxious', 'odd', 'old-fashioned', 'open', 'outrageous', 'outstanding', 'panicky', 'perfect', 'plain', 'pleasant', 'poised', 'poor', 'powerful', 'precious', 'prickly', 'proud', 'putrid', 'puzzled', 'quaint', 'real', 'relieved', 'repulsive', 'rich', 'scary', 'selfish', 'shiny', 'shy', 'silly', 'sleepy', 'smiling', 'smoggy', 'sore', 'sparkling', 'splendid', 'spotless', 'stormy', 'strange', 'stupid', 'successful', 'super', 'talented', 'tame', 'tasty', 'tender', 'tense', 'terrible', 'thankful', 'thoughtful', 'thoughtless', 'tired', 'tough', 'troubled', 'ugliest', 'ugly', 'uninterested', 'unsightly', 'unusual', 'upset', 'uptight', 'vast', 'victorious', 'vivacious', 'wandering', 'weary', 'wicked', 'wide-eyed', 'wild', 'witty', 'worried', 'worrisome', 'wrong', 'zany', 'zealous']
    user = " ".join([random.choice(adjs), random.choice(cryptos)])
    return redirect("/vote/%s" %user, code=302)




@app.route('/reveal')
def reveal():
    s = report.sum
    avg = s = report.avg
    report.reset()
    return render_template('reveal.html', sum=s, avg=avg)

if __name__ == '__main__':
    print("""
This can not be run directly because the Flask development server does not
support web sockets. Instead, use gunicorn:

gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app

""")
