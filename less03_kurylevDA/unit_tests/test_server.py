import unittest
from base import *
from server import test_client_mess

class TestServer(unittest.TestCase):

    err_dict = {RESPONSE:400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE:200}

    # {ACTION: PRESENCE, TIME: time.time(), USER: {ACC_NAME: name}}
    def test_no_action(self):
        self.assertEqual(test_client_mess({TIME: '3.1', USER: {ACC_NAME: 'test'}}), self.err_dict)
    def test_no_time(self):
        self.assertEqual(test_client_mess({ACTION: PRESENCE, USER: {ACC_NAME: 'test'}}), self.err_dict)
    def test_no_user(self):
        self.assertEqual(test_client_mess({ACTION: PRESENCE, TIME: '3.1'}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(test_client_mess({ACTION: 'test', TIME: '3.1', USER: {ACC_NAME: 'test'}}), self.err_dict)
    def test_wrong_time(self):
        self.assertEqual(test_client_mess({ACTION: PRESENCE, TIME: 'test', USER: {ACC_NAME: 'test'}}), self.err_dict)
    def test_wrong_user(self):
        self.assertEqual(test_client_mess({ACTION: PRESENCE, TIME: '3.1', USER: {ACC_NAME: 123}}), self.err_dict)

    def test_correct(self):
        self.assertEqual(test_client_mess({ACTION: PRESENCE, TIME: '3.1', USER: {ACC_NAME: 'Test'}}), self.ok_dict)

if __name__ == '__main__':
    unittest.main()