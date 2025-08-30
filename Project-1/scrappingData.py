import requests
from bs4 import BeautifulSoup
import os

def extract_blog_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Blogspot posts often use <div class="post-body"> or similar
    content_div = soup.find('div', class_='post-body') or soup.find('div', class_='post-content')
    if not content_div:
        print("Could not find main content section.")
        return None

    # Remove unwanted tags like scripts, styles, etc.
    for tag in content_div(['script', 'style', 'aside']):
        tag.decompose()

    # Get clean text
    clean_text = content_div.get_text(separator='\n', strip=True)
    return clean_text

def save_to_file(text, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Content saved to: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

# Example usage
if __name__ == "__main__":
    blog_url = input("Enter Blogspot URL: ")
   # save_path = input("Enter full path to save .txt file (e.g., C:/Users/Rakesh/Documents/blog.txt): ")
    save_path=r"C:\Users\rakes\OneDrive\Desktop\scrap\blog.txt"

    content = extract_blog_content(blog_url)
    if content:
        save_to_file(content, save_path)