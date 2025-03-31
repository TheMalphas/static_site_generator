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


class HTMLNode():
    """HTMLNode class."""
    def __init__(
        self, 
        tag: str | None = None, 
        value: str | None = None, 
        children: list['HTMLNode'] | None = None,  
        props: dict[str: str] | None = None
        ):
        """HTMLNode constructor."""
        self.tag = tag
        self.value =  value
        self.children =  children
        self.props =  props
    
    def to_html(self):
        """To html method."""
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        """Props to html method."""

        def build_props(t: tuple[str, str]) -> str:
            """Build props."""
            return f' {t[0]}="{t[1]}"'

        return ''.join(map(build_props, list(self.props.items())) if self.props else [])

    def __eq__(self, other: 'HTMLNode') -> bool:
        """Equal method."""
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """Repr method."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """LeafNode of HTMLNode."""

    def __init__(
        self,
        *,
        tag: str | None = None, 
        value: str, 
        props: dict[str: str] | None = None
        ):
        if not value:
            raise ValueError('Value is required')
        super().__init__(tag = tag, value = value, props = props)
    
    def to_html(self) -> str:
        """To html method."""
        if not self.value:
            raise ValueError('A leaf node must have a value.')
        if not self.tag:
            return str(self.value)

        def build_tag(tag: str, value: str) -> str:
            """Build tag."""

            try:
                tag_enum = TagType[tag.upper()]
            except AttributeError:
                raise AttributeError(f"Invalid tag: {tag}. Must be a valid TagType.")

            match tag_enum:
                case TagType.H1 | TagType.H2 | TagType.H3 | TagType.H4 | TagType.H5 | TagType.H6 | \
                     TagType.B | TagType.P | TagType.I | TagType.OL | TagType.UL | TagType.BLOCKQUOTE | \
                     TagType.SPAN | TagType.DIV:
                    return simple_tag_build(tag, value)
                case TagType.A:
                    return anchor_tag_build(tag, value, self.props_to_html())
                case TagType.IMG:
                    return image_tag_build(tag, value, self.props_to_html())
                case TagType.CODE:
                    return code_tag_build(value)
                case _:
                    raise ValueError('Tags can only be part of TagType.')
        
        return build_tag(self.tag, self.value)
    

def simple_tag_build(tag: str, value: str) -> str:
    """Get tag for simple types."""

    return f'<{tag}>{value}</{tag}>'

def anchor_tag_build(tag: str, value: str, props) -> str:
    """Get tag for a, img types."""

    return f'<{tag}{props}>{value}</{tag}>'

def image_tag_build(tag: str, value: str, props) -> str:
    """Get tag for a, img types."""

    return f'<{tag}{props} {value} />'

def code_tag_build(value: str) -> str:
    """Get tag for TagTypes.CODE."""

    return f'```\n{value}\n```\n'

class ParentNode(HTMLNode):
    """ParentNode class."""

    def __init__(
        self,
        *,
        tag: str,
        children: list[HTMLNode],
        props: dict[str: str] | None = None
        ):
        """ParentNode init."""
        if not tag:
            raise ValueError('Tag is required')
        if not children:
            raise ValueError('Children are required')
        super().__init__(tag = tag, children = children, props = props)


    def to_html(self) -> str:
        """ParentNode to html method."""
        
        if not self.tag:
            raise ValueError("Tag cannot be None")
        if not self.children:
            raise ValueError("Children cannot be None")
        
        # Start with opening tag (with props if present)
        html_string = f"<{self.tag}{self.props_to_html()}>"
        
        # Accumulate all children's HTML
        for child in self.children:
            html_string += child.to_html()
        
        # Add closing tag
        html_string += f"</{self.tag}>"
        
        return html_string