import unittest
from base import *
from client import cr_presen, proc_ans


class TestClient(unittest.TestCase):
    ok2_dict_cr_presen = {'action': 'presence', 'time': time.time(), 'user': {'account_name': 'Dan'}}
    ok_dict_cr_presen = {'action': 'presence', 'time': time.time(), 'user': {'account_name': 'Test'}}

    err_dict_proc_ans = '400 : error'
    ok_dict_proc_ans = '200 : OK'

    # def cr_presen(name='Test'):
    #     result = {ACTION: PRESENCE, TIME: time.time(), USER: {ACC_NAME: name}}
    #     return result

    # {ACTION: PRESENCE, TIME: time.time(), USER: {ACC_NAME: name}}
    def test_cr_presen_ok(self):
        self.assertEqual(cr_presen(), self.ok_dict_cr_presen)

    def test_cr_presen_ok2(self):
        self.assertEqual(cr_presen(name='Dan'), self.ok2_dict_cr_presen)

    def test_dict_proc_ans_ok(self):
        self.assertEqual(proc_ans(mess={RESPONSE: 200}), self.ok_dict_proc_ans)

    def test_dict_proc_ans_err(self):
        self.assertEqual(proc_ans(mess={RESPONSE: 400}), self.err_dict_proc_ans)


if __name__ == '__main__':
    unittest.main()
