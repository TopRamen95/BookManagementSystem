import customtkinter as ctk
from member.member_login import MemberLogin
from database import view_books, issue_book, view_issued_books, reissue_book, submit_book
import tkinter.messagebox as messagebox

class MemberDashboard(ctk.CTk):
    def __init__(self, member_id):
        super().__init__()
        self.member_id = member_id
        self.title(f"Member Dashboard - ID {member_id}")
        self.geometry("800x600")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Header
        ctk.CTkLabel(self, text=f"Welcome, Member ID {member_id}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=12)

        # Logout button
        ctk.CTkButton(self, text="Logout", fg_color="red", command=self.logout).pack(pady=6)

        # View issued books
        ctk.CTkButton(self, text="View Issued Books", command=self.open_issued_books).pack(pady=6)

        # Scrollable frame for books
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=750, height=350)
        self.scroll_frame.pack(pady=12)
        self.book_buttons = []
        self.selected_book_id = None

        # Action button
        ctk.CTkButton(self, text="Issue Selected Book", command=self.issue_selected_book).pack(pady=6)

        self.load_books()
        self.mainloop()

    def load_books(self, books=None):
        for btn in self.book_buttons:
            btn.destroy()
        self.book_buttons.clear()
        self.selected_book_id = None

        if books is None:
            books = view_books()

        for book in books:
            status = book.get("status", "Available")
            color = "green" if status == "Available" else "red"
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"{book['id']} | {book['title']} - {book['author']} | Category: {book.get('category','')} | Status: {status}",
                fg_color=color,
                anchor="w"
            )
            btn.configure(command=lambda b_id=book['id'], b_btn=btn: self.select_book(b_id, b_btn))
            btn.pack(pady=2, fill="x")
            self.book_buttons.append(btn)

    def select_book(self, book_id, btn):
        for b in self.book_buttons:
            status = "green" if "Available" in b.cget("text") else "red"
            b.configure(fg_color=status)
        btn.configure(fg_color="blue")
        self.selected_book_id = book_id

    def issue_selected_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Warning", "Please select a book to issue!")
            return
        result = issue_book(self.member_id, self.selected_book_id)
        messagebox.showinfo("Info", result)
        self.load_books()

    def open_issued_books(self):
        IssuedBooksWindow(self.member_id)

    def logout(self):
        self.destroy()
        MemberLogin()


class IssuedBooksWindow(ctk.CTkToplevel):
    def __init__(self, member_id):
        super().__init__()
        self.member_id = member_id
        self.title("Issued Books")
        self.geometry("700x400")

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=650, height=300)
        self.scroll_frame.pack(pady=12)
        self.book_buttons = []
        self.selected_book_id = None

        # Action buttons
        ctk.CTkButton(self, text="Reissue Selected Book", command=self.reissue_selected_book).pack(pady=6)
        ctk.CTkButton(self, text="Return Selected Book", command=self.return_selected_book).pack(pady=6)

        self.load_issued_books()

    def load_issued_books(self):
        for btn in self.book_buttons:
            btn.destroy()
        self.book_buttons.clear()
        self.selected_book_id = None

        issued_books = view_issued_books(self.member_id)
        for book in issued_books:
            status = book.get("status", "Issued")
            color = "red" if status in ["Issued","Reissued"] else "green"
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"{book['book_id']} | {book['title']} - {book['author']} | Category: {book.get('category','')} | Status: {status}",
                fg_color=color,
                anchor="w"
            )
            btn.configure(command=lambda b_id=book['book_id'], b_btn=btn: self.select_book(b_id, b_btn))
            btn.pack(pady=2, fill="x")
            self.book_buttons.append(btn)

    def select_book(self, book_id, btn):
        for b in self.book_buttons:
            status = "red" if "Issued" in b.cget("text") else "green"
            b.configure(fg_color=status)
        btn.configure(fg_color="blue")
        self.selected_book_id = book_id

    def reissue_selected_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Warning", "Please select a book to reissue!")
            return
        result = reissue_book(self.member_id, self.selected_book_id)
        messagebox.showinfo("Info", result)
        self.load_issued_books()

    def return_selected_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("Warning", "Please select a book to return!")
            return
        result = submit_book(self.member_id, self.selected_book_id)
        messagebox.showinfo("Info", result)
        self.load_issued_books()
