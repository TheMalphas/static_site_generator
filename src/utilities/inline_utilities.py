import re

from nodes import TextNode, TextType

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
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split link nodes."""

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text) -> list[TextNode]:
    """Transform markdown text to a list of TextNodes."""
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(old_nodes=nodes, delimiter="`", text_type=TextType.CODE)
    
    return nodes