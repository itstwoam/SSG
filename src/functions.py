from textnode import TextType, TextNode
from htmlnode import LeafNode
from enums import TextType, BlockType
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
    """
    Takes a list of nodes and splits any text type nodes into multiple
    nodes based on text_type parameter.

    Parameters:
    old_nodes ([TextNodes]) List of nodes to convert
    delimiter (string) String that defines the node type in markdown
    text_type (TextType) Type of text to look for

    Returns:
    list of textnodes
    """
    #print("In split_nodes_delimiter")
    final = []
    #print(old_nodes)
    for n in old_nodes:
        #print(n)
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

    #print("Returning from split_nodes_delimiter")
    return final


def extract_markdown_images(text):
    """
    Returns alt text and url of html text.

    Parameters:
    text (string) Text to extract alt text and url from 

    Returns:
    List of tuples - [((alt text),(url))]
    """
    #print("In extract_markdown_images")
    #print("Returning from extract_markdown_Images")
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    """
    Returns text and url of links

    Parameters (string) text to extract text and link from

    Returns:
    List of tuples - [((text, link))]
    """
    #print("In extract_markdown_links")
    #print("Returning from extract_markdown_links")
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    """
    Splits text nodes into a series of text and image nodes.

    Parameters:
    old_nodes ([text nodes]) nodes to extract text nodes with image data

    Returns:
    List of text and image nodes
    """
    #print("In split_nodes_images")
    final = []
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            #print("Going to split_nodes_worker")
            final.extend(split_nodes_worker(TextType.IMAGE, n.text))
        else:
            final.append(n)
    #print("Returning from split_nodes_images")
    return final


def split_nodes_links(old_nodes):
    """
    Splits text nodes with a link html into text and image nodes

    Parameters:
    List of textnodes - [textnodes]

    Returns:
    list of text and image nodes
    """
    #print("In split_nodes_links")
    final = []
    #print(old_nodes)
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            #print("Going to split_nodes_worker")
            final.extend(split_nodes_worker(TextType.LINK, n.text))
        else:
            final.append(n)
    #print("Returning from split_nodes_links")
    return final


def split_nodes_worker(tt, text):
    """
    Internal function, should not be called upon
    """
    #print("In split_nodes_worker")
    #print("Going to extract_markdown_images or extract_markdown_links")
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
    #print("Returning from split_nodes_worker")

    return result

def text_to_textnodes(text):
    """
    Converts a string into a list of nodes
    based on content of the string

    Parameters:
    text (string): The text to parse.

    Returns:
    List of textnodes of different types
    """
    #print("In text_to_textnodes")
    final = [TextNode(text, TextType.TEXT)]
    #split_nodes_delimiter(old_nodes, delimiter, text_type):
    #print("Going to split_nodes_delimiter for BOLD")
    final = split_nodes_delimiter(final, "**", TextType.BOLD)
    #print("Going to split_nodes_delimiter for ITALIC")
    final = split_nodes_delimiter(final, '_', TextType.ITALIC)
    #print("Going to split_nodes_delimiter for CODE")
    final = split_nodes_delimiter(final, '`', TextType.CODE)
    #print("Going to split_nodes_image")
    final = split_nodes_image(final)
    #print("Going to split_nodes_links")
    final = split_nodes_links(final)
    #print("Returning from text_to_textnodes")
    return final

def markdown_to_block(markdown):
    """
    Converts a markdown document into text blocks

    Parameters:
    markdown (string) document to break into blocks

    Returns:
    List of blocks consisting of strings not seperated by lines in markdown
    """
    #print("In markdown_to_block")
    work = markdown.split("\n\n")
    final = []
    for t in work:
        t = t.strip()
        if len(t) > 0:
            final.append(t.strip())
    #print("Returning from markdown_to_block")
    return final


def block_to_block_type(block):
    """
    This determins block type based on content of block parameter

    Parameters:
    block (string) Text to use to extract type information from

    Returns:
    BlockType
    """
    #print("In block_to_block_type")
    if bool(re.match(r'^#{1,6} .+', block)):
        return BlockType.HEADING
    if bool(re.match(r'^```[\s\S]*?```$', block)):
        return BlockType.CODE
    lines = block.split("\n")
    if len(lines) > 0:
        arrow = True
        count = 1
        chaos = True
        order = True
        for l in lines:
            if arrow:
                if l[0] != ">":
                    arrow = False
            if chaos:
                if l.find("- ") != 0:
                    chaos = False
            if order:
                if not bool(re.match(r'^[1-9]\d*\.\s.+$', l)) or l.split(".", 1)[0] != str(count):
                    # print(f"The string: {l} is not an ordered list.")
                    # print(bool(re.match(r'^[1-9]\d*\.\s.+$', l)))
                    # print(int(l.split(".", 1)[0]))
                    order = False
            count += 1
        if not arrow and not chaos and not order:
            #print("Returning from block_to_bloc_type")
            return BlockType.PARAGRAPH
        if arrow:
            #print("Returning from block_to_bloc_type")
            return BlockType.QUOTE
        if chaos:
            #print("Returning from block_to_bloc_type")
            return BlockType.UNORDERED
        if order:
            #print("Returning from block_to_bloc_type")
            return BlockType.ORDERED
        #should not be here.  Quick kernel panic!
        #print("Throwing exception in block_to_block_type")
        raise Exception("no block type found!")


def markdown_to_html_node(markdown):
    #print("In markdown")
    final = []
    #print("Going to markdown_to_block")
    work = markdown_to_block(markdown)
    #print(work)
    for l in work:
        #print(l)
        #print("Going to text_to_textnodes")
        final = text_to_textnodes(l)
        #print(l)
    #print(work)
    #print("Returning from block_to_bloc_type")
    return final
