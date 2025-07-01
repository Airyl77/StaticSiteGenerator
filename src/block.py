from enum import Enum
from htmlnode import *
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
       self.text = text
       self.text_type = TextType(text_type)
       self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        
    def __repr__(self):
        if self.url is None:
            return f"TextNode({self.text}, {self.text_type.value})"
        return "TextNode(" + self.text + ", " + self.text_type.value + ", " + self.url + ")"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
        
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_old_list = old_node.text.split(delimiter)
        if len(split_old_list) % 2 == 0:
            raise Exception(f"Unknown text type for delimeter {delimiter}")
            
        for i in range(len(split_old_list)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_old_list[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_old_list[i], text_type))
        
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        one_node = old_node
        #print(f"LBO11 one_node = {one_node}")
        matches = extract_markdown_images(old_node.text)
        #print(f"LBO2 matches = {matches}")
        if len(matches) == 0:
            new_nodes.append(one_node)
            continue
        #for x,y in matches:
        for i in range(len(matches)):
            x = matches[i][0]
            y = matches[i][1]
            text_split = one_node.text.split(f"![{x}]({y})", 1)
            #print(f"LBO3 text_split = {text_split}")
            new_nodes.append(TextNode(text_split[0], old_node.text_type))
            new_nodes.append(TextNode(x, TextType.IMAGE, y))
            #print(f"LBO4 len(text_split) = {len(text_split)}")
            if i == len(matches) - 1 and text_split[1] != "":
                new_nodes.append(TextNode(text_split[1], old_node.text_type))
            else:
                one_node = TextNode(text_split[1], TextType.TEXT)
                

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        one_node = old_node
        #print(f"LBO11 one_node = {one_node}")
        matches = extract_markdown_links(old_node.text)
        #print(f"LBO2 matches = {matches}")
        if len(matches) == 0:
            new_nodes.append(one_node)
            continue
        #for x,y in matches:
        for i in range(len(matches)):
            x = matches[i][0]
            y = matches[i][1]
            text_split = one_node.text.split(f"[{x}]({y})", 1)
            #print(f"LBO3 text_split = {text_split}")
            new_nodes.append(TextNode(text_split[0], old_node.text_type))
            new_nodes.append(TextNode(x, TextType.LINK, y))
            #print(f"LBO4 len(text_split) = {len(text_split)}")
            if i == len(matches) - 1 and text_split[1] != "":
                new_nodes.append(TextNode(text_split[1], old_node.text_type))
            else:
                one_node = TextNode(text_split[1], TextType.TEXT)
                

    return new_nodes


def split_nodes_link_old(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        one_node = old_node
        matches = extract_markdown_links(old_node.text)
        for x,y in matches:
            text_split = one_node.text.split(f"[{x}]({y})", 1)
            new_nodes.append(TextNode(text_split[0], old_node.text_type))
            new_nodes.append(TextNode(x, TextType.LINK, y))
            one_node = TextNode(text_split[1], TextType.TEXT)
    return new_nodes

        
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception(f"Unknown text type {text_node.text_type}")
        
def text_to_textnodes(text):
    textnode = TextNode(text, TextType.TEXT)
    textnodes = split_nodes_delimiter([textnode], "`", TextType.CODE)
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    #print(f"LBO1 textnodes = {textnodes}")
    textnodes2 = split_nodes_image(textnodes)
    #print(f"LBO2 textnodes2 = {textnodes2}")
    textnodes3 = split_nodes_link(textnodes2)
    return textnodes3
    
def markdown_to_blocks(markdown):
    print(f"LBO1 markdown = {markdown}")
    blocks = markdown.split("\n\n")
    print(f"LBO2 blocks = {blocks}")
    new_blocks = []
    for block in blocks:
        new_block = block.strip(" \n")
        if new_block != "":
            new_blocks.append(new_block)
    print(f"LBO2 new_blocks = {new_blocks}")
    return new_blocks


    