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
