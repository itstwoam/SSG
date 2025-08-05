import os
from mcopy import copy
from textnode import *
from enum import Enum
from functions import extract_title, generate_page, generate_pages_recursive

def main():
    copy("./static", "./public")
    generate_page("../content/index.md", "../template.html", "../public/index.html")
    generate_pages_recursive("../content", "../template.html", "../public")
main()
