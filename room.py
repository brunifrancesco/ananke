from collections import defaultdict
from itertools import groupby 
import random
import string
import json
from datetime import datetime, timedelta

class RoomNotExistingException(Exception):
    pass

class InvalidMessageException(Exception):
    pass

class InvalidStatusMessageException(Exception):
    pass


class RoomContainers:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RoomContainers, cls).__new__(cls)
            cls._instance.rooms = dict()
        return cls._instance

    def handle_message(self, message):
        data = json.loads(message)
        if not message:
            raise InvalidMessageException("No message when handling it: => %s" %message)

        if not 'room_key' in data or not data['room_key']:
            raise InvalidMessageException("No room_key in message => %s" %message)

        return self.get_room(data['room_key']).handle_message(message)

    def add_room(self, key=None):
        """Add room with optional provided key; ovveride if exists.
        
        Args:
            key (str): key room
        
        Returns:
            TYPE: Description
        """
        if not key or key in self.rooms.keys():
            key = result_str = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        self.rooms[key] = Room(key)
        return self.rooms[key]

    def remove_room(self, key: str):
        """Remove room from container
        
        Args:
            key (str): room key
        
        Raises:
            RoomNotExistingException: room key does not exist
        """
        room = self.rooms.pop(key, None)
        if not room:
            raise RoomNotExistingException("No room with provided key %s" %key)

        return room

    def get_room(self, key):
        """
        Get room by key
        Args:
            key (str): Description
        
        Raises:
            RoomNotExistingException: room key does not exist
        """
        room = self.rooms.get(key, None)
        if not room:
            raise RoomNotExistingException("No room with provided key %s" %key)
        return room

    def delete_rooms(self):
        """Delete all rooms
        """
        self.rooms = dict()


    def get_rooms(self):
        """Get all rooms as key,value pairs
        """
        return self.rooms.items()

class Room:

    def __init__(self, key):
        self.container_key = key
        self.start_time = datetime.now()
        self.votes = dict()

    def __add_user(self, user):
        self.votes[user] = None
        return self.votes

    def __add_vote(self, user, vote):
        self.votes[user] = vote.strip()
        return self.votes

    def __reset(self):
        print(self.votes)
        self.votes.fromkeys(self.votes, None)
        print(self.votes)

    def __reset_all(self):
        self.votes = dict()

    def __disconnect_user(self, user):
       return  self.votes.pop(user)

    def __compute_report(self):
        v = defaultdict(list)
        for key, value in sorted(self.votes.items()):
          v[value].append(key)
        return [dict(key=key, value=v[key]) for key, value in v.items()]

    def handle_message(self, value=None):
        if not value:
           raise InvalidMessageException("Message is none")
 
        data = json.loads(value)
        
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
        if 'status' in data and data['status'] == 'reveal':
            report = self.__compute_report()
            return [
                json.dumps({'status': 'report', 'value':report, 'user': None}),
            ] 
        raise InvalidStatusMessageException("No correct status %s" %data.get('status', None))
    
    @property
    def users(self):
        return list(self.votes.values())