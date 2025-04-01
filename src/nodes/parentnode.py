from nodes.htmlnode import HTMLNode


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