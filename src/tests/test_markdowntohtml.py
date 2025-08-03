import unittest
from textnode import TextNode
from htmlnode import ParentNode
from enums import BlockType
from functions import (
    markdown_to_html_node,
    paragraph_from_block,
    heading_from_block,
    quote_from_block,
    code_from_block,
    list_from_block,
    olist_from_block
)

class TestMarkdownConverter(unittest.TestCase):

    def test_paragraph_conversion(self):
        block = "This is a paragraph.\nSpanning multiple lines."
        node = paragraph_from_block(block)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "p")
        self.assertGreater(len(node.children), 0)

    def test_heading_conversion(self):
        block = "# Heading Level 1"
        node = heading_from_block(block)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "h1")
        self.assertGreater(len(node.children), 0)

    def test_quote_conversion(self):
        block = "> This is a quote.\n> It spans lines."
        node = quote_from_block(block)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "blockquote")
        self.assertGreater(len(node.children), 0)

    def test_code_conversion(self):
        block = "```\nprint('hello world')\n```"
        node = code_from_block(block)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "pre")
        self.assertIsInstance(node.children[0], ParentNode)
        self.assertEqual(node.children[0].tag, "code")

    def test_unordered_list_conversion(self):
        block = "- Item one\n- Item two"
        node = list_from_block(block)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(len(node.children), 2)
        for child in node.children:
            self.assertEqual(child.tag, "li")

    def test_ordered_list_conversion(self):
        block = "1. First item\n2. Second item"
        node = olist_from_block(block)
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(len(node.children), 2)
        for child in node.children:
            self.assertEqual(child.tag, "li")

    def test_complete_markdown_to_html_node(self):
        markdown = "# Title\n\nThis is a paragraph.\n\n- Item A\n- Item B"
        root = markdown_to_html_node(markdown)
        self.assertIsInstance(root, ParentNode)
        self.assertEqual(root.tag, "div")
        self.assertGreaterEqual(len(root.children), 3)

if __name__ == "__main__":
    unittest.main()
