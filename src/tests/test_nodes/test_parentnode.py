import unittest

from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    """Test suite for ParentNode."""

    def setUp(self):
        """Test setUp method."""

        self.anchor_props: dict = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        
        self.grand_child = LeafNode(tag='a', value='Test grand child', props=self.anchor_props)
        self.child = ParentNode(tag='b', children=[self.grand_child])
        self.parent = ParentNode(tag='span', children=[self.child])

    def test_to_html_with_grandchildren(self):
        """Test props method."""

        node = ParentNode(tag='p', children=[self.grand_child])
        html_string = node.to_html()

        self.assertEqual(
            html_string,
            '<p><a href="https://www.google.com" target="_blank">Test grand child</a></p>'
        )

    def test_to_html_with_grandchildren(self):
        """Test props method."""

        node = ParentNode(tag='p', children=[self.child])
        html_string = node.to_html()

        self.assertEqual(
            html_string,
            '<p><b><a href="https://www.google.com" target="_blank">Test grand child</a></b></p>'
        )

    def test_to_html_with_parent(self):
        """Test props method."""

        node = ParentNode(tag='p', children=[self.parent])
        html_string = node.to_html()

        self.assertEqual(
            html_string,
            '<p><span><b><a href="https://www.google.com" target="_blank">Test grand child</a></b></span></p>'
        )

    def test_to_html_without_children(self):
        """Test props method."""

        with self.assertRaises(ValueError) as context:
            ParentNode(tag='p', children=None)

            error_msg=str(context.exception)
            self.assertEqual(error_msg, 'Children are required')

    def test_to_html_missing_children(self):
        """Test props method."""

        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag='p', children=None)
            node.to_html()

        error_msg=str(context.exception)
        self.assertEqual(error_msg, 'Children are required')


if __name__ == '__main__':
    unittest.main()