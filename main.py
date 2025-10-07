import customtkinter as ctk
from admin.admin_login import AdminLogin
from member.member_login import MemberLogin
from member.member_register import MemberRegister

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("400x300")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="BMS - Role Selection", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkButton(self, text="Admin Login", width=200, command=self.open_admin).pack(pady=12)
        ctk.CTkButton(self, text="Member Login", width=200, command=self.open_member_login).pack(pady=12)
        ctk.CTkButton(self, text="Register Member", width=200, command=self.open_member_register).pack(pady=12)
        self.mainloop()

    def open_admin(self):
        self.destroy()
        AdminLogin()

    def open_member_login(self):
        self.destroy()
        MemberLogin()

    def open_member_register(self):
        self.destroy()
        MemberRegister()

if __name__ == "__main__":
    MainApp()
