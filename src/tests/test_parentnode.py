import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):

    def test_valid_node(self):
        child1 = LeafNode("Hello", tag="span")
        child2 = LeafNode("World", tag="b")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(), 
            "<div><span>Hello</span><b>World</b></div>"
        )

    def test_missing_tag(self):
        child = LeafNode("Content", tag="p")
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [child]).to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have a tag!")

    def test_missing_children(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("section", None).to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have at least one child!")

    def test_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("ul", []).to_html()

    def test_child_html_accuracy(self):
        child1 = LeafNode("123", "code")
        child2 = LeafNode("456", "kbd")
        parent = ParentNode("div", [child1, child2])
        output = parent.to_html()
        self.assertIn("<code>123</code>", output)
        self.assertIn("<kbd>456</kbd>", output)

if __name__ == "__main__":
    unittest.main()
