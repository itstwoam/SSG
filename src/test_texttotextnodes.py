import unittest
from textnode import TextType, TextNode
from functions import text_to_textnodes

class TestParallelFormatting(unittest.TestCase):
    def test_parallel_formatting(self):
        samples = {
            "Bold only": "**bold**",
            "Bold then Italic": "**bold** and _italic_",
            "Italic then Bold": "_italic_ then **bold**",
            "Code + Bold + Italic": "'code', **bold**, _italic_",
            "All separate": "**bold** _italic_ 'code' [link](url) ![alt](img.jpg)"
        }

        for label, sample in samples.items():
            with self.subTest(label=label):
                nodes = text_to_textnodes(sample)
                types = [n.text_type for n in nodes]
                self.assertTrue(
                    any(t == TextType.BOLD for t in types),
                    f"{label} missing BOLD"
                )
                #self.assertIn(TextType.BOLD, types, f"{label} missing BOLD")
                self.assertIn(TextType.ITALIC, types, f"{label} missing ITALIC")
                self.assertTrue(all(isinstance(n, TextNode) for n in nodes))
                self.assertTrue(all(not isinstance(n, list) for n in nodes))  # ensure flat structure

if __name__ == '__main__':
    unittest.main()
