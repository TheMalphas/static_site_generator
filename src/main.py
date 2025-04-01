from nodes.textnode import TextNode
from nodes.htmlnode import HTMLNode

def main():
   text_node = TextNode("Test", 'code', "http://text.text")
   html_node = HTMLNode('This is an html node')


if '__main__' == __name__:
   main()
