import unittest

from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def test_to_html(self):
        htmlnode = HTMLNode("<p>", "This is a paragraph of text.", None,{"t1":"vt1","l1":"http://l1"})
        self.assertEqual(HTMLNode.props_to_html(htmlnode)," t1=vt1 l1=http://l1")
    
    def test_to_html_props(self):
        list = []
        list.append(HTMLNode("<h1>", "Heading 1"))
        list.append(HTMLNode("<h2>", "Heading 2"))

        props = {
            "href": "https://www.google.com",
            "target": "_blank"
                }
       
        htmlnode = HTMLNode("<h3>", "Heading 2", list, props)
        self.assertEqual(HTMLNode.props_to_html(htmlnode), " href=https://www.google.com target=_blank")

def test_values(self):
        list = []
        list.append(HTMLNode("<h1>", "Heading 1"))
        list.append(HTMLNode("<h2>", "Heading 2"))

        props = {
            "href": "https://www.google.com",
            "target": "_blank"
                }
       
        #htmlnode = HTMLNode("<h3>", "Heading 2", list, props)
        htmlnode = HTMLNode("<h3>", "Heading 2", list, props)
        self.assertEqual(htmlnode.tag, "<h3>")

        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            None,
        )

def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

def test_parent_node_to_html_p(self):
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


if __name__ == "__main__":
    unittest.main()
