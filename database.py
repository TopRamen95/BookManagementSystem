from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://qtdhfhxruxxxaxjutysf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF0ZGhmaHhydXh4eGF4anV0eXNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3NDIyMzcsImV4cCI6MjA3NTMxODIzN30.u_HJrUlE__wvI2VRJdxTxb68woZTt1FAoOykO3Tz8r0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------- Table Setup --------------------
def create_tables():
    # Books table
    supabase.rpc("sql", {"q": """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            year INTEGER,
            category TEXT,
            status TEXT DEFAULT 'Available',
            CONSTRAINT unique_book UNIQUE (title, author)
        );
    """}).execute()

    # Members table
    supabase.rpc("sql", {"q": """
        CREATE TABLE IF NOT EXISTS members (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """}).execute()

    # Admins table
    supabase.rpc("sql", {"q": """
        CREATE TABLE IF NOT EXISTS admins (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """}).execute()

    # Issued books table
    supabase.rpc("sql", {"q": """
        CREATE TABLE IF NOT EXISTS issued_books (
            id SERIAL PRIMARY KEY,
            book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
            member_id INTEGER REFERENCES members(id) ON DELETE CASCADE,
            issue_date DATE DEFAULT CURRENT_DATE,
            return_date DATE,
            status TEXT DEFAULT 'Issued' CHECK (status IN ('Issued', 'Returned', 'Reissued'))
        );
    """}).execute()


# -------------------- Admin Functions --------------------
def create_admin(name="admin1", password="admin123"):
    existing = supabase.table("admins").select("*").eq("name", name).execute().data
    if not existing:
        supabase.table("admins").insert({
            "name": name,
            "password": password
        }).execute()
        print(f"Admin '{name}' created!")
    else:
        print("Admin already exists.")


def view_admins():
    return supabase.table("admins").select("*").execute().data


def add_admin(name, password="admin123"):
    existing = supabase.table("admins").select("*").eq("name", name).execute().data
    if not existing:
        supabase.table("admins").insert({"name": name, "password": password}).execute()
        print(f"Admin '{name}' added!")
    else:
        print(f"Admin '{name}' already exists.")


def delete_admin(admin_id):
    supabase.table("admins").delete().eq("id", admin_id).execute()


def validate_admin_login(name, password):
    res = supabase.table("admins").select("*").eq("name", name).eq("password", password).execute().data
    return bool(res)


# -------------------- Book Functions --------------------
def insert_book(title, author, year=None, category=None):
    supabase.table("books").insert({
        "title": title,
        "author": author,
        "year": year,
        "category": category,
        "status": "Available"
    }).execute()


def update_book(book_id, title=None, author=None, year=None, category=None, status=None):
    update_data = {}
    if title is not None: update_data["title"] = title
    if author is not None: update_data["author"] = author
    if year is not None: update_data["year"] = year
    if category is not None: update_data["category"] = category
    if status is not None: update_data["status"] = status
    supabase.table("books").update(update_data).eq("id", book_id).execute()


def delete_book(book_id):
    supabase.table("books").delete().eq("id", book_id).execute()


def view_books():
    return supabase.table("books").select("*").execute().data


def search_books(query):
    query = query.lower()
    return [b for b in view_books() if query in (b.get("title","").lower() + " " + b.get("author","").lower())]


# -------------------- Member Functions --------------------
def add_member(name, email=None, phone=None, password="default123"):
    supabase.table("members").insert({
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }).execute()


def delete_member(member_id):
    supabase.table("members").delete().eq("id", member_id).execute()


def view_members():
    return supabase.table("members").select("*").execute().data


def validate_member_login(email, password):
    res = supabase.table("members").select("*").eq("email", email).eq("password", password).execute().data
    return bool(res)


# -------------------- Issue / Reissue / Return --------------------
def issue_book(member_id, book_id):
    book = supabase.table("books").select("*").eq("id", book_id).execute().data
    if not book: return "Book not found!"
    book = book[0]
    if book["status"] != "Available":
        return f"Book already {book['status']}!"
    supabase.table("issued_books").insert({"book_id": book_id, "member_id": member_id, "status": "Issued"}).execute()
    supabase.table("books").update({"status": "Issued"}).eq("id", book_id).execute()
    return "Book issued successfully!"


def reissue_book(member_id, book_id):
    issued = supabase.table("issued_books").select("*").eq("book_id", book_id).eq("member_id", member_id).execute().data
    if not issued: return "No record of this book issued to you!"
    supabase.table("issued_books").update({"status": "Reissued"}).eq("book_id", book_id).eq("member_id", member_id).execute()
    return "Book reissued successfully!"


def submit_book(member_id, book_id):
    issued = supabase.table("issued_books").select("*").eq("book_id", book_id).eq("member_id", member_id).execute().data
    if not issued: return "No record of this book issued to you!"
    supabase.table("issued_books").update({"status": "Returned"}).eq("book_id", book_id).eq("member_id", member_id).execute()
    supabase.table("books").update({"status": "Available"}).eq("id", book_id).execute()
    return "Book returned successfully!"


def view_issued_books(member_id):
    issued = supabase.table("issued_books").select("book_id, status, books(title, author)").eq("member_id", member_id).execute().data
    result = []
    for i in issued:
        book_info = i.get("books", {})
        result.append({
            "book_id": i.get("book_id"),
            "status": i.get("status"),
            "title": book_info.get("title",""),
            "author": book_info.get("author","")
        })
    return result


# -------------------- View all issued books for admin --------------------
def view_issued_books_all():
    """
    Returns all issued books with book title, member info, and status.
    """
    issued = supabase.table("issued_books").select(
        "id, book_id, member_id, issue_date, return_date, status, books(title, author), members(name, email)"
    ).execute().data

    # Flatten nested book and member info
    result = []
    for i in issued:
        book_info = i.get("books", {})
        member_info = i.get("members", {})
        result.append({
            "issued_id": i.get("id"),
            "book_id": i.get("book_id"),
            "title": book_info.get("title", ""),
            "author": book_info.get("author", ""),
            "member_id": i.get("member_id"),
            "member_name": member_info.get("name", ""),
            "member_email": member_info.get("email", ""),
            "status": i.get("status"),
            "issue_date": i.get("issue_date"),
            "return_date": i.get("return_date")
        })
    return result



# -------------------- DB Init / Reset --------------------
def init_db():
    create_tables()
    create_admin()
    print("Database initialized and default admin created.")


def reset_db():
    supabase.rpc("sql", {"q": "DROP TABLE IF EXISTS issued_books CASCADE;"}).execute()
    supabase.rpc("sql", {"q": "DROP TABLE IF EXISTS books CASCADE;"}).execute()
    supabase.rpc("sql", {"q": "DROP TABLE IF EXISTS members CASCADE;"}).execute()
    supabase.rpc("sql", {"q": "DROP TABLE IF EXISTS admins CASCADE;"}).execute()
    print("Database reset!")


if __name__ == "__main__":
    init_db()
