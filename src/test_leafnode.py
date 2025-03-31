import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    """Test suite for LeafNode."""

    def setUp(self):
        """Test setUp method."""


        self.anchor_props: dict = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        
        self.image_props: dict = {
                "src": "url/of/image.jpg",
                "alt": "Description of image",
            }

        
    def test_no_value(self):
        """Test raise ValueError."""

        with self.assertRaises(ValueError) as context:
            LeafNode(tag='This is a leaf node', value=None, props=self.anchor_props)

            error_msg = str(context.exception)
            self.assertEqual(error_msg, 'Value is required')
    

    def test_eq(self):
        """Test eq method."""

        node = LeafNode(tag='This is a leaf node', value='Test value', props=self.anchor_props)

        with self.subTest("Assert text equal."):
            node2 = LeafNode(tag='This is a leaf node', value='Test value', props=self.anchor_props)
            self.assertEqual(node, node2)

        with self.subTest("Assert text not equal."):
            node2 = LeafNode(tag='This is a banana', value='Test value',)
            self.assertNotEqual(node, node2)


    def test_to_html(self):
        """Test to_html method."""

        with self.subTest('Test simple tags'):
            tags: list[str] = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'p', 'i', 'ol', 'ul', 'blockquote', 'span', 'div']

            for tag in tags:
                node = LeafNode(tag=tag, value='Test value')
                self.assertEqual(node.to_html(), f'<{tag}>Test value</{tag}>')

        with self.subTest('Test anchor tag'):
            tag = 'a'

            node = LeafNode(tag=tag, value='Test value', props=self.anchor_props)
            self.assertEqual(node.to_html(), f'<a href="{self.anchor_props['href']}" target="{self.anchor_props['target']}">{node.value}</a>')

        with self.subTest('Test image tag'):
            tag = 'img'

            node = LeafNode(tag=tag, value='Test value', props=self.image_props)
            self.assertEqual(node.to_html(), f'<img src="{self.image_props['src']}" alt="{self.image_props['alt']}" {node.value} />')

        with self.subTest('Test code tag'):
            tag = 'code'

            node = LeafNode(tag=tag, value='Test value')
            self.assertEqual(
                node.to_html(), 
                f'```\n{node.value}\n```\n'
                )


        with self.subTest('Test wrong tag'):
            tag = ['s']
            with self.assertRaises(AttributeError) as context:
                node = LeafNode(tag=tag, value='Test value')

                error_msg = str(context.exception)
                self.assertEqual(error_msg, 'Must be a valid TagType.')



if __name__ == '__main__':
    unittest.main()