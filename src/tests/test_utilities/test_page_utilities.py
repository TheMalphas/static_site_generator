from pathlib import Path
import unittest

from utilities import extract_title_markdown
from utilities.block_utilities import BlockType
from utilities.page_utilities import generate_page


class TestExtractTitle(unittest.TestCase):
    """Suite of tests for extract_title_markdown."""


    def test_extract_title_markdown(self):
        """Test markdown title."""
        
        md = """
# This is a title
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        title = extract_title_markdown(md)
        self.assertEqual(
            title,
            "This is a title"
        )

    def test_extract_title_markdown_fail(self):
        """Test markdown title."""

        md = """
## This is not a title
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        with self.assertRaises(ValueError) as context:
            extract_title_markdown(md)
        
        error_msg = str(context.exception)
        self.assertEqual(error_msg, 'Missing or incorrect title')


class TestGeneratePage(unittest.TestCase):
    """Suite of tests for generate_page."""

    def setUp(self):
        """SetUp test class."""

        self.from_path = Path("./content/tesindex.md").resolve()
        self.template_path = Path("./template.html").resolve()
        self.to_path = Path("./public/index.html").resolve()

        public_dir = Path("./public").resolve()
        if public_dir.exists():
            import shutil
            shutil.rmtree(public_dir)

    def test_generate_page_no_values(self):
        """Test get error from generate_page."""


        with self.assertRaises(ValueError) as context:
            generate_page(None, self.template_path,  self.to_path)
        
        error_msg = str(context.exception)
        self.assertEqual(error_msg, 'All paths must be valid.')


    def test_generate_page_(self):
        """Test generate page."""

        self.from_path.parent.mkdir(parents=True, exist_ok=True)
        self.from_path.write_text("# Test Title\nSome content")
        self.template_path.write_text("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

        generate_page(self.from_path, self.template_path, self.to_path)
        self.assertTrue(self.to_path.exists())
        content = self.to_path.read_text()
        self.assertIn("Test Title", content)
        self.assertIn("Some content", content)

