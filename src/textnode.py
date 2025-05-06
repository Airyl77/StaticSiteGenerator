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
            new_nodes.append(old_nodes)
    
        old_list = old_node.text.split(delimiter)
        match delimiter:
            case "`":
                ttype = TextType.CODE
            case "**":
                ttype = TextType.BOLD
            case "_":
                ttype = TextType.ITALIC
            case _:
                raise Exception(f"Unknown text type for delimeter {delimiter}")
    
        for l in old_list:
            new_nodes.append(TextNode(l, old_node.text_type))
        new_nodes[1].text_type = ttype
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        one_node = old_node
        matches = extract_markdown_images(old_node.text)
        for x,y in matches:
            text_split = one_node.text.split(f"![{x}]({y})", 1)
            new_nodes.append(TextNode(text_split[0], old_node.text_type))
            new_nodes.append(TextNode(x, TextType.IMAGE, y))
            one_node = TextNode(text_split[1], TextType.TEXT)
    return new_nodes


def split_nodes_link(old_nodes):
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