import customtkinter as ctk
from database import insert_book

class AddBookWindow(ctk.CTkToplevel):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent)
        self.title("Add Book")
        self.geometry("400x400")
        self.refresh_callback = refresh_callback  # store the callback

        # Fields for new book
        ctk.CTkLabel(self, text="Title").pack(pady=(10,0))
        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(pady=4)

        ctk.CTkLabel(self, text="Author").pack(pady=(10,0))
        self.author_entry = ctk.CTkEntry(self)
        self.author_entry.pack(pady=4)

        ctk.CTkLabel(self, text="Year").pack(pady=(10,0))
        self.year_entry = ctk.CTkEntry(self)
        self.year_entry.pack(pady=4)

        ctk.CTkLabel(self, text="Category").pack(pady=(10,0))
        self.category_entry = ctk.CTkEntry(self)
        self.category_entry.pack(pady=4)

        # Add button
        ctk.CTkButton(self, text="Add Book", command=self.add_book).pack(pady=20)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip() or None
        category = self.category_entry.get().strip() or None

        if not title or not author:
            ctk.CTkMessagebox.show_warning("Title and Author are required!")
            return

        # Call database insert (ensure insert_book() now accepts category instead of ISBN)
        insert_book(title, author, year, category)

        if self.refresh_callback:
            self.refresh_callback()  # call the refresh function in parent

        ctk.CTkMessagebox.show_info("Success", f"Book '{title}' added successfully!")
        self.destroy()
