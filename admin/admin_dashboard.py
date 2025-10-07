import customtkinter as ctk
from admin.manage_books import BooksWindow
from admin.manage_members import MembersWindow
from admin.manage_admins import AdminsWindow
from admin.admin_login import AdminLogin
from database import view_issued_books_all  # Make sure this returns list of dicts: book_id, title, member_id, status

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1000x700")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # --- Header ---
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(header_frame, text="Admin Dashboard", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=20)
        ctk.CTkButton(header_frame, text="Logout", fg_color="red", command=self.logout).pack(side="right", padx=20)
        ctk.CTkButton(header_frame, text="Toggle Theme", command=self.toggle_theme).pack(side="right", padx=10)

        # --- Issued Books Overview ---
        issued_frame = ctk.CTkFrame(self, corner_radius=10)
        issued_frame.pack(fill="both", expand=False, padx=20, pady=(0, 20))
        ctk.CTkLabel(issued_frame, text="Issued Books Overview", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=10, pady=6)

        self.issued_scroll = ctk.CTkScrollableFrame(issued_frame, width=950, height=200)
        self.issued_scroll.pack(padx=10, pady=6)
        self.issued_labels = []

        # --- Action Buttons ---
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10)
        ctk.CTkButton(buttons_frame, text="Manage Books", width=200, command=self.open_books).pack(pady=6)
        ctk.CTkButton(buttons_frame, text="Manage Members", width=200, command=self.open_members).pack(pady=6)
        ctk.CTkButton(buttons_frame, text="Manage Admins", width=200, command=self.open_admins).pack(pady=6)

        # --- Window references ---
        self.books_window = None
        self.members_window = None
        self.admins_window = None

        # Start loading issued books and auto-refresh every 3 seconds
        self.load_issued_books()
        self.after(3000, self.refresh_issued_books)

        self.mainloop()

    # --- Load issued books into scrollable frame ---
    def load_issued_books(self):
        # Clear previous labels
        for lbl in self.issued_labels:
            lbl.destroy()
        self.issued_labels.clear()

        # Get all issued books (updated to match new schema)
        issued_books = view_issued_books_all()  # should return list of dicts: book_id, title, member_id, status

        for ib in issued_books:
            # Status color: red = Issued, orange = Reissued, green = Returned
            status_color = "green" if ib["status"] == "Returned" else "orange" if ib["status"] == "Reissued" else "red"
            lbl = ctk.CTkLabel(
                self.issued_scroll,
                text=f"{ib['book_id']} | {ib['title']} | Member: {ib['member_id']} | Status: {ib['status']}",
                fg_color=status_color,
                corner_radius=5,
                height=30,
                anchor="w"
            )
            lbl.pack(fill="x", padx=5, pady=2)
            self.issued_labels.append(lbl)

    # --- Auto-refresh ---
    def refresh_issued_books(self):
        self.load_issued_books()
        self.after(3000, self.refresh_issued_books)

    # --- Open windows ---
    def open_books(self):
        if self.books_window and ctk.CTkToplevel.winfo_exists(self.books_window):
            self.books_window.lift()
            return
        self.books_window = BooksWindow(self)

    def open_members(self):
        if self.members_window and ctk.CTkToplevel.winfo_exists(self.members_window):
            self.members_window.lift()
            return
        self.members_window = MembersWindow(self)

    def open_admins(self):
        if self.admins_window and ctk.CTkToplevel.winfo_exists(self.admins_window):
            self.admins_window.lift()
            return
        self.admins_window = AdminsWindow(self)

    # --- Logout ---
    def logout(self):
        self.destroy()
        AdminLogin()

    # --- Toggle dark/light theme ---
    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Dark" if mode=="Light" else "Light")
