# -*-coding:utf-8 -*-
import os


class CaseBuilder(object):

    def __init__(self, path, suite_name, func_name):
        self.path = path
        self.suite_name = suite_name
        self.func_name = suite_name





class_template = """# -*-coding:utf-8 -*-
import json
import unittest\n\n
class {}(unittest.TestCase):
"""

function_template = """
    def setUp(self):
        pass\n
    def tearDown():
        pass\n
    def {}(self):
        {}
        self.assertIsNotNone(json.loads(self.result))
        # 添加你的断言
"""


class DataTemplate(object):

    def case_builder(self, case_data, suite_name, suite_dir='./'):
        """
        用于生成测试用例文件
        :param suite_dir: 测试用例文件目录
        :return:
        """
        fun = ''
        for case_func in case_data.keys():
            desc = case_data.get(case_func).get("desc")
            desc = '"""' + '\t' + desc.encode("utf-8") + '"""' if desc is not None else ''
            fun += function_template.format(case_func, desc)
        case_file_path = os.path.join(suite_dir, suite_name + '.py')
        with open(case_file_path, 'wb') as f:
            f.write(class_template.format(suite_name) + fun)