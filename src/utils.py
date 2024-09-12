import re
from textnode import TextNode
from htmlnode import LeafNode, ParentNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Takes a list of old nodes, a delimiter, and a text type.
    Splits "text" type nodes based on the delimiter and returns a new list of nodes.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != "text":
            # If the node is not a "text" node, add it as is
            new_nodes.append(node)
            continue

        if not node.text:  # Handles empty text nodes
            new_nodes.append(TextNode("", node.text_type))
            continue

        # Use a regular expression to split the text based on the delimiter
        parts = re.split(f'({re.escape(delimiter)}.*?{re.escape(delimiter)})', node.text)

        for part in parts:
            if part.startswith(delimiter) and part.endswith(delimiter):
                # This part is between the delimiters, so it should be of type `text_type`
                stripped_part = part[len(delimiter):-len(delimiter)]  # Remove the delimiters
                new_nodes.append(TextNode(stripped_part, text_type))
            else:
                # This part is outside the delimiters, so it remains "text"
                if part:  # Ignore empty strings
                    new_nodes.append(TextNode(part, node.text_type))

    return new_nodes

def extract_markdown_images(text):
    """
    Extracts markdown image syntax from a string and returns a list of tuples.
    Each tuple contains the alt_text and the URL.
    """
    # Regular expression to match ![alt_text](url)
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown link syntax from a string and returns a list of tuples.
    Each tuple contains the link_text and the URL.
    """
    # Regular expression to match [link_text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)
    
    return matches



def split_nodes_link(old_nodes):
    """
    Splits nodes containing Markdown links into individual nodes.
    Example: [text](url)
    """
    new_nodes = []
    
    # Regex pattern for Markdown links [text](url)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # Find all matches for the link pattern
        start = 0
        for match in re.finditer(link_pattern, node.text):
            link_text, link_url = match.groups()
            link_start, link_end = match.span()

            # Add the text before the link (if any)
            if start < link_start:
                new_nodes.append(TextNode(node.text[start:link_start], text_type_text))

            # Add the link as a separate node
            new_nodes.append(TextNode(link_text, text_type_link, link_url))
            start = link_end

        # Add any remaining text after the last link
        if start < len(node.text):
            new_nodes.append(TextNode(node.text[start:], text_type_text))

    return new_nodes


def split_nodes_image(old_nodes):
    """
    Splits nodes containing Markdown images into individual nodes.
    Example: ![alt_text](url)
    """
    new_nodes = []
    
    # Regex pattern for Markdown images ![alt_text](url)
    image_pattern = r'!\[([^\]]+)\]\(([^)]+)\)'

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # Find all matches for the image pattern
        start = 0
        for match in re.finditer(image_pattern, node.text):
            alt_text, image_url = match.groups()
            image_start, image_end = match.span()

            # Add the text before the image (if any)
            if start < image_start:
                new_nodes.append(TextNode(node.text[start:image_start], text_type_text))

            # Add the image as a separate node
            new_nodes.append(TextNode(alt_text, text_type_image, image_url))
            start = image_end

        # Add any remaining text after the last image
        if start < len(node.text):
            new_nodes.append(TextNode(node.text[start:], text_type_text))

    return new_nodes



def text_to_textnodes(text):
    """
    Converts a text containing Markdown-like syntax into a list of TextNode objects.
    """
    # Step 1: Initialize the text nodes list
    text_nodes = [TextNode(text, text_type_text)]
    
    # Step 2: Handle Images first (since they are special cases of links)
    text_nodes = split_nodes_image(text_nodes)

    # Step 3: Handle Links
    text_nodes = split_nodes_link(text_nodes)

    # Step 4: Handle Bold, Italic, and Code
    text_nodes = split_nodes_delimiter(text_nodes, "**", text_type_bold)  # Handle Bold
    text_nodes = split_nodes_delimiter(text_nodes, "*", text_type_italic)  # Handle Italic
    text_nodes = split_nodes_delimiter(text_nodes, "`", text_type_code)  # Handle Code

    return text_nodes



def markdown_to_blocks(markdown):
    """
    Converts a Markdown string into a list of blocks.
    
    Each block can be a heading, a paragraph, or a list block.
    Leading/trailing whitespace is removed, and empty blocks are filtered out.
    """
    # Step 1: Split the Markdown into blocks based on two or more newlines
    blocks = re.split(r'\n\s*\n', markdown.strip())


    # Step 2: Normalize each block by removing excessive spaces, but preserving newlines inside lists
    def normalize_block(block):
        lines = block.splitlines()
        normalized_lines = [re.sub(r'[ \t]+', ' ', line.strip()) for line in lines if line.strip()]
        return "\n".join(normalized_lines)
    
    # Step 3: Normalize each block and ensure separation
    blocks = [normalize_block(block) for block in blocks]


    # Step 4: Filter out empty blocks (in case of excessive newlines)
    blocks = [block for block in blocks if block]

    
    return blocks



def block_to_block_type(block):
    """
    Determines the type of a given block of Markdown text.
    """
    # Handle empty blocks (return 'paragraph' if the block is empty)
    if not block.strip():
        return 'paragraph'
    
    # Check for heading (1-6 # followed by a space)
    if re.match(r'^#{1,6} ', block):
        return 'heading'
    
    # Check for code block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```'):
        return 'code block'
    
    # Check for quote block (every line starts with >)
    if all(line.startswith('> ') for line in block.splitlines()):
        return 'quote block'
    
    # Check for unordered list (every line starts with * or - followed by a space)
    if all(re.match(r'^(\*|\-) ', line) for line in block.splitlines()):
        return 'unordered list'
    
    # Check for ordered list (each line starts with 1. 2. 3. etc.)
    lines = block.splitlines()
    if all(re.match(r'^\d+\. ', line) for line in lines):
        # Check if the numbers increment correctly
        for i, line in enumerate(lines):
            number = int(line.split('.')[0])
            if number != i + 1:
                return 'paragraph'  # If numbers are not sequential, it's a paragraph
        return 'ordered list'
    
    # If none of the above, it's a paragraph
    return 'paragraph'



def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single HTMLNode containing many child HTMLNodes.
    """
    # Create a root ParentNode that will hold all child nodes (no tag needed)
    root = ParentNode(children=[], is_root=True)

    # Step 1: Split the Markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Step 2: Iterate through each block, determine its type, and convert to HTMLNode
    for block in blocks:
        block_type = block_to_block_type(block)

        # Step 3: Convert each block based on its type
        if block_type == 'heading':
            heading_level = len(block.split()[0])  # Number of # symbols
            heading_text = block[heading_level + 1:].strip()  # The actual heading text
            heading_text = parse_inline_markdown(heading_text)  # Handle inline elements
            node = LeafNode(value=heading_text, tag=f"h{heading_level}")
        
        elif block_type == 'paragraph':
            block = parse_inline_markdown(block)  # Handle inline elements for paragraphs
            node = LeafNode(value=block, tag="p")
        
        elif block_type == 'code block':
            code_content = block.strip("```").strip()  # Remove the backticks
            node = LeafNode(value=code_content, tag="pre")  # Use <pre> for code blocks
        
        elif block_type == 'quote block':
            quote_content = "\n".join(line[2:] for line in block.splitlines())  # Remove the '> ' from each line
            node = LeafNode(value=quote_content, tag="blockquote")
        
        elif block_type == 'unordered list':
            list_items = [LeafNode(value=parse_inline_markdown(item[2:]), tag="li") for item in block.splitlines()]
            node = ParentNode(children=list_items, tag="ul")  # Use <ul> for unordered lists
        
        elif block_type == 'ordered list':
            list_items = [LeafNode(value=parse_inline_markdown(item.split(". ", 1)[1]), tag="li") for item in block.splitlines()]
            node = ParentNode(children=list_items, tag="ol")  # Use <ol> for ordered lists
        
        else:
            # Fallback to a paragraph if the block type is unknown
            block = parse_inline_markdown(block)  # Handle inline elements
            node = LeafNode(value=block, tag="p")
        
        # Step 4: Add the node to the root ParentNode
        root.children.append(node)
    
    return root

def parse_inline_markdown(text):
    """
    Parse inline markdown elements like bold, italic, code, and links and convert them to HTML.
    """

    # Handle bold (**bold** -> <strong>bold</strong>)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Handle italic (*italic* -> <em>italic</em>)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

    # Handle inline code (`code` -> <code>code</code>)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    # Handle links ([text](url) -> <a href="url">text</a>)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    return text


def extract_title(markdown):
    """
    Extracts the H1 header from the markdown text.
    
    Args:
        markdown (str): The markdown content as a string.
    
    Returns:
        str: The extracted H1 header text.
    
    Raises:
        Exception: If no H1 header is found in the markdown.
    """
    lines = markdown.splitlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    
    # If no H1 header is found, raise a generic Exception
    raise Exception("No H1 header found in the markdown.")


