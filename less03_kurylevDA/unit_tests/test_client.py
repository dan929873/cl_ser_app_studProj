
import unittest
from base import *
from client import cr_presen, proc_ans

class TestClient(unittest.TestCase):

    err_dict_cr_presen = ''
    ok_dict_cr_presen= ''

    err_dict_proc_ans = ''
    ok_dict_proc_ans = ''

    # {ACTION: PRESENCE, TIME: time.time(), USER: {ACC_NAME: name}}
    def test_(self):
        self.assertEqual(cr_presen(), self.err_dict_cr_presen)

    def test_(self):
        self.assertEqual(proc_ans(), self.err_dict_proc_ans)