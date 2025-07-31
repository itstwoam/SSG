import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_pass_through_non_text_node(self):
        node = TextNode("Bold section", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])  # Should pass untouched

    def test_basic_split_with_valid_delimiters(self):
        node = TextNode("Hello **world** again", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], TextNode("Hello ", TextType.TEXT))
        self.assertEqual(result[1], TextNode("world", TextType.BOLD))
        self.assertEqual(result[2], TextNode(" again", TextType.TEXT))

    def test_multiple_delimiters(self):
        node = TextNode("One **two** three **four**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("One ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" three ", TextType.TEXT),
            TextNode("four", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_invalid_markdown_even_split_raises(self):
        node = TextNode("One **two** three **", TextType.TEXT)  # Dangling opener
        with self.assertRaises(Exception) as ctx:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(ctx.exception), "invalid markdown syntax")

    def test_empty_string_returns_empty_list(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], TextNode("", TextType.TEXT))

    def test_only_delimiter_raises(self):
        node = TextNode("**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_nested_delimiter_content(self):
        node = TextNode("This is **nested **content** example**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("nested ", TextType.BOLD),
            TextNode("content", TextType.TEXT),
            TextNode(" example", TextType.BOLD),
            TextNode("!", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

