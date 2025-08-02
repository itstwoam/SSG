import unittest
from textnode import TextType, TextNode
from functions import text_to_textnodes

class TestParallelFormatting(unittest.TestCase):
    def test_parallel_formatting(self):
        samples = {
            "Bold only": "**bold**",
            "Bold then Italic": "**bold** and _italic_",
            "Italic then Bold": "_italic_ then **bold**",
            "Code + Bold + Italic": "`code`, **bold**, _italic_",
            "All separate": "**bold** _italic_ `code` [link](url) ![alt](img.jpg)"
        }

        expected = {
                "Bold only": [TextType.BOLD],
                "Bold then Italic": [TextType.BOLD,
                                     TextType.TEXT,
                                     TextType.ITALIC],
                "Italic then Bold": [TextType.ITALIC,
                                    TextType.TEXT,
                                    TextType.BOLD],
                "Code + Bold + Italic": [TextType.CODE,
                                        TextType.TEXT,
                                        TextType.BOLD,
                                        TextType.TEXT,
                                        TextType.ITALIC],
                "All separate": [TextType.BOLD,
                                 TextType.TEXT,
                                 TextType.ITALIC,
                                 TextType.TEXT,
                                 TextType.CODE,
                                 TextType.TEXT,
                                 TextType.LINK,
                                 TextType.TEXT,
                                 TextType.IMAGE]
        }



        for label, sample in samples.items():
            with self.subTest(label=label):
                nodes = text_to_textnodes(sample)
                types = [n.text_type for n in nodes]

                self.assertEqual(
                    types,
                    expected[label],
                    f"{label} text types mismatch.\nExpected: {expected[label]}\nGot: {types}"
                )

                self.assertTrue(all(isinstance(n, TextNode) for n in nodes))
                self.assertTrue(all(not isinstance(n, list) for n in nodes))  # ensure flat structure

if __name__ == '__main__':
    unittest.main()
