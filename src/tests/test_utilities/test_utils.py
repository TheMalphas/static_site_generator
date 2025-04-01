import unittest
from nodes import TextNode
from structs import TextType

from utilities import (
    split_nodes_delimiter, 
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

class TestSplitNodesDelimiter(unittest.TestCase):
    """Suite of tests for test_split_nodes_delimiter."""

    def test_split_nodes_delimiter_no_delimiters(self):
        """Test with text that doesn't contain delimiters."""
        node = TextNode("This is a text node", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(1, len(result))
        self.assertEqual(node, result[0])
    
    def test_split_nodes_delimiter_with_bold(self):
        """Test with bold delimiter."""
        node = TextNode("This is a **bold** node", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(3, len(result))
        self.assertEqual(TextNode("This is a ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("bold", TextType.BOLD), result[1])
        self.assertEqual(TextNode(" node", TextType.TEXT), result[2])

    def test_split_nodes_delimiter_with_italic(self):
        """Test with italic delimiter."""
        node = TextNode("This is an _italic_ node", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="_", text_type=TextType.ITALIC)
        
        self.assertEqual(3, len(result))
        self.assertEqual(TextNode("This is an ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("italic", TextType.ITALIC), result[1])
        self.assertEqual(TextNode(" node", TextType.TEXT), result[2])
    
    def test_split_nodes_delimiter_with_code(self):
        """Test with code delimiter."""
        node = TextNode("This is a `code` node", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="`", text_type=TextType.CODE)
        
        self.assertEqual(3, len(result))
        self.assertEqual(TextNode("This is a ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("code", TextType.CODE), result[1])
        self.assertEqual(TextNode(" node", TextType.TEXT), result[2])
    
    def test_split_nodes_delimiter_multiple_pairs(self):
        """Test with multiple delimiter pairs."""
        node = TextNode("**Bold1** normal **Bold2**", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(3, len(result))
        self.assertEqual(TextNode("Bold1", TextType.BOLD), result[0])
        self.assertEqual(TextNode(" normal ", TextType.TEXT), result[1])
        self.assertEqual(TextNode("Bold2", TextType.BOLD), result[2])
    
    def test_split_nodes_delimiter_adjacent_pairs(self):
        """Test with adjacent delimiter pairs."""
        node = TextNode("**Bold1**_Italic1_", TextType.TEXT)
        # First split by bold
        result1 = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        # Then split by italic
        result2 = split_nodes_delimiter(old_nodes=result1, delimiter="_", text_type=TextType.ITALIC)
        
        self.assertEqual(2, len(result2))
        self.assertEqual(TextNode("Bold1", TextType.BOLD), result2[0])
        self.assertEqual(TextNode("Italic1", TextType.ITALIC), result2[1])
    
    def test_split_nodes_delimiter_with_non_text_nodes(self):
        """Test with a mix of text and non-text nodes."""
        text_node = TextNode("This is **bold**", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        nodes = [text_node, bold_node]
        
        result = split_nodes_delimiter(old_nodes=nodes, delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(3, len(result))
        self.assertEqual(TextNode("This is ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("bold", TextType.BOLD), result[1])
        self.assertEqual(bold_node, result[2])
    
    def test_split_nodes_delimiter_missing_closing(self):
        """Test with missing closing delimiter."""
        node = TextNode("This has **bold without closing", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
    
    def test_split_nodes_delimiter_missing_closing(self):
        """Test with missing closing delimiter."""
        node = TextNode("This has **bold without closing", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
    
    def test_split_nodes_delimiter_empty_content(self):
        """Test with empty content between delimiters."""
        node = TextNode("Empty bold: ****", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(2, len(result))
        self.assertEqual(TextNode("Empty bold: ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("", TextType.BOLD), result[1])
    
    def test_split_nodes_delimiter_at_beginning(self):
        """Test with delimiter at the beginning of text."""
        node = TextNode("**Bold** at beginning", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(2, len(result))
        self.assertEqual(TextNode("Bold", TextType.BOLD), result[0])
        self.assertEqual(TextNode(" at beginning", TextType.TEXT), result[1])
    
    def test_split_nodes_delimiter_at_end(self):
        """Test with delimiter at the end of text."""
        node = TextNode("At end **Bold**", TextType.TEXT)
        result = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        
        self.assertEqual(2, len(result))
        self.assertEqual(TextNode("At end ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("Bold", TextType.BOLD), result[1])



class TestExtractMarkdownImages(unittest.TestCase):
    """Suite of tests for extract_markdown_images."""

    def setUp(self):
        """Setup the values."""
        self.text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    def test_extract_markdown_limages(self):
        """Test basic extraction."""
        result = extract_markdown_images(self.text)
        self.assertEqual(result, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])
        
        

class TestExtractMarkdownLinks(unittest.TestCase):
    """Suite of tests for extract_markdown_links."""

    def setUp(self):
        """Setup the values."""
        self.text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

    def test_extract_markdown_links(self):
        """Test basic extraction."""
        result = extract_markdown_links(self.text)
        self.assertEqual(result,  [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])

        

class TestSplitNodesImage(unittest.TestCase):
    """Suite of tests for split_nodes_image."""

    def test_split_images(self):
        """Test split image nodes."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_images(self):
        """Test when there are no images in the input."""
        node = TextNode("This is text with no images!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_single_image(self):
        """Test when there is a single image in the text."""
        node = TextNode(
            "This is text with a single ![image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a single ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_image_at_start_and_end(self):
        """Test when images appear at the beginning and end of the text."""
        node = TextNode(
            "![start-image](https://i.imgur.com/start.png) and some text and ![end-image](https://i.imgur.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start-image", TextType.IMAGE, "https://i.imgur.com/start.png"),
                TextNode(" and some text and ", TextType.TEXT),
                TextNode("end-image", TextType.IMAGE, "https://i.imgur.com/end.png"),
            ],
            new_nodes,
        )

    def test_text_with_only_image(self):
        """Test when the input text contains only a single image."""
        node = TextNode(
            "![only-image](https://i.imgur.com/only.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only-image", TextType.IMAGE, "https://i.imgur.com/only.png"),
            ],
            new_nodes,
        )

    def test_multiple_consecutive_images(self):
        """Test when multiple images appear with no text in between."""
        node = TextNode(
            "![image1](https://i.imgur.com/img1.png)![image2](https://i.imgur.com/img2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/img1.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/img2.png"),
            ],
            new_nodes,
        )

    def test_malformed_image_markdown(self):
        """Test when the input text contains malformed image markdown."""
        node = TextNode(
            "This text contains a malformed image ![broken-image]https://i.imgur.com/broken.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )
    
    def test_image_with_no_alt_text(self):
        """Test when the image markdown has no alt text."""
        node = TextNode(
            "This text has an image without alt text ![](https://i.imgur.com/noalt.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has an image without alt text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/noalt.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_large_text_with_images(self):
        """Test very large text with multiple images."""
        text = (
            "This is a huge wall of text with images ![image1](https://img1.com) "
            + "and more text and ![image2](https://img2.com). " * 1000  # Repeat pattern
        )
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        # Simplified check: just ensure the output size matches expectations
        self.assertGreater(len(new_nodes), 2000)  # Lots of nodes are created!
    
    def test_broken_url_image(self):
        """Test when the image markdown has a broken or missing URL."""
        node = TextNode(
            "This text has ![an image without a URL](). And another broken one ![broken-image](broken-url).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("an image without a URL", TextType.IMAGE, ""),
                TextNode(". And another broken one ", TextType.TEXT, None),
                TextNode("broken-image", TextType.IMAGE, "broken-url"),
                TextNode(".", TextType.TEXT, None),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    """Suite of tests for split_nodes_link."""

    def test_split_links(self):
        """Test split link nodes."""
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://example.org"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        """Test when there are no links in the input."""
        node = TextNode("This is text with no links!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_single_link(self):
        """Test when there is a single link in the text."""
        node = TextNode(
            "This is text with a single [link](https://example.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a single ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_start_and_end(self):
        """Test when links appear at the beginning and end of the text."""
        node = TextNode(
            "[start-link](https://example.com/start) and some text and [end-link](https://example.com/end)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start-link", TextType.LINK, "https://example.com/start"),
                TextNode(" and some text and ", TextType.TEXT),
                TextNode("end-link", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    def test_text_with_only_link(self):
        """Test when the input text contains only a single link."""
        node = TextNode(
            "[only-link](https://example.com/only)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("only-link", TextType.LINK, "https://example.com/only"),
            ],
            new_nodes,
        )

    def test_multiple_consecutive_links(self):
        """Test when multiple links appear with no text in between."""
        node = TextNode(
            "[link1](https://example.com/1)[link2](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://example.com/1"),
                TextNode("link2", TextType.LINK, "https://example.com/2"),
            ],
            new_nodes,
        )

    def test_malformed_link_markdown(self):
        """Test when the input text contains malformed link markdown."""
        node = TextNode(
            "This text contains a malformed link [broken-link](https://example.com/broken",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_link_with_no_text(self):
        """Test when the link markdown has no text."""
        node = TextNode(
            "This text has a link without text [](https://example.com/notext).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has a link without text ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com/notext"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_large_text_with_links(self):
        """Test very large text with multiple links."""
        text = (
            "This is a huge wall of text with links [link1](https://example.com/1) "
            + "and more text and [link2](https://example.com/2). " * 100  # Repeat pattern
        )
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        # Simplified check: just ensure the output size matches expectations
        self.assertGreater(len(new_nodes), 200)  # Lots of nodes are created!

    def test_broken_url_link(self):
        """Test when the link markdown has a broken or missing URL."""
        node = TextNode(
            "This text has [a link without a URL](). And another broken one [broken-link](broken-url).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("a link without a URL", TextType.LINK, ""),  # Empty URL
                TextNode(". And another broken one ", TextType.TEXT),
                TextNode("broken-link", TextType.LINK, "broken-url"),  # Invalid URL processed as is
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_not_treated_as_link(self):
        """Test that image markdown is not treated as a link."""
        node = TextNode(
            "This contains an image ![image](https://example.com/image.jpg) and a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This contains an image ![image](https://example.com/image.jpg) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

def test_link_within_code_block(self):
    """Test handling of link within a code block (which should be preserved)."""
    node = TextNode(
        "This is a code block: `function([param](https://example.com))` and a real [link](https://real.com)",
        TextType.TEXT,
    )
    # Note: A more sophisticated parser might ignore links in code blocks
    # But for now, we'll expect the simple behavior based on your implementation
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is a code block: `function(", TextType.TEXT),
            TextNode("param", TextType.LINK, "https://example.com"),
            TextNode(")` and a real ", TextType.TEXT),  # Changed from "))` to ")`
            TextNode("link", TextType.LINK, "https://real.com"),
        ],
        new_nodes,
    )

    def test_empty_input(self):
        """Test with empty input."""
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    def test_non_text_nodes(self):
        """Test that non-text nodes are preserved."""
        image_node = TextNode("image", TextType.IMAGE, "https://example.com/image.jpg")
        text_node = TextNode("This is a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([image_node, text_node])
        self.assertListEqual(
            [
                image_node,
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    """Suite of tests for text_to_text_nodes."""

    def test_transform(self):
        """Test text to list of TextNodes."""

        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )