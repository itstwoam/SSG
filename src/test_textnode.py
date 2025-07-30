import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        ttexts = ("This is a text node",
                  "This is also a text node"
                  )
        tttexts =(TextType.BOLD,
                 TextType.TEXT,
                 TextType.ITALIC,
                 TextType.CODE,
                 TextType.LINK,
                 TextType.IMAGE
                 )
        utexts = ("https://github.com/itstwoam/",
                  "https://boot.dev/"
                  )
        node = TextNode(ttexts[0], tttexts[0])
        node2 = TextNode(ttexts[0], tttexts[0])
        node3 = TextNode(ttexts[1], tttexts[0])
        node4 = TextNode(ttexts[0], tttexts[1])
        node5 = TextNode(ttexts[1], tttexts[0])
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node2, node4)
        self.assertEqual(node3, node5)



if __name__ == "__main__":
    unittest.main()
