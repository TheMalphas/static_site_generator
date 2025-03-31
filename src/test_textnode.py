import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    """Test suite for TextNode."""

    def test_eq(self):
        """Test eq method."""

        node = TextNode('This is a text node', TextType.BOLD)

        with self.subTest("Assert text equal."):
            node2 = TextNode('This is a text node', TextType.BOLD)
            self.assertEqual(node, node2)

        with self.subTest("Assert text not equal."):
            node2 = TextNode('This is not a text node', TextType.BOLD)
            self.assertNotEqual(node, node2)

        with self.subTest("Assert text_type not equal."):
            node2 = TextNode('This is a text node', TextType.LINK)
            self.assertNotEqual(node, node2)

        with self.subTest("Assert url not equal."):
            node2 = TextNode('This is a text node', TextType.BOLD, 'http://test.test')
            self.assertNotEqual(node, node2)


if __name__ == '__main__':
    unittest.main()