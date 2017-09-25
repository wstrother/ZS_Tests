from unittest import TestCase
import src.cfg as cfg
from json import dumps
import os

example_cfg = """
# data

Test Cfg
\tinteger: 1
\tstring1: "Hey, this isn't not a string"
\tstring2: another string here
\tlist: 1, 2, meow
\tfloat: 3.01
\tsingle_element_list: hello,
\tbool_false: false
\tbool_true

# items

Hello World
\ta_description: "Hi, It's an example of CFG data syntax for ZSquirrel"
\tb_test_value: 1.3
\tc_test_list: 1, 2, 3, 4
\td_single_element_list: "one",

Squirrel
\tname: Slavoj
"""

example_json = {
    "data": {
        "Test Cfg": {
            "integer": 1,
            "string1": "Hey, this isn't not a string",
            "string2": "another string here",
            "list": [1, 2, "meow"],
            "float": 3.01,
            "single_element_list": ["hello"],
            "bool_false": False,
            "bool_true": True
        }
    },
    "items": {
        "Hello World": {
            "a_description": "Hi, It's an example of CFG data syntax for ZSquirrel",
            "b_test_value": 1.3,
            "c_test_list": [1, 2, 3, 4],
            "d_single_element_list": ["one"]
        },
        "Squirrel": {
            "name": "Slavoj"
        }
    }
}


class TestCfg(TestCase):
    @classmethod
    def setUpClass(cls):
        file = open("test.cfg", "w")
        file.write(example_cfg)
        file.close()

        cls.example_text = example_cfg
        cls.example_json = example_json
        cls.cfg_1 = cfg.load_cfg("test.cfg")

        json_str = dumps(cls.cfg_1)
        file = open("test.json", "w")
        file.write(json_str)
        file.close()

    @classmethod
    def tearDownClass(cls):
        files = [
            "test.cfg",
            "test.json",
            "test1.cfg",
            "test1.json"
        ]
        for name in files:
            if os.path.isfile(name):
                os.remove(name)

    def test_items(self):
        data = self.cfg_1["data"]["Test Cfg"]
        json = self.example_json["data"]["Test Cfg"]

        for arg in data:
            self.assertEqual(
                type(json[arg]), type(data[arg])
            )
            self.assertEqual(
                json[arg], data[arg]
            )

    def test_sections(self):
        section = self.cfg_1["items"]
        json = self.example_json["items"]
        self.assertEqual(
            section["Hello World"],
            json["Hello World"]
        )
        self.assertEqual(
            section["Squirrel"],
            json["Squirrel"]
        )

    def test_cfg(self):
        json = self.example_json
        self.assertEqual(
            self.cfg_1, json
        )

        cfg.save_cfg(self.cfg_1, "test1.cfg")
        test_cfg = cfg.load_cfg("test1.cfg")
        self.assertEqual(
            json, test_cfg
        )

    def test_json(self):
        json = self.example_json
        cfg.save_json(self.cfg_1, "test1.json")
        test_json = cfg.load_json("test1.json")
        self.assertEqual(
            json, test_json
        )

