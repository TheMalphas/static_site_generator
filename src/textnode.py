from enum import Enum, auto

class TextType(Enum):
    """TextType Enum."""
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()

class TextNode():
    """TextNode class."""
    def __init__(self, text: str, text_type: TextType, url: str):
        """TextNode constructor."""
        self.text = text
        self.text_type =  text_type
        self.url =  url
    
    def __eq__(self, text_node: 'TextNode'):
        """Equal method."""
        return (
            self.text == text_node.text and
            self.text_type == text_node.text_type and
            self.url == text_node.url
        )

    def __repr__(self):
        """Repr method."""
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
