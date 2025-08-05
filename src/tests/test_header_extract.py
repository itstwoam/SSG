import unittest
from functions import extract_title  # Replace 'your_module' with the actual file name

class TestExtractTitle(unittest.TestCase):



    def test_header_not_at_top(self):
        md = """Intro text.

Another line.

# Hello there!"""
        self.assertEqual(extract_title(md), "Hello there!")



    def test_multiple_headers(self):
        md = """# First Title
## Subtitle
# Second Title"""
        self.assertEqual(extract_title(md), "First Title")


    def test_no_headers(self):
        md = """Just plain text.
No headers here."""
        with self.assertRaises(Exception):
            extract_title(md)






    def test_valid_header(self):
        md = """# Welcome to the jungle
This is a paragraph.

## Section Two
More stuff."""
        self.assertEqual(extract_title(md), "Welcome to the jungle")














    def test_whitespace_title(self):
        md = "#    Title with space     \nContent below."
        self.assertEqual(extract_title(md), "Title with space")


    def test_newmarkdown(self):
        md = """

# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).

"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

if __name__ == '__main__':
    unittest.main()
