import unittest
import re
from enums import BlockType
from functions import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):

    def test_ordered_list_valid(self):
        self.assertEqual(block_to_block_type("1. One\n2. Two\n3. Three"), BlockType.ORDERED)

    def test_ordered_list_skipped_number(self):
        self.assertEqual(block_to_block_type("1. One\n3. Three"), BlockType.PARAGRAPH)

    def test_ordered_leading_zero(self):
        self.assertEqual(block_to_block_type("01. One\n02. Two"), BlockType.PARAGRAPH)

    def test_ordered_missing_space(self):
        self.assertEqual(block_to_block_type("1.One\n2.Two"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> Quote\n> More quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item\n- Another"), BlockType.UNORDERED)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text\nNothing fancy"), BlockType.PARAGRAPH)

    def test_heading_valid(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_missing_space(self):
        self.assertEqual(block_to_block_type("##Heading"), BlockType.PARAGRAPH)

    def test_code_block_valid(self):
        self.assertEqual(block_to_block_type("```code\nblock```"), BlockType.CODE)

    def test_code_block_unterminated(self):
        self.assertEqual(block_to_block_type("```code\nblock"), BlockType.PARAGRAPH)

    def test_ordered_wrong_start(self):
        self.assertEqual(block_to_block_type("2. Should start at 1\n3. Second"), BlockType.PARAGRAPH)

    def test_ordered_with_blank_lines(self):
        self.assertEqual(block_to_block_type("1. One\n2. Two\n3. Three"), BlockType.ORDERED)

    def test_ordered_leading_blanks(self):
        self.assertEqual(block_to_block_type("1. One\n2. Two"), BlockType.ORDERED)


if __name__ == "__main__":
    unittest.main()
