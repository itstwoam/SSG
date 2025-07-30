from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, text_node_one):
        return self.text == text_node_one.text and self.text_type == text_node_one.text_type and self.url == text_node_one.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
