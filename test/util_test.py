import json
import sys
import unittest

sys.path.append("./..")

from util import *

class TestMultiIndexAssign(unittest.TestCase):

    def setUp(self):
        self.data = {"a":
                         {"b":
                              {"c": "foo"},
                          },
                     }

    def test_assigns_to_nested_hash_key(self):
        self.assertEqual(self.data["a"]["b"]["c"], "foo")

        multiIndexAssign(self.data, ["a","b","c"], "bar")
        self.assertEqual(self.data["a"]["b"]["c"], "bar")

    def test_assigns_to_top_level_hash_key(self):
        self.assertEqual(self.data["a"], {"b": {"c": "foo"}})

        multiIndexAssign(self.data, ["a"], "bar")
        self.assertEqual(self.data["a"], "bar")

    def test_accepts_string_instead_of_array(self):
        self.assertEqual(self.data["a"], {"b": {"c": "foo"}})

        multiIndexAssign(self.data, "a", "bar")
        self.assertEqual(self.data["a"], "bar")


if __name__ == "__main__":
    unittest.main()
