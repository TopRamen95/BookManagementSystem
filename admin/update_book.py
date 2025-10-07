import customtkinter as ctk
from database import update_book, view_books

class UpdateBookWindow(ctk.CTkToplevel):
    def __init__(self, parent, book_id, refresh_callback=None):
        super().__init__(parent)
        self.title("Update Book")
        self.geometry("400x400")
        self.book_id = book_id
        self.refresh_callback = refresh_callback

        # Fetch current book details
        book = next((b for b in view_books() if b["id"] == book_id), None)
        if not book:
            ctk.CTkMessagebox.show_error("Error", "Book not found!")
            self.destroy()
            return

        # Fields
        ctk.CTkLabel(self, text="Title").pack(pady=(10,0))
        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(pady=4)
        self.title_entry.insert(0, book["title"])

        ctk.CTkLabel(self, text="Author").pack(pady=(10,0))
        self.author_entry = ctk.CTkEntry(self)
        self.author_entry.pack(pady=4)
        self.author_entry.insert(0, book.get("author", ""))

        ctk.CTkLabel(self, text="Year").pack(pady=(10,0))
        self.year_entry = ctk.CTkEntry(self)
        self.year_entry.pack(pady=4)
        self.year_entry.insert(0, book.get("year",""))

        ctk.CTkLabel(self, text="Category").pack(pady=(10,0))
        self.category_entry = ctk.CTkEntry(self)
        self.category_entry.pack(pady=4)
        self.category_entry.insert(0, book.get("category",""))

        ctk.CTkLabel(self, text="Status").pack(pady=(10,0))
        self.status_var = ctk.StringVar(value=book.get("status","Available"))
        ctk.CTkOptionMenu(self, variable=self.status_var, values=["Available","Issued"]).pack(pady=4)

        # Update button
        ctk.CTkButton(self, text="Update Book", command=self.update_book).pack(pady=20)

    def update_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip() or None
        category = self.category_entry.get().strip() or None
        status = self.status_var.get()

        if not title or not author:
            ctk.CTkMessagebox.show_warning("Title and Author are required!")
            return

        # Call database update (ensure update_book() now accepts category instead of ISBN)
        update_book(self.book_id, title, author, year, category, status)

        if self.refresh_callback:
            self.refresh_callback()  # refresh parent

        ctk.CTkMessagebox.show_info("Success", f"Book '{title}' updated successfully!")
        self.destroy()
