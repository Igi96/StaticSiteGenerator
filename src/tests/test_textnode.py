import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self): 
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is a text node", "bold", "url")     
        self.assertEqual(node, node2)

    def test_type(self): 
        node = TextNode("This is a text node", 2)
        node2 = TextNode("This is a text node", 2)     
        self.assertEqual(node, node2)    

if __name__ == "__main__": 
    unittest.main()


