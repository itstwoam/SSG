import sys
import os
from mcopy import copy
from textnode import *
from enum import Enum
from functions import extract_title, generate_page, generate_pages_recursive

def main():
    basepath = "/"
    if sys.argv[1]:
        basepath = sys.argv[1]
    copy("./static", "./docs")
    generate_page(basepath, "../content/index.md", "../template.html", "../docs/index.html")
    generate_pages_recursive(basepath, "../content", "../template.html", "../docs")
main()
