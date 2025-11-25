import os
from pathlib import Path

# --- CONFIGURATION ---
# Define the root path to start searching for image folders.
# Use '.' to start from the root of the repository.
IMAGE_ROOT = '.' 

# List of directory names to completely ignore and skip processing.
# Add your document, config, or non-image folders here.
EXCLUDE_DIRS = [
    '.git',
    '.github',
    '__pycache__',
    'docs',     
    'config',  
    # Add any other folders you want to skip
]

# Supported image file extensions
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.webp']

# Number of thumbnails per row in the Markdown table
THUMBNAILS_PER_ROW = 4
# --- END CONFIGURATION ---


def generate_gallery_html(image_files):
    """Generates the HTML table code for a list of image files."""
    html_content = "<table>\n  <tr>\n"
    col_count = 0
    
    for image_file in image_files:
        # Create a link that wraps the image
        # width="200" sets the thumbnail size
        image_tag = (
            f'<a href="{image_file}">'
            f'<img src="{image_file}" width="150" height="150" '
            f'alt="{image_file}" style="object-fit: cover; margin: 5px;">'
            f'</a>'
        )
        
        # Add the table cell
        html_content += f'    <td align="center" style="border: none;">{image_tag}</td>\n'
        col_count += 1
        
        # Start a new row every THUMBNAILS_PER_ROW images
        if col_count % THUMBNAILS_PER_ROW == 0:
            html_content += "  </tr>\n  <tr>\n"

    # Fill remaining cells in the last row if needed
    while col_count % THUMBNAILS_PER_ROW != 0:
        html_content += '    <td style="border: none;"></td>\n'
        col_count += 1

    html_content += "  </tr>\n</table>\n"
    return html_content

def main():
    """Recursively walks directories and generates/updates README.md files."""
    print(f"Starting README generation from root: {IMAGE_ROOT}")
    
    for root, dirs, files in os.walk(IMAGE_ROOT):
        # 1. Exclusion Logic: Skip unwanted directories
        current_dir_name = os.path.basename(root)
        if current_dir_name in EXCLUDE_DIRS:
            # Crucially, modify 'dirs' in place to prevent os.walk from descending
            dirs[:] = [] 
            print(f"-> Skipping excluded directory: {root}")
            continue

        # 2. Identify Image Files
        # Filter files for supported image extensions
        image_files = sorted([
            f for f in files 
            if Path(f).suffix.lower() in IMAGE_EXTENSIONS
        ])
        
        # 3. Process the Directory
        if image_files:
            print(f"-> Processing directory: {root} ({len(image_files)} images found)")
            
            # Generate the content
            gallery_html = generate_gallery_html(image_files)
            
            # Combine components for the full README content
            readme_title = f"# 🖼️ Image Gallery: {current_dir_name or 'Root'}\n\n"
            readme_content = readme_title + gallery_html
            
            # Write to README.md
            readme_path = Path(root) / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
                
        # Optional: Skip subdirectories if the parent folder has images 
        # (Uncomment this if you only want a README at the top level of image groups)
        # if image_files:
        #     dirs[:] = [] 
            
if __name__ == "__main__":
    main()