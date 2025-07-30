import unittest
import itertools

from itertools import product
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        
        tags = ["div", "span", None]
        values = ["Hello", "World", None]
        children_sets = [[], [HTMLNode("b", "Bold")], None]
        props_sets = [{}, {"class": "header"}, None]
        
        combinations = list(product(tags, values, children_sets, props_sets))

        for i, combo1 in enumerate(combinations):
            node1 = HTMLNode(*combo1)
            for j, combo2 in enumerate(combinations):
                node2 = HTMLNode(*combo2)
                if combo1 == combo2:
                    self.assertEqual(node1, node2)
                else:
                    self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
