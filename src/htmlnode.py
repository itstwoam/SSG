from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag  = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        final = ""
        for k,v in self.props.items():
            final += f'{k}="{v}"'
        return final

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value!")
        if not self.tag:
            return str(self.value)
        return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag!")
        if not self.children:
            raise ValueError("ParentNode must have at least one child!")
        else:
            final = f"<{self.tag}>"
            for n in self.children:
                final += n.to_html()
            final += f"</{self.tag}>"
            return final

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text, None, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b", None)
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i", None)
        case TextType.CODE:
            return LeafNode(text_node.text, "code", None)
        case TextType.LINK:
            return LeafNode(text_node.text, "a", text_node.props)
        case TextType.IMAGE:
            return LeafNode("", "img", text_node.props)
        case _:
            raise Exception("unkown text type")
