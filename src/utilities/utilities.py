import re

from nodes import TextNode
from structs import TextType

def split_nodes_delimiter(*, old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """Split nodes by delimiter."""
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        result = []

        while delimiter in text:
            start_idx = text.find(delimiter)
            end_idx = text.find(delimiter, start_idx + len(delimiter))

            if end_idx == -1:
                raise ValueError(f'No closing delimiter found for {delimiter}')
            
            if start_idx > 0:
                result.append(TextNode(text[:start_idx], TextType.TEXT))
            
            inner_text = text[start_idx + len(delimiter):end_idx]
            result.append(TextNode(inner_text, text_type))

            text = text[end_idx + len(delimiter):]
        
        if text: 
            result.append(TextNode(text, TextType.TEXT))
        
        new_nodes.extend(result)
        
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Use regex to find markdown image tag."""
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Use regex to find markdown link tag."""
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split image nodes."""
    new_nodes = []

    for old_node in old_nodes:
        original_text = old_node.text

        if not original_text:
            continue

        results = extract_markdown_images(original_text)
        
        if not results:
            new_nodes.append(old_node)
            continue

        remaining_text = original_text
        
        for alt_text, img_url in results:
            img_markdown = f"![{alt_text}]({img_url})"
            parts = remaining_text.split(img_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=img_url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
                
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split link nodes."""
    new_nodes = []

    for old_node in old_nodes:
        original_text = old_node.text

        if not original_text:
            continue

        results = extract_markdown_links(original_text)
        
        if not results:
            new_nodes.append(old_node)
            continue

        remaining_text = original_text
        
        for link_text, link_url in results:
            link_markdown = f"[{link_text}]({link_url})"
            parts = remaining_text.split(link_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""
                
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

