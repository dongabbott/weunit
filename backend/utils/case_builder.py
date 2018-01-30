# -*-coding:utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class_template = """# -*-coding:utf-8 -*-
import json
import unittest\n\n
class {}(unittest.TestCase):
    {}
    def setUp(self):
        pass\n
    def tearDown(self):
        pass\n
"""

function_template = """
    def {}(self):
        {}
        self.assertIsNotNone(json.loads(self.result))
        # 添加你的断言
"""


class CaseBuilder(object):

    def __init__(self, path):
        self.path = path

    def suite_build(self, suite_name, suite_desc=None):
        print suite_desc, type(suite_desc)
        desc = '"""' + '\t' + suite_desc + '"""' if suite_desc is not None else ''
        return class_template.format(suite_name, desc)

    def case_build(self, func_name, case_desc=None):
        desc = '"""' + '\t' + case_desc + '"""' if case_desc is not None else ''
        return function_template.format(func_name, desc)