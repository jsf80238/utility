import urllib.parse
import requests


def search_open_library_for_book(query):
    """Searches Open Library to resolve standard metadata and precise book title."""
    print(f"Searching Open Library for: '{query}'...")
    url = f"https://openlibrary.org/search.json?q={urllib.parse.quote(query)}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("numFound", 0) == 0:
            print("No books found on Open Library matching that query.")
            return None

        book = data["docs"][0]
        title = book.get("title", "Unknown Title")
        isbn = book.get("isbn", [None])[0]

        return {"title": title, "isbn": isbn}

    except Exception as e:
        print(f"Error querying Open Library API: {e}")
        return None


def generate_dpl_clean_book_link(book_identifiers):
    """Generates an error-free, filtered live link targeting strictly exact

    matches and print-only book media.
    """
    if not book_identifiers:
        return

    base_url = "https://catalog.denverlibrary.org/search/searchresults.aspx"

    # Base operational contexts required by DPL's Polaris system
    params = {
        "ctx": "1.1033.0.0.6",
        "type": "Keyword",
        "sort": "RELEVANCE",
        "page": "0",
        "limit": "TOM=b",  # Restricts material strictly to physical books
        "query": "",  # Leaves backend filtering to clear standard url encoding
    }

    # Wrap the search string inside literal double quotes to enforce exact matching
    # without breaking the SQL query layer on the backend.
    if book_identifiers["isbn"]:
        params["term"] = f'"{book_identifiers["isbn"]}"'
        params["by"] = "IS"  # ISBN search index
    else:
        params["term"] = f'"{book_identifiers["title"]}"'
        params["by"] = "TI"  # Title search index

    # Build the cleanly encoded query string
    clean_dpl_url = f"{base_url}?{urllib.parse.urlencode(params)}"

    print("\n" + "=" * 60)
    print("CLEAN PRINT-ONLY DPL CATALOG LINK")
    print("=" * 60)
    print(f"Target Title: {book_identifiers['title']}")
    print(f"\nFiltered Direct Link:\n{clean_dpl_url}")
    print("=" * 60)


if __name__ == "__main__":
    book_query = "The Great Gatsby"

    identifiers = search_open_library_for_book(book_query)
    if identifiers:
        generate_dpl_clean_book_link(identifiers)