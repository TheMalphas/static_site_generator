
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
        tag: str, 
        value: str, 
        props: dict[str: str] | None = None
        ):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self) -> str:
        """To html method."""
        if self.value is None:
            raise ValueError('A leaf node must have a value.')
        if not self.tag:
            return str(self.value)

        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    """ParentNode class."""

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str: str] | None = None
        ):
        super().__init__(tag=tag, children=children, props=props)
        """ParentNode init."""

    def to_html(self) -> str:
        """ParentNode to html method."""
        
        if not self.tag:
            raise ValueError("Tag cannot be None")
        if not self.children:
            raise ValueError("Children cannot be None")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"