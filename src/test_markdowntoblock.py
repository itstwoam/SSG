import unittes
from functions import markdown_to_block  # Adjust if in a different module

class TestMarkdownToBlock(unittest.TestCase):
    def test_clean_blocks(self):
        input_text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        expected = ["Paragraph one.", "Paragraph two.", "Paragraph three."]
        self.assertEqual(markdown_to_block(input_text), expected)

    def test_extra_whitespace(self):
        input_text = "   Paragraph one.   \n\n   \n\n  Paragraph two.  "
        expected = ["Paragraph one.", "Paragraph two."]
        self.assertEqual(markdown_to_block(input_text), expected)

    def test_single_block(self):
        input_text = "Only one block — no double newline."
        expected = ["Only one block — no double newline."]
        self.assertEqual(markdown_to_block(input_text), expected)

    def test_empty_string(self):
        input_text = ""
        expected = []
        self.assertEqual(markdown_to_block(input_text), expected)

    def test_only_newlines(self):
        input_text = "\n\n\n\n"
        expected = []
        self.assertEqual(markdown_to_block(input_text), expected)

    def test_malformed_blocks(self):
        input_text = "\n\nFirst block.\n\n\n\nSecond block.\n\n\nThird block.\n\n\n"
        expected = ["First block.", "Second block.", "Third block."]
        self.assertEqual(markdown_to_block(input_text), expected)

    def test_blocks_with_inline_newlines(self):
        input_text = "This is a paragraph\nthat spans multiple lines.\n\nAnother one here."
        expected = [
            "This is a paragraph\nthat spans multiple lines.",
            "Another one here."
        ]
        self.assertEqual(markdown_to_block(input_text), expected)

if __name__ == "__main__":
    unittest.main()
