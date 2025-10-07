import customtkinter as ctk
from database import view_admins, add_admin, delete_admin

class AdminsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Admins")
        self.geometry("600x500")

        # Search
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=10, fill="x")
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(search_frame, placeholder_text="Search Admins...", textvariable=self.search_var).pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkButton(search_frame, text="Search", command=self.search_admins).pack(side="left", padx=10)

        # Admins List
        self.admins_listbox = ctk.CTkScrollableFrame(self, width=550, height=350)
        self.admins_listbox.pack(pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Add Admin", command=self.add_admin_popup).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Delete Admin", command=self.delete_admin_popup).pack(side="left", padx=10)

        self.selected_admin = None
        self.load_admins()

    def load_admins(self, admins=None):
        for widget in self.admins_listbox.winfo_children():
            widget.destroy()

        if admins is None:
            admins = view_admins()

        for a in admins:
            btn = ctk.CTkButton(
                self.admins_listbox,
                text=f"{a['id']} | {a['name']}",
                fg_color="purple",
                command=lambda aid=a['id']: self.select_admin(aid)
            )
            btn.pack(pady=2, fill="x", padx=5)

    def select_admin(self, admin_id):
        self.selected_admin = admin_id
        # Optional highlight
        for b in self.admins_listbox.winfo_children():
            b.configure(fg_color="purple")
        for b in self.admins_listbox.winfo_children():
            if b.cget("text").startswith(str(admin_id)):
                b.configure(fg_color="green")

    def add_admin_popup(self):
        from tkinter.simpledialog import askstring
        name = askstring("Add Admin", "Enter Name:")
        password = askstring("Add Admin", "Enter Password:")
        if name and password:
            add_admin(name, password)
            self.refresh_admins()

    def delete_admin_popup(self):
        if self.selected_admin:
            delete_admin(self.selected_admin)
            self.selected_admin = None
            self.refresh_admins()
        else:
            ctk.CTkMessagebox.show_warning("Select an admin first!")

    def refresh_admins(self):
        self.load_admins()

    def search_admins(self):
        query = self.search_var.get().lower()
        filtered = [
            a for a in view_admins()
            if query in (str(a['id']) + " " + a['name'].lower())
        ]
        self.load_admins(filtered)
