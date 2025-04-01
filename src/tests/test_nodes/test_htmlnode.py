import unittest

from nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    """Test suite for HTMLNode."""

    def setUp(self):
        """Test setUp method."""
        self.anchor_props: dict = {
                "href": "https://www.google.com",
                "target": "_blank",
            }

    def test_eq(self):
        """Test eq method."""

        node = HTMLNode('This is an html node', value=None, children=None, props=self.anchor_props)

        with self.subTest("Assert text equal."):
            node2 = HTMLNode('This is an html node', value=None, children=None, props=self.anchor_props)
            self.assertEqual(node, node2)

        with self.subTest("Assert text not equal."):
            node2 = HTMLNode('This is a banana')
            self.assertNotEqual(node, node2)


    def test_props_to_html(self):
        """Test props method."""

        node = HTMLNode(tag='p', value=None, children=None, props=self.anchor_props)

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )


if __name__ == '__main__':
    unittest.main()