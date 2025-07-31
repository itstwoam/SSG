import unittest
from textnode import TextNode, TextType
from functions import split_nodes_image, split_nodes_links

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_links(self):
        mock_node = TextNode("Link: [OpenAI](https://openai.com) and [GitHub](https://github.com)", TextType.TEXT)
        nodes = split_nodes_links([mock_node])
        
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0], TextNode("Link: ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("OpenAI", TextType.LINK, "https://openai.com"))
        self.assertEqual(nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("GitHub", TextType.LINK, "https://github.com"))
        for node in nodes:
            if node.text_type == TextType.TEXT:
                self.assertNotEqual(node.text,"")

    def test_split_nodes_image(self):
        mock_node = TextNode("Header ![logo](logo.png) then ![icon](icon.svg)", TextType.TEXT)
        nodes = split_nodes_image([mock_node])

        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0], TextNode("Header ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("logo", TextType.IMAGE, "logo.png"))
        self.assertEqual(nodes[2], TextNode(" then ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("icon", TextType.IMAGE, "icon.svg"))
        for node in nodes:
            if node.text_type == TextType.TEXT:
                self.assertNotEqual(node.text,"")

    def test_no_match(self):
        mock_node = TextNode("No markdown here!", TextType.TEXT)
        self.assertEqual(split_nodes_links([mock_node]), [TextNode("No markdown here!", TextType.TEXT)])
        self.assertEqual(split_nodes_image([mock_node]), [TextNode("No markdown here!", TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()
