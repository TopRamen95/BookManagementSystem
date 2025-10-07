import requests
import time
from supabase import create_client, Client

# 🔗 Supabase credentials
SUPABASE_URL = "https://qtdhfhxruxxxaxjutysf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0ZGhmaHhydXh4eGF4anV0eXNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3NDIyMzcsImV4cCI6MjA3NTMxODIzN30.u_HJrUlE__wvI2VRJdxTxb68woZTt1FAoOykO3Tz8r0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_books(subject="fiction", limit=100, offset=0):
    """Fetch books from Open Library by subject."""
    url = f"https://openlibrary.org/subjects/{subject}.json?limit={limit}&offset={offset}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"❌ Error fetching books for {subject}: {e}")
        return []

    books = []
    for b in data.get("works", []):
        books.append({
            "title": b.get("title"),
            "author": ", ".join([a["name"] for a in b.get("authors", [])]) if b.get("authors") else "Unknown",
            "year": b.get("first_publish_year"),
            "category": subject.capitalize(),  # Add category (e.g., Fiction, Science)
            "status": "Available"
        })
    return books


def insert_books_no_duplicates(books):
    """Insert books into Supabase while skipping duplicates."""
    try:
        existing_books = supabase.table("books").select("title, author").execute().data
        existing_set = set((b["title"], b["author"]) for b in existing_books)
    except Exception as e:
        print(f"❌ Error fetching existing books: {e}")
        return

    to_insert = []
    for book in books:
        key = (book["title"], book["author"])
        if key not in existing_set:
            to_insert.append(book)
            existing_set.add(key)

    if to_insert:
        try:
            supabase.table("books").insert(to_insert).execute()
            print(f"✅ Inserted {len(to_insert)} new books.")
        except Exception as e:
            print(f"❌ Error inserting books: {e}")
    else:
        print("⚠️ No new books to insert (all duplicates).")


if __name__ == "__main__":
    subjects = [
        "fiction", "science", "technology", "history", "mystery",
        "romance", "fantasy", "art", "philosophy", "biography",
        "mathematics", "engineering", "psychology", "computer_science",
        "children", "medical", "travel", "education", "music"
    ]

    for subject in subjects:
        print(f"\n📚 Fetching books for subject: {subject}")
        offset = 0

        while True:
            print(f"   ➤ Fetching batch: {offset + 1} to {offset + 100}")
            books = fetch_books(subject=subject, limit=100, offset=offset)
            if not books:
                print(f"✅ No more books for {subject}. Moving to next subject.")
                break

            insert_books_no_duplicates(books)
            offset += 100
            time.sleep(5)  # avoid API rate limits

    print("\n🎉 All subjects processed! Database fully populated.")
