import re
from structs import BlockType


def markdown_to_blocks(markdown) -> list[str]:
    """Transform markdown to blocks."""
    return list(filter(str.strip, map(str.strip, markdown.strip().split('\n\n'))))

def block_to_block_type(markdown_block) -> BlockType:
    """Return block type based on markdown_block."""

    if re.match(r'^#{1,6} ', markdown_block):
        return BlockType.HEADING
    
    if re.match(r'^```[\s\S]*```$', markdown_block, re.DOTALL):
        return BlockType.CODE

    lines = markdown_block.strip().split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    if all(re.match(r'^\d+\. ', line) for line in lines):
        numbers = [int(re.match(r'^(\d+)\.', line).group(1)) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH