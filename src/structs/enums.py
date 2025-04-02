from enum import Enum, auto

class TagType(Enum):
    """TagType Enum."""
    H1 = auto()
    H2 = auto()
    H3 = auto()
    H4 = auto()
    H5 = auto()
    H6 = auto()
    A = auto()
    B = auto()
    P = auto()
    I = auto()
    SPAN = auto()
    DIV = auto()
    CODE = auto()
    IMG = auto()
    OL = auto()
    BLOCKQUOTE = auto()
    UL = auto()


class TextType(Enum):
    """TextType Enum."""
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()
    TEXT = auto()

class BlockType(Enum):
    """BlockType Enum."""
    PARAGRAPH =  auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST =  auto()
    ORDERED_LIST = auto()