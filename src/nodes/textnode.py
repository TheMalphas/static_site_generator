from enum import Enum, auto

from nodes import LeafNode


class TextType(Enum):
    """TextType Enum."""
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()
    TEXT = auto()


class TextNode():
    """TextNode class."""
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        """TextNode constructor."""
        self.text = text
        self.text_type =  text_type
        self.url =  url
    
    def __eq__(self, other: 'TextNode') -> bool:
        """Equal method."""
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self) -> str:
        """Repr method."""
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Transform TextNode to LeafNode"""

    if not text_node.text_type in TextType:
        raise ValueError('Invalid text type')
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={'href':text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag='img', value="", props={'src':text_node.url,'alt':text_node.text})