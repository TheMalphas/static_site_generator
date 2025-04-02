import unittest

from nodes.textnode import TextNode, TextType, text_node_to_html_node

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

    def test_transform_text_node_to_leaf_node(self):
        """Test transform TextNode to LeafNode."""
        text = 'This is a '

        with self.subTest('Transform text'):
            text += 'text node'
            node = TextNode(text, TextType.TEXT)
            
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, None)
            self.assertEqual(html_node.value, text)

        with self.subTest('Transform bold'):
            text += 'bold node'
            node = TextNode(text, TextType.BOLD)

            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, 'b')
            self.assertEqual(html_node.value, text)

        with self.subTest('Transform italic'):
            text += 'italic node'
            node = TextNode(text, TextType.ITALIC)

            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, 'i')
            self.assertEqual(html_node.value, text)

        with self.subTest('Transform code'):
            text += 'code node'
            node = TextNode(text, TextType.CODE)

            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, 'code')
            self.assertEqual(html_node.value, text)

        with self.subTest('Transform link'):
            text += 'link node'
            node = TextNode(text, TextType.LINK)

            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, 'a')
            self.assertEqual(html_node.value, text)

        with self.subTest('Transform image'):
            text += 'image node'
            url = 'https://google.com'
            node = TextNode(text, TextType.IMAGE, url=url)

            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, 'img')
            self.assertEqual(html_node.props, {'alt':text, 'src':url})

if __name__ == '__main__':
    unittest.main()