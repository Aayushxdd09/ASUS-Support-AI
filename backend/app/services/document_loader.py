
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Sources file location
SOURCES_FILE = PROJECT_ROOT / "data" / "raw" / "sources.txt"

# Folder where extracted documents will be saved
DOCUMENTS_FOLDER = PROJECT_ROOT / "data" / "processed"


def load_documents():
    # Create processed folder if it doesn't exist
    DOCUMENTS_FOLDER.mkdir(parents=True, exist_ok=True)

    # Read URLs from sources.txt
    with open(SOURCES_FILE, "r", encoding="utf-8") as file:
        urls = [
            line.strip()
            for line in file
            if line.strip()
        ]

    for index, url in enumerate(urls, start=1):
        try:
            print(f"Downloading: {url}")

            response = requests.get(
                url,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Remove unnecessary elements
            for element in soup(
                ["script", "style", "nav", "footer", "header"]
            ):
                element.decompose()

            # Extract readable text
            text = soup.get_text(
                separator="\n",
                strip=True
            )

            # Save extracted content
            output_file = (
                DOCUMENTS_FOLDER / f"document_{index}.txt"
            )

            output_file.write_text(
                text,
                encoding="utf-8"
            )

            print(f"Saved: {output_file.name}")

        except requests.RequestException as error:
            print(f"Failed to download {url}: {error}")


if __name__ == "__main__":
    load_documents()
