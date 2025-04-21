"""
Example of using the trafilatura web scraper to extract text content from websites.
This example demonstrates getting the main text content from a URL.
"""

import trafilatura
import argparse
from utils.url_bypass import bypass_url_shortener


def get_website_text_content(url):
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    """
    # Check if the URL is a shortener and bypass it
    bypassed_url = bypass_url_shortener(url)
    print(f"Processing URL: {bypassed_url}")
    
    # Send a request to the website
    downloaded = trafilatura.fetch_url(bypassed_url)
    
    if downloaded:
        # Extract the main text content
        text = trafilatura.extract(downloaded)
        return text
    else:
        return "Failed to download the content from the website."


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract text content from a website.')
    parser.add_argument('url', help='URL of the website to scrape')
    args = parser.parse_args()
    
    # Get the text content
    content = get_website_text_content(args.url)
    
    # Print the first 500 characters of the content
    print("\n----- Website Content Preview -----")
    print(f"{content[:500]}...")
    print("----- End of Preview -----\n")
    
    # Ask if the user wants to see the full content
    show_full = input("Do you want to see the full content? (y/n): ")
    if show_full.lower() == 'y':
        print("\n----- Full Website Content -----")
        print(content)
        print("----- End of Content -----")


if __name__ == "__main__":
    main()