import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test with no props
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

        # Test with single prop
        node = HTMLNode(tag="a", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

        # Test with multiple props
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"class": "text"})
        expected_repr = "HTMLNode(tag='p', value='Hello', children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)

    def test_children_handling(self):
        child_node = HTMLNode(tag="span", value="Child")
        parent_node = HTMLNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.children[0], child_node)


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_without_props(self):
        # Test with a tag but no props
        node = LeafNode(value="This is bold", tag="b")
        expected_html = "<b>This is bold</b>"
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_node_with_one_prop(self):
        # Test with a tag and one property (e.g., an anchor tag with an href)
        node = LeafNode(value="Click here", tag="a", props={"href": "https://example.com"})
        expected_html = '<a href="https://example.com">Click here</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_node_without_tag(self):
        # Test with no tag (just raw text)
        node = LeafNode(value="Just some text")
        expected_html = "Just some text"
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_node_with_empty_value(self):
        # Test for raising a ValueError when value is None or empty
        with self.assertRaises(ValueError):
            LeafNode(value="").to_html()

    def test_leaf_node_with_tag_and_empty_props(self):
        # Test with a tag but an empty props dictionary
        node = LeafNode(value="Paragraph text", tag="p", props={})
        expected_html = "<p>Paragraph text</p>"
        self.assertEqual(node.to_html(), expected_html)





class TestParentNode(unittest.TestCase):

    def test_parent_node_with_children(self):
        """Test a ParentNode with multiple children"""
        parent = ParentNode(
            children=[
                LeafNode(tag='p', value="This is a paragraph."),
                LeafNode(tag='span', value="This is a span.")
            ],
            tag='div'
        )
        expected_html = '<div><p>This is a paragraph.</p><span>This is a span.</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_plain_text(self):
        """Test a ParentNode with plain text as a child"""
        parent = ParentNode(
            children=[
                "Some plain text.",
                LeafNode(tag='span', value="This is a span.")
            ],
            tag='div'
        )
        expected_html = '<div>Some plain text.<span>This is a span.</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_empty_children(self):
        """Test that a ParentNode without children raises an error"""
        with self.assertRaises(ValueError):
            ParentNode(children=None, tag='div')

    def test_parent_node_without_tag(self):
        """Test that a non-root ParentNode without a tag raises an error when rendering."""
        # Create a non-root ParentNode without a tag (which should raise an error)
        parent_node = ParentNode(children=[LeafNode(value="Some text", tag="p")], is_root=False)

        # Ensure it raises a ValueError when rendering
        with self.assertRaises(ValueError):
            parent_node.to_html()



    def test_parent_node_with_props(self):
        """Test a ParentNode with HTML attributes (props)"""
        parent = ParentNode(
            children=[
                LeafNode(tag='p', value="This is a paragraph.")
            ],
            tag='div',
            props={'class': 'container', 'id': 'main-div'}
        )
        expected_html = '<div class="container" id="main-div"><p>This is a paragraph.</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_mixed_children(self):
        """Test a ParentNode with a mix of HTMLNode children and plain text"""
        parent = ParentNode(
            children=[
                "Some plain text.",
                LeafNode(tag='p', value="A paragraph."),
                "More plain text.",
                LeafNode(tag='span', value="A span.")
            ],
            tag='div'
        )
        expected_html = '<div>Some plain text.<p>A paragraph.</p>More plain text.<span>A span.</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_with_empty_props(self):
        """Test a ParentNode with empty props"""
        parent = ParentNode(
            children=[
                LeafNode(tag='p', value="This is a paragraph.")
            ],
            tag='div',
            props={}
        )
        expected_html = '<div><p>This is a paragraph.</p></div>'
        self.assertEqual(parent.to_html(), expected_html)


if __name__ == "__main__": 
    unittest.main()