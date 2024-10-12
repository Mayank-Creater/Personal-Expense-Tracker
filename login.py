import customtkinter as ctk
from main_window import Home

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # self.geometry("400x400")
        self.title("Login Page")

        self.grid_columnconfigure(0, weight=1)

        self.userLabel = ctk.CTkLabel(self, text="Enter Username:")
        self.userEntry = ctk.CTkEntry(self, placeholder_text="Username", width=200)
        self.userLabel.grid(row=0, column=0, padx=10, pady=10)
        self.userEntry.grid(row=0, column=1, padx=10, pady=10)

        self.passlabel = ctk.CTkLabel(self, text="Enter Password:")
        self.passEntry = ctk.CTkEntry(self, placeholder_text="Password", width=200, show="*")
        self.passlabel.grid(row=1, column=0, padx=10, pady=10)
        self.passEntry.grid(row=1, column=1, padx=10, pady=10)

        self.loginBtn = ctk.CTkButton(self, text="Login", command=self.login)
        self.loginBtn.grid(row=2, column=0, padx=20, pady=20, columnspan=2)

    def validate_login(self):
        username = self.userEntry.get()
        password = self.passEntry.get()
        if username=='admin' and password=='admin':
            self.destroy()
            Home()
        else:
            return False

if __name__=="__main__":
    app = LoginPage()
    app.mainloop()