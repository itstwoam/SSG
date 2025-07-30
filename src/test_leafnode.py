import unittest
import itertools

from itertools import product
from htmlnode import *

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        
        tags = ["div", "span", None]
        values = ["Hello", "World"]
        #children_sets = [[], [HTMLNode("b", "Bold")], None]
        props_sets = [{}, {"class": "header"}]
        
        combinations = list(product(values, tags, props_sets))

        for i, combo1 in enumerate(combinations):
            node1 = LeafNode(*combo1)
            for j, combo2 in enumerate(combinations):
                node2 = LeafNode(*combo2)
                #print(f'node1 = {node1.to_html()}')
                if combo1 == combo2:
                    self.assertEqual(node1, node2)
                    self.assertEqual(node1.to_html(), node2.to_html())
                else:
                    self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
