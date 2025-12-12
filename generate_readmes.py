import os
import sys
import logging
from pathlib import Path

# --- CONFIGURATION ---
# Define the root path to start searching for image folders.
IMAGE_ROOT = '.'

# List of directory names to completely ignore and skip processing.
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

# --- LOGGING SETUP ---
def setup_logging():
    """Sets up basic logging to stdout (GitHub Actions default)"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stdout  # Ensure output goes to the action logs
    )
    # Log configuration details
    logging.info("--- Configuration Details ---")
    logging.info(f"IMAGE_ROOT: {IMAGE_ROOT}")
    logging.info(f"EXCLUDE_DIRS: {EXCLUDE_DIRS}")
    logging.info(f"IMAGE_EXTENSIONS: {IMAGE_EXTENSIONS}")
    logging.info(f"THUMBNAILS_PER_ROW: {THUMBNAILS_PER_ROW}")
    logging.info("-----------------------------\n")

# --- CORE FUNCTIONS ---

def generate_gallery_html(image_files):
    """Generates the HTML table code for a list of image files."""
    html_content = "<table>\n  <tr>\n"
    col_count = 0

    for image_file in image_files:
        # Create a link that wraps the image
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
    setup_logging()
    logging.info(f"Starting README generation from root: {IMAGE_ROOT}")

    for root, dirs, files in os.walk(IMAGE_ROOT):
        # Determine the name of the current directory (or 'Root' for '.')
        current_dir_name = os.path.basename(root) or 'Root'
        logging.debug(f"Scanning directory: {root}")

        # 1. Exclusion Logic: Skip unwanted directories
        if current_dir_name in EXCLUDE_DIRS:
            # Crucially, modify 'dirs' in place to prevent os.walk from descending
            dirs[:] = []
            logging.warning(f"-> EXCLUDED: Skipping directory and its contents: {root}")
            continue

        # 2. Identify Image Files
        image_files = sorted([
            f for f in files
            if Path(f).suffix.lower() in IMAGE_EXTENSIONS
        ])

        # 3. Process the Directory
        if image_files:
            num_images = len(image_files)
            readme_path = Path(root) / "README.md"

            logging.info(f"✅ FOUND: {num_images} images in {root}")
            logging.info(f"Images found: {', '.join(image_files[:5])}{'...' if num_images > 5 else ''}")

            # Generate the content
            gallery_html = generate_gallery_html(image_files)

            # Combine components for the full README content
            readme_title = f"# 🖼️ Image Gallery: {current_dir_name}\n\n"
            readme_content = readme_title + gallery_html

            # Write to README.md
            try:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
                logging.info(f"🎉 SUCCESS: Generated/updated {readme_path}")
            except Exception as e:
                logging.error(f"❌ ERROR: Failed to write {readme_path}. Error: {e}")

        else:
            # Log when a folder is scanned but contains no images
            logging.debug(f"No image files found in {root}. Skipping README generation.")

if __name__ == "__main__":
    main()
