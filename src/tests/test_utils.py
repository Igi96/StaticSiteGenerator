import unittest
from src.textnode import TextNode
from src.utils import *

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_single_delimiter(self):
        """Test splitting a single delimiter in the text."""
        node = TextNode("This is a `code block` example", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected_output = [
            TextNode("This is a ", "text"),
            TextNode("code block", "code"),
            TextNode(" example", "text"),
        ]

        self.assertEqual(new_nodes, expected_output)

    def test_empty_text_node(self):
        """Test when an empty text node is passed."""
        node = TextNode("", "text")  # Use text_type instead of type
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected_output = [TextNode("", "text")]

        self.assertEqual(new_nodes, expected_output)

    def test_no_text_type_node(self):
        """Test when non-text type nodes are passed."""
        node = TextNode("This should remain unchanged.", "bold")  # Non-text node type
        new_nodes = split_nodes_delimiter([node], "`", "code")

        expected_output = [
            TextNode("This should remain unchanged.", "bold"),
        ]

        self.assertEqual(new_nodes, expected_output)



class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        """Test extracting a single Markdown image."""
        text = "This is an image ![alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple(self):
        """Test extracting multiple Markdown images."""
        text = "This has two images ![first image](https://example.com/1.png) and ![second image](https://example.com/2.png)"
        result = extract_markdown_images(text)
        expected = [
            ("first image", "https://example.com/1.png"),
            ("second image", "https://example.com/2.png")
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_no_image(self):
        """Test when there are no images in the text."""
        text = "This text has no images."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_images_malformed(self):
        """Test when there is a malformed image in the text."""
        text = "This is a malformed image ![alt text](example.com/image.png"
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)



class TestExtractMarkdownLinks(unittest.TestCase):

    def test_extract_markdown_links_single(self):
        """Test extracting a single Markdown link."""
        text = "This is a link [to example](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("to example", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        """Test extracting multiple Markdown links."""
        text = "This has two links [first link](https://example.com/1) and [second link](https://example.com/2)"
        result = extract_markdown_links(text)
        expected = [
            ("first link", "https://example.com/1"),
            ("second link", "https://example.com/2")
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_no_link(self):
        """Test when there are no links in the text."""
        text = "This text has no links."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_links_malformed(self):
        """Test when there is a malformed link in the text."""
        text = "This is a malformed link [example](https://example.com"
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)



class TestSplitNodesLink(unittest.TestCase):

    def test_split_nodes_link_single(self):
        """Test splitting a single Markdown link."""
        node = TextNode("This is a link [boot dev](https://www.boot.dev)", text_type_text)
        new_nodes = split_nodes_link([node])
        
        expected_output = [
            TextNode("This is a link ", text_type_text),
            TextNode("boot dev", text_type_link, "https://www.boot.dev")
        ]

        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_link_multiple(self):
        """Test splitting multiple Markdown links."""
        node = TextNode("Here is [boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com)", text_type_text)
        new_nodes = split_nodes_link([node])

        expected_output = [
            TextNode("Here is ", text_type_text),
            TextNode("boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode("youtube", text_type_link, "https://www.youtube.com")
        ]

        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_link_no_link(self):
        """Test when there is no Markdown link in the node."""
        node = TextNode("This is plain text with no links.", text_type_text)
        new_nodes = split_nodes_link([node])

        expected_output = [node]
        self.assertEqual(new_nodes, expected_output)





class TestSplitNodesImage(unittest.TestCase):


    def test_split_nodes_image_single(self):
        """Test splitting a single Markdown image."""
        node = TextNode("This is an image ![boot logo](https://www.boot.dev/logo.png)", text_type_text)
        new_nodes = split_nodes_image([node])

        expected_output = [
            TextNode("This is an image ", text_type_text),
            TextNode("boot logo", text_type_image, "https://www.boot.dev/logo.png")
        ]

        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_image_multiple(self):
        """Test splitting multiple Markdown images."""
        node = TextNode("Here is an image ![boot logo](https://www.boot.dev/logo.png) and another ![youtube logo](https://www.youtube.com/logo.png)", text_type_text)
        new_nodes = split_nodes_image([node])

        expected_output = [
            TextNode("Here is an image ", text_type_text),
            TextNode("boot logo", text_type_image, "https://www.boot.dev/logo.png"),
            TextNode(" and another ", text_type_text),
            TextNode("youtube logo", text_type_image, "https://www.youtube.com/logo.png")
        ]

        self.assertEqual(new_nodes, expected_output)

    def test_split_nodes_image_no_image(self):
        """Test when there is no Markdown image in the node."""
        node = TextNode("This is plain text with no images.", text_type_text)
        new_nodes = split_nodes_image([node])

        expected_output = [node]
        self.assertEqual(new_nodes, expected_output)



class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        """Test with plain text, no formatting."""
        text = "This is just plain text."
        expected_output = [
            TextNode("This is just plain text.", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_bold_text(self):
        """Test with bold formatting."""
        text = "This is **bold** text."
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text.", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_italic_text(self):
        """Test with italic formatting."""
        text = "This is *italic* text."
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text.", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_code_text(self):
        """Test with code block formatting."""
        text = "This is `code block`."
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_mixed_formatting(self):
        """Test with mixed bold, italic, and code formatting."""
        text = "This is **bold**, *italic*, and `code block`."
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(", ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(", and ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_with_link(self):
        """Test with a Markdown link."""
        text = "Here is a [link](https://example.com)."
        expected_output = [
            TextNode("Here is a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_with_image(self):
        """Test with a Markdown image."""
        text = "Here is an ![image](https://example.com/image.png)."
        expected_output = [
            TextNode("Here is an ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.png"),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_complex_text(self):
        """Test with complex text, including bold, italic, code, image, and link."""
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)."
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)



class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_heading(self):
        """Test with a single Markdown heading."""
        markdown = "# This is a heading"
        expected_output = [
            "# This is a heading"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

    def test_paragraph(self):
        """Test with a single paragraph."""
        markdown = "This is a paragraph of text."
        expected_output = [
            "This is a paragraph of text."
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

    def test_multiple_blocks(self):
        """Test with a heading, a paragraph, and a list."""
        markdown = """
# This is a heading

This is a paragraph of text.

* List item 1
* List item 2
"""
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text.",
            "* List item 1\n* List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

    def test_extra_whitespace(self):
        """Test with extra newlines and whitespace around the blocks."""
        markdown = """
        
        # Heading with leading and trailing whitespace   
        
        This is a paragraph with extra spaces.   
        
        * List item 1  
        * List item 2    
        
        """
        expected_output = [
            "# Heading with leading and trailing whitespace",
            "This is a paragraph with extra spaces.",
            "* List item 1\n* List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

    def test_empty_blocks(self):
        """Test with empty blocks due to excessive newlines."""
        markdown = """
# Heading

This is a paragraph.


* List item 1
* List item 2
"""
        expected_output = [
            "# Heading",
            "This is a paragraph.",
            "* List item 1\n* List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

    def test_all_empty_blocks(self):
        """Test with only newlines and empty blocks."""
        markdown = "\n\n\n\n"
        expected_output = []
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

    def test_single_list_block(self):
        """Test with a single list block."""
        markdown = """
* List item 1
* List item 2
"""
        expected_output = [
            "* List item 1\n* List item 2"
        ]
        self.assertEqual(markdown_to_blocks(markdown), expected_output)

if __name__ == "__main__":
    unittest.main()



class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        """Test with headings of different levels."""
        self.assertEqual(block_to_block_type("# Heading level 1"), 'heading')
        self.assertEqual(block_to_block_type("## Heading level 2"), 'heading')
        self.assertEqual(block_to_block_type("###### Heading level 6"), 'heading')

    def test_code_block(self):
        """Test with code block."""
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), 'code block')

    def test_quote_block(self):
        """Test with a quote block."""
        block = "> This is a quote\n> Another quote line"
        self.assertEqual(block_to_block_type(block), 'quote block')

    def test_unordered_list(self):
        """Test with unordered list blocks."""
        block = "* List item 1\n* List item 2\n* List item 3"
        self.assertEqual(block_to_block_type(block), 'unordered list')
        
        block = "- List item 1\n- List item 2\n- List item 3"
        self.assertEqual(block_to_block_type(block), 'unordered list')

    def test_ordered_list(self):
        """Test with a valid ordered list."""
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), 'ordered list')

    def test_invalid_ordered_list(self):
        """Test with an invalid ordered list (numbers out of order)."""
        block = "1. First item\n3. Third item\n2. Second item"
        self.assertEqual(block_to_block_type(block), 'paragraph')

    def test_paragraph(self):
        """Test with a normal paragraph."""
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), 'paragraph')

    def test_empty_block(self):
        """Test with an empty block."""
        block = ""
        self.assertEqual(block_to_block_type(block), 'paragraph')






class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_single_heading(self):
        """Test Markdown with a single heading."""
        markdown = "# Heading Level 1"
        html_node = markdown_to_html_node(markdown)
        expected_output = '<h1>Heading Level 1</h1>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_paragraph(self):
        """Test Markdown with a single paragraph."""
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        expected_output = '<p>This is a paragraph.</p>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_unordered_list(self):
        """Test Markdown with an unordered list."""
        markdown = """
* List item 1
* List item 2
* List item 3
"""
        html_node = markdown_to_html_node(markdown)
        expected_output = '<ul><li>List item 1</li><li>List item 2</li><li>List item 3</li></ul>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_ordered_list(self):
        """Test Markdown with an ordered list."""
        markdown = """
1. First item
2. Second item
3. Third item
"""
        html_node = markdown_to_html_node(markdown)
        expected_output = '<ol><li>First item</li><li>Second item</li><li>Third item</li></ol>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_code_block(self):
        """Test Markdown with a code block."""
        markdown = """


```
print('Hello, World!')
```

"""
        html_node = markdown_to_html_node(markdown)
        expected_output = '<pre>print(\'Hello, World!\')</pre>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_quote_block(self):
        """Test Markdown with a quote block."""
        markdown = """
> This is a quote.
> Another quote line.
"""
        html_node = markdown_to_html_node(markdown)
        expected_output = '<blockquote>This is a quote.\nAnother quote line.</blockquote>'
        self.assertEqual(html_node.to_html(), expected_output)

    def test_complex_markdown(self):
        """Test Markdown with multiple elements (heading, paragraph, list, code, quote)."""
        markdown = """
# Heading Level 1

This is a paragraph.

* List item 1
* List item 2

```
print('Code block')
```

> This is a quote
"""
        html_node = markdown_to_html_node(markdown)
        expected_output = (
            '<h1>Heading Level 1</h1>'
            '<p>This is a paragraph.</p>'
            '<ul><li>List item 1</li><li>List item 2</li></ul>'
            '<pre>print(\'Code block\')</pre>'
            '<blockquote>This is a quote</blockquote>'
        )
        self.assertEqual(html_node.to_html(), expected_output)

if __name__ == "__main__":
    unittest.main()



class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_no_title(self):
        markdown = "## This is a subtitle\nNo title here"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found in the markdown.")
    
    def test_title_with_extra_whitespace(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_title_among_other_text(self):
        markdown = """
        Some text here
        
        # My Title
        
        More text here
        """
        self.assertEqual(extract_title(markdown), "My Title")

if __name__ == '__main__':
    unittest.main()



#Start tests

if __name__ == "__main__":
    unittest.main()



