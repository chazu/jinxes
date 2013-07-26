import json
import sys
import unittest

sys.path.append("./..")

from widget import Widget
from util import *

class TestCacheStateAtPath(unittest.TestCase):

    def setUp(self):
        self.json = json.load(open("./../tui.json"))

    def test_cache_state_at_path_array(self):
        test_text = "foo"
        test_path = ["contents","text"]

        widget = Widget(None, self.json["widgets"][0])

        original_value = multiIndex(widget.cached_state, test_path)
        widget.current_state["contents"]["text"] = test_text
        self.assertNotEqual(original_value, test_text)
        self.assertEqual(widget.current_state["contents"]["text"], test_text)
        widget.cache_state_at_path(test_path)

        self.assertEqual(widget.cached_state["contents"]["text"], test_text)


if __name__ == "__main__":

    unittest.main()
