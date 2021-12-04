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
        """Handle incoming message
        
        Args:
            message (str): the incoming message
        
        Returns:
            TYPE: list of to-be-sent messages
        
        Raises:
            InvalidMessageException: received message is not valid
        """
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
        """Add new user
        
        Args:
            user (TYPE): the user to be added
        
        Returns:
            dict: the current votes
        """
        self.votes[user] = None
        return self.votes

    def __add_vote(self, user, vote):
        """Set vote for user
        
        Args:
            user (TYPE): the incoming user
            vote (TYPE): the vote
        
        Returns:
            dict: The update voting data
        """
        self.votes[user] = vote.strip()
        return self.votes

    def __reset(self):
        """Set all votes to None
        """
        self.votes.fromkeys(self.votes, None)
        

    def __reset_all(self):
        """Reset votes and users
        """
        self.votes = dict()

    def __disconnect_user(self, user):
       """Remove user from the current room
       
       Args:
           user (str): the current user
       
       Returns:
           dict: the updated voting data
       """
       return  self.votes.pop(user)

    def __compute_report(self):
        """For each vote receive, compute a simple report to get 
        how many votes were received for each value
        
        Returns:
            TYPE: a list of mapping, one per vote value
        """
        v = defaultdict(list)
        for key, value in sorted(self.votes.items()):
          v[value].append(key)
        return [dict(key=key, value=v[key]) for key, value in v.items()]

    def handle_message(self, value=None):
        """Handle message by case
        
        Args:
            value (None, optional): the incoming message
        
        Returns:
            list: A list of messages to be sent
        
        Raises:
            InvalidMessageException: invalid message
            InvalidStatusMessageException: no 'status' key in message, unprocessable
        """
        if not value:
           raise InvalidMessageException("Message is none")
 
        data = json.loads(value)

        
        # add user to room
        if 'status' in data and data['status'] == 'connect':
            self.__add_user(data['user'])
            return [json.dumps({'room_key': data['room_key'], 'status': 'users', 'value':self.users, 'user': data['user']})]
        
        # reset votes
        if 'status' in data and data['status'] == 'reset':
            self.__reset()
            return [json.dumps({'room_key': data['room_key'], 'status': 'reset', 'value': None, 'user': data['user']})]

        # reset all
        if 'status' in data and data['status'] == 'reset_all':
            self.__reset_all()
            return [json.dumps({'room_key': data['room_key'], 'status': 'reset', 'value': 'all', 'user': data['user']})]
        
        # add vote
        if 'status' in data and data['status'] == 'vote':
            self.__add_vote(data['user'], data['value'])
            return []
        
        # user disconnect
        if 'status' in data and data['status'] == 'disconnect':
            self.__disconnect_user(data['user'])
            return [
                json.dumps({'room_key': data['room_key'], 'status': 'disconnect', 'value':data['user'], 'user': data['user']}),
                json.dumps({'room_key': data['room_key'], 'status': 'users', 'value':self.users, 'user': data['user']})
            ]

        if 'status' in data and data['status'] == 'block':
            return [
                json.dumps({'room_key': data['room_key'], 'status': 'block', 'value':None, 'user': None}),
            ] 
        if 'status' in data and data['status'] == 'reveal':
            report = self.__compute_report()
            return [
                json.dumps({'room_key': data['room_key'], 'status': 'report', 'value':report, 'user': None}),
            ] 
        raise InvalidStatusMessageException("No correct status %s" %data.get('status', None))
    
    @property
    def users(self):
        return list(self.votes.values())