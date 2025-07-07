import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_isUrlNone(self):
        node = TextNode("This is a text node bold", TextType.BOLD)
        self.assertTrue(node.url is None)

    def test_split_del(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
       # print(f"LBO new_nodes{new_nodes}")

        check_nodes = [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                     ]

        #print(f"LBO check_nodes{check_nodes}")
        self.assertEqual(new_nodes, check_nodes)

    def test_regexp_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_regexp_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_images(self):
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

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        #print(f"LBO link2 new_nodes = {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],           
            new_nodes,
        )

    def test_split_images2(self):
        node = [TextNode(
            "This is **text** with an _italic_ word and a `code block`",
            TextType.TEXT,
        ),TextNode(
            " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        ]
        new_nodes = split_nodes_image(node)
        #print(f"LBO images2 new_nodes = {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is **text** with an _italic_ word and a `code block`", TextType.TEXT),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a [link](https://boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_link2(self):
        node = [TextNode(
            "This is **text** with an _italic_ word and a `code block`",
            TextType.TEXT,
        ),TextNode(
            " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        ]
        new_nodes = split_nodes_link(node)
        # print(f"LBO link2 new_nodes = {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is **text** with an _italic_ word and a `code block`", TextType.TEXT),
                TextNode(" and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
             ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        #print(f"LBO test_text_to_nodes new_nodes = {new_nodes}")
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
            ]
            ,           
            new_nodes,
        )

    def test_markdown_to_blocks(self):
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

    def test_block_to_block_type(self):
        md = "###### Heading6"
       # blocks = markdown_to_blocks(md)
        self.assertEqual(
            block_to_block_type(md),
            BlockType.heading,
        )

    def test_block_to_block_type2(self):
        md = """```
This is code
```"""
       # blocks = markdown_to_blocks(md)
        self.assertEqual(
            block_to_block_type(md),
            BlockType.code,
        )

    def test_block_to_block_type_quote(self):
        md = "> I am in fact a Hobbit in all but size."

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            block_to_block_type(md),
            BlockType.quote,
        )

    def test_block_to_block_type_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3"""
       # blocks = markdown_to_blocks(md)
        print("LBO test_block_to_block_type_unordered_list")
        self.assertEqual(
            block_to_block_type(md),
            BlockType.unordered_list,
        )

    def test_block_to_block_type_ordered_list(self):
        md = """1. Item 1
2. Item 2
3. Item 3"""
       # blocks = markdown_to_blocks(md)
        print("LBO test_block_to_block_type_ordered_list")
        self.assertEqual(
            block_to_block_type(md),
            BlockType.ordered_list,
        )

    def _test_paragraphs(self):
#        md = """
#This is **bolded** paragraph
#text in a p
#tag here
#
#This is another paragraph with _italic_ text and `code` here
#
#"""
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def _test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_unordered_list(self):
        md = """[Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
[Why Tom Bombadil Was a Mistake](/blog/tom)
[The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        
        print(f"LBO =>>>>>>>>>>>>>> node={node}")
        
        print(f"LBO =>>>>>>>>>>>>>> html={html}")
        self.assertEqual(
            html,
            "<div><ul><li>Item 1\n</li><li>Item 2\n</li><li>Item 3</li></ul></div>",
        )

    def _test_ordered_list(self):
        md = """1. Item 1
2. Item 2
3. Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

    def _test_heading(self):
        md = """# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_heading2(self):
        md = """# Heading 1

## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
"""

        node = extract_title(md)
        self.assertEqual(
            node,
            "Heading 1",
        )


        

if __name__ == "__main__":
    unittest.main()

