from nodes.htmlnode import HTMLNode
from structs import TagType

class LeafNode(HTMLNode):
    """LeafNode of HTMLNode."""

    def __init__(
        self,
        tag: str | None = None, 
        value: str | None = None, 
        props: dict[str: str] | None = None
        ):
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