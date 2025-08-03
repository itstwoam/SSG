from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
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
    #print(f"In text_to_textnodes with text=: {text}")
    final = [TextNode(text, TextType.TEXT)]
    #split_nodes_delimiter(old_nodes, delimiter, text_type):
    #print("Going to split_nodes_delimiter for BOLD")
    final = split_nodes_delimiter(final, "**", TextType.BOLD)
    #print(f'final after bold delimiter: {final}')
    #print("Going to split_nodes_delimiter for ITALIC")
    final = split_nodes_delimiter(final, '_', TextType.ITALIC)
    #print(f'final after italic delimiter: {final}')
    #print("Going to split_nodes_delimiter for CODE")
    final = split_nodes_delimiter(final, '`', TextType.CODE)
    #print(f'final after code delimiter: {final}')
    #print("Going to split_nodes_image")
    final = split_nodes_image(final)
    #print(f'final after image delimiter: {final}')
    #print("Going to split_nodes_links")
    final = split_nodes_links(final)
    #print(f'final after links delimiter: {final}')
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
        quote = True
        count = 1
        chaos = True
        order = True
        for l in lines:
            if quote:
                if l[0] != ">":
                    quote = False
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
        if quote:
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
        return BlockType.PARAGRAPH

def block_to_html_node(block, block_type):
    """
    Converts a block of markdown to an htmlnode

    Parameters:
    block (string) Block of text to convert to htmlnode
    block_type (BlockType) defines the block type

    Returns:
    htmlnode consisting of the nodes required for the block.
    """
    final = []
    match block_type:
        case BlockType.PARAGRAPH:
            tag = "p"
            #create the children nodes first
            children = text_to_textnodes(block)
            #create the parent node
    #def __init__(self, tag, children, props=None):
            pnode = ParentNode("p", children)










def markdown_to_html_node(markdown):
    """
    Converts a markdown document to a single htmlnode containing all the individual html nodes
    described by the markdown document

    Parameters:
    markdown (string) document containing lines of markdown

    Return:
    html node
    """
    #print("In markdown")
    final = []
    #print("Going to markdown_to_block")
    blocks = markdown_to_block(markdown)
    #print(block)
    for b in blocks:
        #print(b)
        #print("Going to text_to_textnodes")
        # Figure out what each block type is
        b_type = block_to_block_type(b)
        # Call function to deal with the type
        match b_type:
            case BlockType.PARAGRAPH:
                final.append(paragraph_from_block(b))
            case BlockType.CODE:
                final.append(code_from_block(b))
            case BlockType.QUOTE:
                final.append(quote_from_block(b))
            case BlockType.HEADING:
                final.append(heading_from_block(b))
            case BlockType.ORDERED:
                final.append(olist_from_block(b))
            case BlockType.UNORDERED:
                final.append(list_from_block(b))
            case _:
                raise Exception("Invalid block type in markdown_to_html_node")
        # Return an htmlnode based on block type
    return ParentNode("div", final, None)

def get_children(text):
    final = []
    t_nodes = text_to_textnodes(text)
    for n in t_nodes:
        h_node = text_node_to_html_node(n)
        final.append(h_node)
    return final

def paragraph_from_block(block):
    #lines = block.split("\n")
    lines = [line.strip() for line in block.split("\n")]
    new_lines = " ".join(lines)
    children = get_children(new_lines)
    return ParentNode("p", children)


def heading_from_block(block):
    level = 0
    for l in block:
        if l == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise Exception(f"invalid heading level: {level}")
    text = block[level+ 1 :]
    children = get_children(text)
    return ParentNode(f"h{level}", children)

def code_from_block(block):
    text = block[4:-3]
    t_node = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(t_node)
    parent = ParentNode("code", [children])
    return ParentNode("pre", [parent])

def quote_from_block(block):
    final = []
    lines = block.split("\n")
    for l in lines:
        final.append(l.lstrip(">").strip())
    t_nodes = " ".join(final)
    children = get_children(t_nodes)
    return ParentNode("blockquote", children)


def list_from_block(block):
    final = []
    lines = block.split("\n")
    for l in lines:
        text = l[2:]
        children = get_children(text)
        final.append(ParentNode("li", children))
    return ParentNode("ul", final)


def olist_from_block(block):
    final = []
    lines = block.split("\n")
    for l in lines:
        text = l[l.find(" ")+1:]
        children = get_children(text)
        final.append(ParentNode("li", children))
    return ParentNode("ol", final)
