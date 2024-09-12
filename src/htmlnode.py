class HTMLNode:
	def __init__(self, tag = None, value = None , children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def __repr__(self):
		return (f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
                f"children={self.children!r}, props={self.props!r})")

	def to_html(self):
		raise NotImplementedError
	
	def props_to_html(self):
		if self.props == None:
			return ""
		
		final = ""
		for key,values in self.props.items():
			final += f'{key}="{values}" '


		return f" {final.strip()}" if final else ""
	

class LeafNode(HTMLNode):
	def __init__(self, value, tag = None, props = None):
		super().__init__(tag = tag, value = value, props=props)


	def to_html(self):
		if not self.value:
			raise ValueError
		
		if not self.tag:
			return self.value
		
		
		props_str = self.props_to_html()
		return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
	

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None, is_root=False):
        if children is None:
            raise ValueError("ParentNode must have children")
        self.is_root = is_root  # Add a flag to determine if it's a root node
        super().__init__(children=children, tag=tag, props=props)

    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode must have children")

        # If this ParentNode is the root node (is_root=True), it doesn't need a tag
        if self.is_root and self.tag is None:
            children_html = "".join(
                child.to_html() if isinstance(child, HTMLNode) else str(child)
                for child in self.children
            )
            return children_html

        # If it's a non-root ParentNode, it must have a tag
        if not self.is_root and not self.tag:
            raise ValueError("ParentNode must have a tag")

        # Concatenate the HTML for all child nodes
        children_html = "".join(
            child.to_html() if isinstance(child, HTMLNode) else str(child)
            for child in self.children
        )

        # Return the parent tag with its children rendered inside
        props_str = (
            " ".join(f'{key}="{value}"' for key, value in self.props.items())
            if self.props
            else ""
        )
        return f"<{self.tag}{(' ' + props_str) if props_str else ''}>{children_html}</{self.tag}>"
