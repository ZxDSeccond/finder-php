import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import os # Import modul os untuk fungsi clear screen

# --- ASCII Art Logo ZXD ---
# Perbaikan: Menghindari escape sequence yang tidak valid dengan raw string (r"")
ZXD_LOGO = r"""
  _____ _____ _____
 |  __ \_   _/ ____|
 | |__) || || (___
 |  ___/ | | \___ \
 | |    _| | ____) |
 |_|   |_____|_____/
       _
      | |__   ___  ___
      | '_ \ / _ \/ __|
      | | | | (_) \__ \
      |_| |_|\___/|___/
"""

# Fungsi untuk mengosongkan layar terminal
def clear_screen():
    # Perintah 'cls' untuk Windows, 'clear' untuk Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

def print_loading_logo():
    clear_screen() # Kosongkan layar sebelum menampilkan logo
    print(ZXD_LOGO)
    print("Starting URL Scanner...")
    time.sleep(1) # Wait a bit after showing the logo

def find_id_parameters(base_url):
    found_urls = []
    # Added User-Agent header to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with href attribute
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Check if the URL contains 'id=', 'page=', or 'product.php?id=' (case-insensitive)
            if 'id=' in full_url.lower() or 'page=' in full_url.lower() or 'product.php?id=' in full_url.lower():
                found_urls.append(full_url)
                print(f"Found: {full_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {base_url}: {e}")
        # Hint for 403 error
        if "403 Client Error: Forbidden" in str(e):
            print("Tip: This often means the website is blocking automated access. Try a different URL or check website's robots.txt.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return found_urls

# --- Main execution ---
if __name__ == "__main__":
    print_loading_logo() # Call this first to clear screen and show logo
    target_url = input("Enter the target website URL (e.g., https://example.com): ")
    print(f"\nScanning {target_url}...")
    results = find_id_parameters(target_url)

    if results:
        print("\n--- URLs with 'id', 'page', or 'product.php?id' parameters Found ---")
        for url in results:
            print(url)
    else:
        print("\nNo URLs with 'id', 'page', or 'product.php?id' parameters found on this page.")
