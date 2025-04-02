import logging
from pathlib import Path
import re

from utilities.block_utilities import markdown_to_html_node

def extract_title_markdown(text: str):
    """Extract title from the first header."""

    match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)

    if match:
        if not re.match(r'^#+', match.group(0)[1:]):
            return match.group(1).strip()
    raise ValueError('Missing or incorrect title')


logger = logging.getLogger(__name__)


def generate_page(from_path, template_path, dest_path) -> None:
    """Generate page converting from md to html."""
    
    msg = f'Generating page from {from_path} to {dest_path} using {template_path}.'
    logger.info(msg)

    if not from_path or not template_path or not dest_path:
        raise ValueError('All paths must be valid.')

    with Path(from_path).open('r') as f:
        markdown = f.read()

    with Path(template_path).open('r') as t:
        template = t.read()

    title = extract_title_markdown(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = template.replace('{{ Title }}', title).replace('{{ Content }}', content)

    dest_path = Path(dest_path).resolve()
    
    if dest_path.is_dir():
        raise IsADirectoryError(f"Destination path '{dest_path}' is a directory, not a file.")

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(html)

    logger.info(f"Page generated at {dest_path}.")

def generate_pages_recursive(content_dir, template_path, public_dir):
    """Generate pages recursively."""

    content_path = Path(content_dir)
    public_path = Path(public_dir)
    
    for item in content_path.rglob("*.md"):
        rel_path = item.relative_to(content_path)
        
        dest_path = public_path / rel_path.with_suffix(".html")
        
        generate_page(str(item), template_path, str(dest_path))