import unittest
from functions import markdown_to_html_node
from htmlnode import ParentNode

string = "How will \n\n split?"
print(string.split("\n"))
#class TestMarkdownInlineCombinations(unittest.TestCase):

    # def test_multiple_inline_formats(self):
    #     markdown = (
    #         "# Heading _with italics_ and **bold**\n\n"
    #         "Paragraph with **bold**, _italic_, and `code` snippets inline.\n\n"
    #         "> Quote with **emphasis** and `inline code`.\n\n"
    #         "- List item with _italic text_\n- Another item with `code`\n\n"
    #         "1. Ordered item with **bold** text\n2. Second item with `code block`\n\n"
    #         "```\nThis is a fenced code block\nIt should not be parsed for inline formatting\n```\n"
    #     )
    #
    #     root = markdown_to_html_node(markdown)
    #     self.assertIsInstance(root, ParentNode)
    #     self.assertEqual(root.tag, "div")
    #     self.assertGreaterEqual(len(root.children), 6)
    #
    #     # Sanity check on structure
    #
    #     expected_tags = {"h1", "p", "blockquote", "ul", "ol", "pre"}
    #     actual_tags = set(child.tag for child in root.children)
    #     self.assertTrue(expected_tags.issubset(actual_tags))
    #
    # def test_heading_with_inline_emphasis(self):
    #     markdown = "## This is a heading with _italic_ and **bold**"
    #     root = markdown_to_html_node(markdown)
    #     heading = root.children[0]
    #     self.assertEqual(heading.tag, "h2")
    #     self.assertTrue(any(child.tag == "i" for child in heading.children))
    #     self.assertTrue(any(child.tag == "b" for child in heading.children))
    #
    # def test_list_with_inline_styles(self):
    #     markdown = "- **Bold item**\n- Item with `code`\n- _Italicized item_"
    #     root = markdown_to_html_node(markdown)
    #     ul = root.children[0]
    #     self.assertEqual(ul.tag, "ul")
    #     self.assertEqual(len(ul.children), 3)
    #     self.assertTrue(all(li.tag == "li" for li in ul.children))

#    def test_paragraphs(self):
# md = """
#     This is **bolded** paragraph
#     text in a p
#     tag here
#
#     This is another paragraph with _italic_ text and `code` here
#
#     """
#
# node = markdown_to_html_node(md)
# html = node.to_html()
# print(bool(html == "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
# ))
# if __name__ == "__main__":
#     unittest.main()
