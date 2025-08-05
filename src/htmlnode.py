import inspect
from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag  = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        print("I'm not implemented yet!")
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        final = ""
        for prop in self.props:
            final += f' {prop}="{self.props[prop]}"'
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
        #print(f"HTMLNode of type: {type(self)} with a tag of {self.tag}, {len(self.children)} children nodes and {self.props} props")
        #if not self.value:
        if self.value == None:
            raise ValueError("LeafNode must have a value!")
        if not self.tag:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    """
         Parent node that must contain at least one child

         Functions:
         to_html() - prints out an html version of it's contents

         Fields:
         tag: symbol used for the tag <tag>
         children: List of child nodes, can't be empty
         props: Props for the html tag
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        #print(f"HTMLNode of type: {type(self)} with a tag of {self.tag}, {len(self.children)} children nodes and {self.props} props")
        if not self.tag:
            raise ValueError("ParentNode must have a tag!")
        if not self.children:
            raise ValueError("ParentNode must have at least one child!")
        else:
            final = f"<{self.tag}>"
        for n in self.children:
            #print(n.value,"\n")
            final += n.to_html()
        final += f"</{self.tag}>"
        return final

