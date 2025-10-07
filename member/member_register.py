import customtkinter as ctk
from tkinter import messagebox
from database import add_member  # updated add_member function uses name, email, phone, password

class MemberRegister(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Member Registration")
        self.geometry("400x400")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Register as Member", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        ctk.CTkLabel(self, text="Name").pack(pady=(10,0))
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack()

        ctk.CTkLabel(self, text="Email(Required)").pack(pady=(10,0))
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        ctk.CTkLabel(self, text="Phone (Required)").pack(pady=(10,0))
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.pack()

        ctk.CTkLabel(self, text="Password").pack(pady=(10,0))
        self.pw_entry = ctk.CTkEntry(self, show="*")
        self.pw_entry.pack()

        ctk.CTkButton(self, text="Register", command=self.register).pack(pady=20)
        self.mainloop()

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip() or None
        phone = self.phone_entry.get().strip() or None
        pw = self.pw_entry.get().strip() or "member123"

        if not name:
            messagebox.showwarning("Validation", "Name is required")
            return

        add_member(name=name, email=email, phone=phone, password=pw)
        messagebox.showinfo("Success", "Member registered successfully")
        self.destroy()
