import customtkinter as ctk
from database import view_members, add_member, delete_member

class MembersWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manage Members")
        self.geometry("600x500")

        # Search
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=10, fill="x")
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(search_frame, placeholder_text="Search Members...", textvariable=self.search_var).pack(side="left", padx=10, fill="x", expand=True)
        ctk.CTkButton(search_frame, text="Search", command=self.search_members).pack(side="left", padx=10)

        # Members List
        self.members_listbox = ctk.CTkScrollableFrame(self, width=550, height=350)
        self.members_listbox.pack(pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Add Member", command=self.add_member_popup).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Delete Member", command=self.delete_member_popup).pack(side="left", padx=10)

        self.selected_member = None
        self.load_members()

    def load_members(self, members=None):
        for widget in self.members_listbox.winfo_children():
            widget.destroy()

        if members is None:
            members = view_members()

        for m in members:
            btn = ctk.CTkButton(
                self.members_listbox,
                text=f"{m['id']} | {m['name']} | Email: {m.get('email','N/A')}",
                fg_color="blue",
                command=lambda mid=m['id']: self.select_member(mid)
            )
            btn.pack(pady=2, fill="x", padx=5)

    def select_member(self, member_id):
        self.selected_member = member_id
        # Highlight selection (optional)
        for b in self.members_listbox.winfo_children():
            b.configure(fg_color="blue")
        # Find the button corresponding to selected_member
        for b in self.members_listbox.winfo_children():
            if b.cget("text").startswith(str(member_id)):
                b.configure(fg_color="green")

    def add_member_popup(self):
        # Use simple dialogs for name, email, phone, password
        from tkinter.simpledialog import askstring
        name = askstring("Add Member", "Enter Name:")
        email = askstring("Add Member", "Enter Email (optional):")
        phone = askstring("Add Member", "Enter Phone (optional):")
        password = askstring("Add Member", "Enter Password:")
        if name and password:
            add_member(name, email, phone, password)
            self.refresh_members()

    def delete_member_popup(self):
        if self.selected_member:
            delete_member(self.selected_member)
            self.selected_member = None
            self.refresh_members()
        else:
            ctk.CTkMessagebox.show_warning("Select a member first!")

    def refresh_members(self):
        self.load_members()

    def search_members(self):
        query = self.search_var.get().lower()
        filtered = [
            m for m in view_members()
            if query in (str(m['id']) + " " + m['name'].lower() + " " + (m.get('email','').lower()))
        ]
        self.load_members(filtered)
