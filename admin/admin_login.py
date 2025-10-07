import customtkinter as ctk
from tkinter import messagebox
from database import validate_admin_login

class AdminLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Login")
        self.geometry("400x300")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Admin Login", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Name").pack(pady=(10,0))
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=4)
        ctk.CTkLabel(self, text="Password").pack(pady=(10,0))
        self.pw_entry = ctk.CTkEntry(self, show="*")
        self.pw_entry.pack(pady=4)
        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)

        self.mainloop()

    def login(self):
        name = self.name_entry.get().strip()
        pw = self.pw_entry.get().strip()

        if not name or not pw:
            messagebox.showwarning("Input Error", "Please enter both Name and Password")
            return

        if validate_admin_login(name, pw):
            self.destroy()
            from admin.admin_dashboard import AdminDashboard
            AdminDashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
