from enum import Enum, auto


class HTMLNode():
    """HTMLNode class."""
    def __init__(
        self, 
        tag: str | None = None, 
        value: str | None = None, 
        children: list['HTMLNode'] | None = None,  
        props: dict[str: str] | None = None, 
        ):
        """HTMLNode constructor."""
        self.tag = tag
        self.value =  value
        self.children =  children
        self.props =  props
    
    def to_html(self):
        """To html method."""
        raise NotImplementedError()
    
    def props_to_html(self):
        """Props to html method."""

        def build_props(t: tuple[str, str]):
            """Build props."""
            return f' "{t[0]}"="{t[1]}"'

        return ''.join(map(build_props, list(self.props.items())))

    def __eq__(self, other: 'HTMLNode'):
        """Equal method."""
        return self.__dict__ == other.__dict__

    def __repr__(self):
        """Repr method."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
