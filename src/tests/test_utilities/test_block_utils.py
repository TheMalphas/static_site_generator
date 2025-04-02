import unittest

from utilities import markdown_to_blocks, block_to_block_type

from structs import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    """Suite of tests for markdown_to_blocks."""


    def test_markdown_to_blocks(self):
        """Test markdown to blocks."""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_with_more_inline(self):
        """Test markdown to blocks."""
        # set to failure
        md = """
This is **bolded** paragraph

This is another paragraph with **_italic_** text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertNotEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlock(unittest.TestCase):
    """Suite of tests for markdown_to_blocks."""

    def setUp(self):
        """Setup data for test."""

        self.markdown_text = """
This is a paragraph

# This is a heading paragraph

## This is heading paragraph

### This is heading paragraph

#### This is heading paragraph

##### This is heading paragraph

###### This is heading paragraph

```
This is code paragraph
```

>This is quote paragraph

- This is an unordered list
- with items

1. This is an ordered list
2. with items
3. and items
"""
        self.blocks = markdown_to_blocks(self.markdown_text)

    def test_block_to_block_type(self):
        """Test blocks to block type."""

        with self.subTest('Match paragraph.'):
            md_section = self.blocks[0]
            block_type = block_to_block_type(md_section)

            self.assertEqual(block_type, BlockType.PARAGRAPH)

        with self.subTest('Match heading.'):
            for i in range(1, 7):
                md_section = self.blocks[i]
                block_type = block_to_block_type(md_section)

                self.assertEqual(block_type, BlockType.HEADING)

        with self.subTest('Match code.'):
            md_section = self.blocks[7]
            block_type = block_to_block_type(md_section)

            self.assertEqual(block_type, BlockType.CODE)

        with self.subTest('Match quote.'):
            md_section = self.blocks[8]
            block_type = block_to_block_type(md_section)

            self.assertEqual(block_type, BlockType.QUOTE)

        with self.subTest('Match unordered list.'):
            md_section = self.blocks[9]
            block_type = block_to_block_type(md_section)

            self.assertEqual(block_type, BlockType.UNORDERED_LIST)

        with self.subTest('Match ordered list.'):
            md_section = self.blocks[10]
            block_type = block_to_block_type(md_section)

            self.assertEqual(block_type, BlockType.ORDERED_LIST)