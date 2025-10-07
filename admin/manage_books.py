import customtkinter as ctk
from admin.add_book import AddBookWindow
from admin.update_book import UpdateBookWindow
from database import view_books, delete_book, search_books

class BooksWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Books")
        self.geometry("750x500")
        self.parent = parent

        ctk.set_appearance_mode("Light")

        # Search bar
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(self, placeholder_text="Search Books...", textvariable=self.search_var).pack(pady=6)
        ctk.CTkButton(self, text="Search", command=self.search_books).pack(pady=4)

        # Scrollable frame for books
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=700, height=300)
        self.scroll_frame.pack(pady=12)
        self.book_buttons = []
        self.selected_book_id = None

        # Action buttons
        ctk.CTkButton(self, text="Add Book", command=self.add_book).pack(pady=6)
        ctk.CTkButton(self, text="Update Selected Book", command=self.update_book).pack(pady=6)
        ctk.CTkButton(self, text="Delete Selected Book", command=self.delete_selected_book).pack(pady=6)

        self.load_books()

    def load_books(self, books=None):
        # Clear existing buttons
        for b in self.book_buttons:
            b.destroy()
        self.book_buttons.clear()
        self.selected_book_id = None

        if books is None:
            books = view_books()

        for b in books:
            status = b.get("status", "Available")
            color = "green" if status == "Available" else "red"
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"{b['id']} | {b['title']} - {b.get('author', 'Unknown')} | Category: {b.get('category','N/A')} | Status: {status}",
                fg_color=color,
                command=lambda book_id=b['id'], button=None: self.select_book(book_id, button),
                anchor="w"
            )
            btn.pack(pady=2, fill="x")
            # Attach button reference to lambda
            btn.configure(command=lambda book_id=b['id'], btn=btn: self.select_book(book_id, btn))
            self.book_buttons.append(btn)

    def select_book(self, book_id, btn):
        # Deselect previous
        for b in self.book_buttons:
            status = "green" if "Available" in b.cget("text") else "red"
            b.configure(fg_color=status)

        # Select current
        btn.configure(fg_color="blue")
        self.selected_book_id = book_id

    def search_books(self):
        query = self.search_var.get().strip()
        if query:
            results = search_books(query)  # Ensure this searches in title, author, and category
            self.load_books(results)
        else:
            self.load_books()

    def add_book(self):
        AddBookWindow(self, self.load_books)

    def update_book(self):
        if self.selected_book_id is None:
            ctk.CTkMessagebox.show_warning("Please select a book to update!")
        else:
            UpdateBookWindow(self, self.selected_book_id, self.load_books)

    def delete_selected_book(self):
        if self.selected_book_id is None:
            ctk.CTkMessagebox.show_warning("Please select a book to delete!")
        else:
            delete_book(self.selected_book_id)
            self.load_books()
