import re
from enum import Enum, auto
from nodes import ParentNode
from nodes.textnode import TextNode, TextType, text_node_to_html_node

from utilities.inline_utilities import text_to_textnodes


class BlockType(Enum):
    """BlockType Enum."""
    PARAGRAPH =  auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST =  auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown) -> list[str]:
    """Transform markdown to blocks."""
    return list(filter(str.strip, map(str.strip, markdown.strip().split('\n\n'))))


def block_to_block_type(markdown_block) -> BlockType:
    """Return block type based on markdown_block."""

    if re.match(r'^#{1,6} ', markdown_block):
        return BlockType.HEADING
    
    if re.match(r'^```[\s\S]*```$', markdown_block, re.DOTALL):
        return BlockType.CODE

    lines = markdown_block.strip().split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = [int(re.match(r'^(\d+)\.', line).group(1)) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown_text) -> ParentNode:
    """Generate a full Parent HTMLNode"""

    blocks = markdown_to_blocks(markdown_text)

    children = []

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)


def block_to_html_node(block):
    """Block to html."""

    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")


def text_to_children(text):
    """Text to children node."""
    return list(map(text_node_to_html_node, text_to_textnodes(text)))


def paragraph_to_html_node(block):
    """Transform paragraph blocks."""

    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Transform heading blocks."""

    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Transform code blocks."""

    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    """Transform ordered_list blocks."""

    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    """Transform unordered_list blocks."""

    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    """Transform quote blocks."""

    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)