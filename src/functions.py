from textnode import TextType, TextNode
from htmlnode import LeafNode
from enums import TextType
import re

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
            

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            final.append(n)
            continue

        # Don't skip truly empty nodes — preserve them if untouched
        if delimiter not in n.text:
            final.append(n)
            continue

        broken = n.text.split(delimiter)

        if len(broken) % 2 == 0:
            raise Exception("invalid markdown syntax")

        for i, t in enumerate(broken):
            # Only skip empty segments generated *after* splitting
            if t == "":
                continue
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            final.append(TextNode(t, node_type))

    return final


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    final = []
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            final.extend(split_nodes_worker(TextType.IMAGE, n.text))
        else:
            final.append(n)
    return final


def split_nodes_links(old_nodes):
    final = []
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            final.extend(split_nodes_worker(TextType.LINK, n.text))
        else:
            final.append(n)
    return final


def split_nodes_worker(tt, text):
    matches = extract_markdown_images(text) if tt == TextType.IMAGE else extract_markdown_links(text)
    result = []
    work = text

    for alt, link in matches:
        if tt == TextType.IMAGE:
            delimiter = f"![{alt}]({link})"
        else:
            delimiter = f"[{alt}]({link})"

        parts = work.split(delimiter, 1)

        if len(parts) > 0:
            if len(parts[0]) > 0:
                result.append(TextNode(parts[0], TextType.TEXT))

        node = TextNode(alt, tt, link)
        result.append(node)

        if len(parts) > 1:
            work = parts[1]
        else:
            work = ""

    if len(work) > 0:
        result.append(TextNode(work, TextType.TEXT))

    return result

def text_to_textnodes(text):
    final = [TextNode(text, TextType.TEXT)]
    #split_nodes_delimiter(old_nodes, delimiter, text_type):
    final = split_nodes_delimiter(final, "**", TextType.BOLD)
    final = split_nodes_delimiter(final, '_', TextType.ITALIC)
    final = split_nodes_delimiter(final, '\'', TextType.CODE)
    final = split_nodes_image(final)
    final = split_nodes_links(final)
    return final

def markdown_to_block(markdown):
    work = markdown.split("\n\n")
    final = []
    for t in work:
        t = t.strip()
        if len(t) > 0:
            final.append(t.strip())
    return final
