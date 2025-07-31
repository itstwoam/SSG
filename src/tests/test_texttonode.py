import unittest
from htmlnode import LeafNode 
from textnode import TextNode, TextType
from functions import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_plain_text(self):
        node = TextNode("Just text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Just text")
        self.assertEqual(html_node.to_html(), "Just text")

    def test_bold_text(self):
        node = TextNode("Bold!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>Bold!</b>")

    def test_italic_text(self):
        node = TextNode("Italicized", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>Italicized</i>")

    def test_code_text(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>print('hi')</code>")

    def test_link_text(self):
        node = TextNode("Click me", TextType.LINK, url="https://example.com")
        node.props = {"href": "https://example.com"}
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(html_node.to_html(), "<a>Click me</a>")

    def test_image_node_raises(self):
        node = TextNode("", TextType.IMAGE, url="image.png")
        node.props = {"src": "image.png", "alt": "alt text"}
        with self.assertRaises(ValueError):
            text_node_to_html_node(node).to_html()
        
    def test_unknown_type_raises(self):
        class FakeType: pass
        node = TextNode("Oops", FakeType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "unkown text type")

if __name__ == "__main__":
    unittest.main()
