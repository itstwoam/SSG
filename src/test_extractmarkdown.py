import unittest
from functions import extract_markdown_images, extract_markdown_links

class TestMarkdownExtraction(unittest.TestCase):

    def test_valid_image(self):
        text = "![Alt](image.png)"
        expected = [("Alt", "image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_valid_link(self):
        text = "[Link](https://example.com)"
        expected = [("Link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_image_with_brackets_in_alt(self):
        text = "![Alt [Text]](image.png)"
        expected = []  # Should fail to match due to inner brackets
        self.assertEqual(extract_markdown_images(text), expected)

    # def test_link_with_parentheses_in_text(self):
    #     text = "[Click (here)](link.com)"
    #     expected = []  # Fails due to inner parentheses
    #     self.assertEqual(extract_markdown_links(text), expected)

    def test_link_that_is_actually_an_image(self):
        text = "![Image](img.png)"
        expected = []  # Should NOT match as a link due to lookbehind
        self.assertEqual(extract_markdown_links(text), expected)

    def test_malformed_image(self):
        text = "![Alt(image.png)"
        expected = []  # Missing closing bracket
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_link(self):
        text = "[Text(link.com)"
        expected = []  # Missing closing bracket
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_strict_matches(self):
        text = "![One](1.png) and ![Two](2.jpg), [A](a.com) and [B](b.com)"
        expected_images = [("One", "1.png"), ("Two", "2.jpg")]
        expected_links = [("A", "a.com"), ("B", "b.com")]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)

if __name__ == '__main__':
    unittest.main()
