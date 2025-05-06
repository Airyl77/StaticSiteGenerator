from textnode import *

def main():
    obj_TextNode = TextNode("This is some anchor text", TextType.LINK_TEXTTYPE, "https://www.boot.dev")
    print(obj_TextNode)

if __name__ == "__main__":
    main()