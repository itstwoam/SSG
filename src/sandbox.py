from functions import markdown_to_block

input_text = "This is a paragraph\nthat spans multiple lines.\n\nAnother one here."
expected = [
    "This is a paragraph\nthat spans multiple lines.",
    "Another one here."
]
print(markdown_to_block(input_text))
