from enum import Enum
from htmlnode import LeafNode, ParentNode
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
    #print(f"LBO1 markdown = {markdown}")
    blocks = markdown.split("\n\n")
    #blocks = markdown.split("\n")
    #print(f"LBO2 blocks = {blocks}")
    new_blocks = []
    for block in blocks:
        new_block= block.strip(" \n")
       # new_block = new_block1.strip("\n")
        if new_block != "":
            new_blocks.append(new_block)
    #print(f"LBO2 new_blocks = {new_blocks}")
    return new_blocks

BlockType = Enum('BlockType', ['paragraph','heading','code','quote','unordered_list','ordered_list'])

def block_to_block_type(block):
    
    #print(f"LBO block1={block[0:3]}_")
    #print(f"LBO block2={block[-3:]}_")
    #print(f"LBO block2={(block[0:7]).lstrip("#")}_")
    if block[0:7].lstrip("#")[0] == " ":
        return BlockType.heading
    elif block[0:3] == "```" and block[-3:] == "```":
        return BlockType.code
    else:
        strings = block.split("\n")
        if isQuote(strings):
            return BlockType.quote
        elif isUnordered(strings):
            return BlockType.unordered_list
        elif isOrdered(strings):
            return BlockType.ordered_list
        else:
            return BlockType.paragraph
            
def isQuote(strings):
    for string in strings:
        if string[0] != ">":
            return False
    return True

def isUnordered(strings):
    for string in strings:
        if string[0:2] != "- ":
            return False
    return True

def isOrdered(strings):
    i = 1
    for string in strings:
        #print(f"LBO3 string ={string}, i={i}")
        s = string.split(".", 1)
        n = str(i)
        #print(f"LBO3 s ={s}")
        if s == string:
            #print(f"LBO4 s ={s}")
            return False
        elif s[0] != n:
            #print(f"LBO5 s[0] ='{s[0]}'")
            return False
        elif s[1][0] != " ":
            #print(f"LBO6 s[1][0]={s[1][0]}")
            return False
        i += 1
    #print(f"LBO7={s}")
    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    #print(f"LBO10 blocks={blocks}")
    child_nodes = ""
    for block in blocks:
        type_block = block_to_block_type(block)
        #print(f"LBO10 type_block={type_block}")
        #text_node_to_html_node
        #new_HTMLNode = 
        #print(f"LBO12 block={block}")
        
        #print(f"LBO12_0 st={st}")        
        match type_block:
            case BlockType.paragraph:
                st = text_to_children(block)
                child_nodes += "<p>" + st + "</p>"
                #print(f"LBO12_1 st={st}")
            case BlockType.quote:
                st = text_to_children(block)
                st1 = st[2:]
                child_nodes += "<blockquote>" + st1 + "</blockquote>"
                #print(f"LBO12_2 st={st}")
            case BlockType.unordered_list:
                list_st = block.split("- ")
                st = ""
                for l in list_st:
                    if l != "":
                        st1 = text_to_children(l)
                        st += "<li>" + st1.strip("\n") + "</li>"
                #print(f"LBO12_3 st={st}")
                child_nodes += "<ul>" + st + "</ul>"
                
            case BlockType.ordered_list:
                list_st = block.split("\n")
                st = ""
                for l in list_st:
                    if l != "":
                        l2 = l.split(". ", 1)
                        #print(f"LBO12_52 l2={text_to_children(l2[1])}")
                        st1 = text_to_children(l2[1])
                        st += "<li>" + st1.strip("\n") + "</li>"
                #print(f"LBO12_5 st={st}")
                child_nodes += "<ol>" + st + "</ol>"
            case BlockType.heading:
                list_st = block.split("\n")
                st = ""
                #print(f"LBO12_50000 list_st___={list_st}")
                for l in list_st:
                    if l != "":
                        l2 = l.split(" ", 1)
                        n = len(l2[0])
                        #print(f"LBO12_52 n and l2_0={l2[0]}, {l2[1]}")
                        st += f"<h{n}>"+ text_to_children(l2[1]) + f"</h{n}>"
                        #print(f"LBO12_5 st___={st}")
                child_nodes += st
            case BlockType.code:
                st = block.split("```")[1].lstrip("\n")
                #print(f"LBO12_56666666 list_st={st}")
                child_nodes += "<pre><code>" + st + "</code></pre>"
                #print(f"LBO12_5 st={st}")
    #print(f"LBO12 child_nodes={child_nodes}")
    parent_node = ParentNode("div", [LeafNode(None, child_nodes)])
    #print(f"LBO12 parent_node={parent_node}")
    return parent_node
        

        
def text_to_children(text):
    #print(f"LBO11 text={text}")
    textnodes = text_to_textnodes(text)
    #print(f"LBO11 textnodes={textnodes}")
    children = ""
    for textnode in textnodes:
        html_node = text_node_to_html_node(textnode)
        #print(f"LBO11 html_node={html_node}")
        #children.append(html_node)
        children += html_node.to_html()
        #print(f"LBO11 html_node.to_html={html_node.to_html()}")
        #print(f"LBO11 children={children}")
    return children
    #t takes a string of text and returns a list 
    #of HTMLNodes that represent the inline markdown using previously 
    #created functions (think TextNode -> HTMLNode).

def extract_title(markdown):
    list = markdown.split("\n")
    #print(f"LBO markdown={markdown}")
    for st in list:
        if st.startswith("# "):
            return (st.strip("#")).strip(" ")
    raise Exception("there is no h1 header")