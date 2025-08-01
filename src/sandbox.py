#input_text = "This is a paragraph\nthat spans multiple lines.\n\nAnother one here."
from functions import markdown_to_html_node
from enums import *
string = "This is regular text.\n\n**This text is bold.**\n\n_This text is italic._\n\n`This text is displayed as inline code.`\n\nHere is a [hyperlink to Python's homepage](https://www.python.org).\n\n![Alt text for image](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)\n\n1. First item in ordered list\n2. Second item in ordered list\n3. Third item in ordered list\n\n- First item in unordered list\n- Second item in unordered list\n- Third item in unordered list"
print(markdown_to_html_node(string))
