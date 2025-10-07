import customtkinter as ctk
from tkinter import messagebox
from database import validate_member_login

class MemberLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Member Login")
        self.geometry("400x300")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Member Login", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Email").pack(pady=(10,0))
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(pady=4)
        ctk.CTkLabel(self, text="Password").pack(pady=(10,0))
        self.pw_entry = ctk.CTkEntry(self, show="*")
        self.pw_entry.pack(pady=4)
        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)

        self.mainloop()

    def login(self):
        email = self.email_entry.get().strip()
        pw = self.pw_entry.get().strip()

        if not email or not pw:
            messagebox.showwarning("Input Error", "Please enter both Email and Password")
            return

        if validate_member_login(email, pw):
            self.destroy()
            from member.member_dashboard import MemberDashboard
            MemberDashboard(email)  # Pass email to dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
