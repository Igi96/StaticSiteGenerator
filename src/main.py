# main.py
import os
from copy_static import clear_and_copy
from utils import extract_title, markdown_to_html_node



def generate_page(from_path, template_path, dest_path):
    """
    Generates an HTML page from a markdown file using a template.
    
    Args:
        from_path (str): Path to the markdown file.
        template_path (str): Path to the HTML template.
        dest_path (str): Path where the generated HTML file will be written.
    """
    print(f"Markdown file: {from_path}")
    print(f"Template file: {template_path}")
    print(f"Generating HTML at: {dest_path}")

    # Basic error handling for reading files
    try:
        with open(from_path, 'r') as md_file:
            markdown_content = md_file.read()
    except FileNotFoundError:
        print(f"Error: Markdown file {from_path} not found.")
        return

    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        print(f"Error: Template file {template_path} not found.")
        return

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()




    # Extract title
    try:
        title = extract_title(markdown_content)
    except Exception as e:
        print(f"Error extracting title: {e}")
        title = "Untitled"

    # Replace placeholders
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML to dest_path
    with open(dest_path, 'w') as output_file:
        output_file.write(final_html)

    print(f"Page generated successfully at {dest_path}")



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages from markdown files in the content directory.
    
    Args:
        dir_path_content (str): The root path to the content directory.
        template_path (str): The path to the HTML template file.
        dest_dir_path (str): The root path where the generated HTML files will be written.
    """
    # Walk through the content directory recursively
    for root, dirs, files in os.walk(dir_path_content):
        print(f"Exploring directory: {root}")  # Add this to see which directory you're in

        for file in files:
            if file.endswith(".md"):  # Only process markdown files
                # Build full path for the markdown file
                markdown_file_path = os.path.join(root, file)
                
                print(f"Processing markdown file: {markdown_file_path}")  # Add this to check the files being processed
                

                # Construct the corresponding output path in the destination directory
                relative_path = os.path.relpath(markdown_file_path, dir_path_content)  # Get relative path from content root
                output_file_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")
                
                print(f"Output HTML file will be: {output_file_path}")  # Check the output path
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # Call the generate_page function to generate the HTML for this markdown file
                generate_page(markdown_file_path, template_path, output_file_path)
                
                print(f"Generated page from {markdown_file_path} -> {output_file_path}")




def main():

    # Change the working directory to the project root
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Define the source and destination directories
    src_dir = "static"  # Your static source files should be here
    dest_dir = "public"  # Your generated public files go here
    content_file = "content" # The markdown file
    template_file = "static/template.html"  # The HTML template
    output_file = "public" # The generated HTML folder

    
    # content_file = "content/index.md" Just for one file
    # template_file = "static/template.html" 
    # output_file = "public/index.html"  Just for one file



    # Call the function to clear and copy static files to the public directory
    clear_and_copy(src_dir, dest_dir)

    # Generate the page
    generate_pages_recursive(content_file, template_file, output_file)



if __name__ == "__main__":
    main()
