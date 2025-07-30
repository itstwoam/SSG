from textnode import *
from enum import Enum

def main():
    bender = TextType.PLAIN
    tn = TextNode("This is some anchor text", bender, "https://no.links.here/")
    print(tn)


main()
