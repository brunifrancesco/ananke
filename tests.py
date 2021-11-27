import unittest
import json

from room import RoomContainers, RoomNotExistingException, Room, InvalidMessageException, InvalidStatusMessageException

class RoomContainersTest(unittest.TestCase):
    
    def cleanup(self):
        RoomContainers._instance = None

    def test_singleton(self):
        room_containers = RoomContainers()
        self.assertEqual(id(room_containers), id(RoomContainers()))
        self.cleanup()

    def test_add_room_no_key(self):
        room_containers = RoomContainers()
        room = room_containers.add_room()
        self.assertNotEqual(room.container_key, None)
        self.cleanup()

    def test_add_room_key_ok(self):
        room_containers = RoomContainers()
        room = room_containers.add_room("AAAA")
        self.assertNotEqual(room, None)
        self.assertEqual(room.container_key, "AAAA")
        self.cleanup()

    def test_add_room_key_not_ok(self):
        room_containers = RoomContainers()
        room_containers.add_room("AAAA")
        room = room_containers.add_room("AAAA")
        self.assertNotEqual(room, None)
        self.assertNotEqual(room.container_key, "AAAA")
        self.cleanup()

    def test_get_room(self):
        room_containers = RoomContainers()
        rooms = room_containers.add_room(key="ABC")
        room = room_containers.get_room("ABC")
        self.assertEqual(room.container_key, "ABC")
        self.cleanup()

    def test_get_room_exception(self):
        room_containers = RoomContainers()
        rooms = room_containers.add_room(key="ABC")
        with self.assertRaises(RoomNotExistingException):
            room_containers.get_room("ABCD")
        self.cleanup()
    
    def test_remove_room(self):
        room_containers = RoomContainers()
        rooms = room_containers.add_room(key="ABC")
        room = room_containers.remove_room("ABC")
        self.assertEqual(room.container_key, "ABC")
        self.assertEqual(len(room_containers.rooms), 0)
        self.cleanup()

    def test_get_room_exception(self):
        room_containers = RoomContainers()
        rooms = room_containers.add_room(key="ABC")
        with self.assertRaises(RoomNotExistingException):
            room_containers.remove_room("ABCD")
        self.cleanup()

class RoomTest(unittest.TestCase):

    def test_new_room(self):
        room = Room("KEY")
        assert room.container_key
        assert room.votes == dict()

    def test_handle_message_no_message(self):
        room = Room("KEY")
        with self.assertRaises(InvalidMessageException):
            room.handle_message()

    def test_handle_message_no_message_status(self):
        room = Room("KEY")
        with self.assertRaises(InvalidStatusMessageException):
            room.handle_message(json.dumps({'aaa':1}))

    def test_handle_message_connect(self):
        room = Room("KEY")
        data = dict(status="connect", user="franco")

        data = room.handle_message(json.dumps(data))
        
        assert len(data) == 1
        data = json.loads(data[0])

        assert data['status'] == 'users'
        assert data['user'] == 'franco'
        assert len(room.votes) == 1

    def test_handle_message_reset(self):
        room = Room("KEY")
        data = dict(status="reset", user="franco")
        room.votes = dict(franco=None)
        data = room.handle_message(json.dumps(data))
        
        assert len(data) == 1
        data = json.loads(data[0])

        assert data['status'] == 'reset'
        assert len(room.votes) == 1
        assert room.votes['franco'] is None

    def test_handle_message_reset_all(self):
        room = Room("KEY")
        data = dict(status="reset_all", user="franco")
        room.votes = dict(franco=None)
        data = room.handle_message(json.dumps(data))
        
        assert len(data) == 1
        data = json.loads(data[0])

        assert data['status'] == 'reset'
        assert len(room.votes) == 0

    def test_handle_message_vote(self):
        room = Room("KEY")
        data = dict(status="vote", user="franco", value='2')
        room.votes = dict(franco=None)
        data = room.handle_message(json.dumps(data))
        assert room.votes['franco'] == '2'
        assert len(data) == 0
        

    def test_handle_message_disconnect(self):
        room = Room("KEY")
        data = dict(status="disconnect", user="franco")
        room.votes = dict(franco=None)
        data = room.handle_message(json.dumps(data))
        assert room.votes == dict()
        assert len(data) == 2


    def test_handle_message_block(self):
        room = Room("KEY")
        data = dict(status="block")
        room.votes = dict(franco=None)
        data = room.handle_message(json.dumps(data))
        assert len(room.votes) == 1
        assert len(data) == 1        

    def test_handle_message_reveal(self):
        room = Room("KEY")
        data = dict(status="reveal")
        room.votes = dict(franco=1, mike=2)
        data = room.handle_message(json.dumps(data))
        assert len(room.votes) == 2
        assert len(data) == 1
        print(json.loads(data[0])['value'])                
        assert json.loads(data[0])['value'] == [{'key': 1, 'value': ['franco']}, {'key':2, 'value':['mike']}]

if __name__ == '__main__':
    unittest.main()