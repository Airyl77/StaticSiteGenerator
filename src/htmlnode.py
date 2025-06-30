#from textnode import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
       self.tag = tag
       self.value = value
       self.children = children
       self.props = props

    def to_html(self):
        raise NotImplementedError
        
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""        
        for i in self.props:
            result += " " + i + "=" + self.props[i]
        return result

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value = {self.value}, children={self.children}, props={self.props})"
   
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")
        if self.children is None:
            raise ValueError("children is missing")
        leafs = ""
        for l in self.children:
            leafs += l.to_html()
         #   if isinstance(l, ParentNode):
         #       leafs += ParentNode.to_html(l)
         #   elif isinstance(l, LeafNode):
         #       leafs += LeafNode.to_html(l)
        return f"<{self.tag}{self.props_to_html()}>{leafs}</{self.tag}>"

        
