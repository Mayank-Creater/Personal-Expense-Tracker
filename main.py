import customtkinter as ctk
from PIL import Image, ImageDraw

BLACK = "#0F0F0F"
GREY = "#262625"
GREY_TEXT = "#A9A9A9"
GREEN = "#5C8D7B"
ORANGE = "#F58F36"
ORANGE_HOVER = "#F7831E"
WHITE = "#FFF"

class NavBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color=GREY, corner_radius=16)
        self.grid_rowconfigure(8, weight=1)

        self.btnWidth = 200
        self.btnHeight = 48
        self.labelFont = ('Gilroy-Medium', 20)
        self.btnFont = ('Gilroy-Regular', 20)

        self.dashboardIcon = ctk.CTkImage(Image.open('./images/dashboard_white.png'))
        self.invoiceIcon = ctk.CTkImage(Image.open('./images/invoice_white.png'))
        self.transactionIcon = ctk.CTkImage(Image.open('./images/transaction_white.png'))
        self.reportIcon = ctk.CTkImage(Image.open('./images/report_white.png'))


        self.userFrame = ctk.CTkFrame(self)
        self.userFrame.grid(row=0, column=0, pady=(20, 40))

        self.userFrame.grid_rowconfigure(1,minsize=20)
        self.userFrame.configure(fg_color="transparent")

        image = self.add_corners('./images/avatar.jpg', 80)
        photo = ctk.CTkImage(image, size=(60, 60))

        self.image_label = ctk.CTkLabel(self.userFrame,
                                        text='', 
                                        image=photo, 
                                        corner_radius=16)
        self.image_label.grid(row=0, column=0)

        self.text_label = ctk.CTkLabel(self.userFrame, 
                                       text="Hi, Mayank", 
                                       text_color='#fff', 
                                       font=("Gilroy-Bold", 24))
        self.text_label.grid(row=2, column=0)

        self.separator = ctk.CTkProgressBar(self.userFrame, height=2, width=175)
        self.separator.configure(progress_color='#ff0000', fg_color="#ff0000")
        self.separator.grid(row=3, column=0, pady=(50,0))

        self.adminLabel = ctk.CTkLabel(self, text="Administration", text_color="#fff", font=self.labelFont)
        self.adminLabel.grid(row=1, column=0, padx=10, sticky="w")        
        self.dashboardBtn = ctk.CTkButton(self, text="Dashboard", 
                                    width=self.btnWidth, 
                                    height=self.btnHeight, 
                                    image=self.dashboardIcon, 
                                    anchor='w', 
                                    corner_radius=8, 
                                    fg_color=ORANGE, 
                                    text_color=WHITE,
                                    hover_color=ORANGE_HOVER,
                                    font=self.btnFont,
                                    command=self.dashboard_btn_callback)

        self.dashboardBtn.grid(row=2, column=0, padx=(30,10), pady=(4,10))

        self.managementLabel = ctk.CTkLabel(self, text="Management", text_color="#fff", font=self.labelFont)
        self.managementLabel.grid(row=3, column=0, padx=10, sticky='w')
        self.invoiceBtn = ctk.CTkButton(self, text="Invoices", 
                                    width=self.btnWidth, 
                                    height=self.btnHeight, 
                                    image=self.invoiceIcon, 
                                    anchor='w', 
                                    corner_radius=8, 
                                    fg_color='transparent', 
                                    text_color=GREY_TEXT,
                                    hover_color=ORANGE_HOVER,
                                    font=self.btnFont,
                                    command=self.invoice_btn_callback)

        self.invoiceBtn.grid(row=4, column=0, padx=(30,10), pady=(4,2))

        self.transactionBtn = ctk.CTkButton(self, text="Transactions", 
                                    width=self.btnWidth, 
                                    height=self.btnHeight, 
                                    image=self.transactionIcon, 
                                    anchor='w', 
                                    corner_radius=8, 
                                    fg_color='transparent', 
                                    hover_color=ORANGE_HOVER,
                                    text_color=GREY_TEXT,
                                    font=self.btnFont,
                                    command=self.transaction_btn_callback)

        self.transactionBtn.grid(row=5, column=0, padx=(30,10), pady=(2,10))

        self.accountingLabel = ctk.CTkLabel(self, text="Accounting", text_color="#fff", font=self.labelFont)
        self.accountingLabel.grid(row=6, column=0, padx=10, sticky='w')

        self.reportBtn = ctk.CTkButton(self,
                                       text="Report",
                                       width=self.btnWidth,
                                       height=self.btnHeight,
                                       image=self.reportIcon,
                                       anchor='w', 
                                       corner_radius=8, 
                                       fg_color='transparent', 
                                       hover_color=ORANGE_HOVER,
                                       text_color=GREY_TEXT,
                                       font=self.btnFont,
                                       command=self.report_btn_callback)
        
        self.reportBtn.grid(row=7, column=0, padx=(30,10), pady=(4,20))

        self.signoutBtn = ctk.CTkButton(self,
                                        text='Sign Out',
                                        width=self.btnWidth,
                                        height=self.btnHeight,
                                        corner_radius=10,
                                        fg_color='#fff',
                                        text_color='#000',
                                        font=self.btnFont)
        self.signoutBtn.grid(row=9, column=0, pady=(0,10))

    def add_corners(self, image_path, radius):
        image = Image.open(image_path).convert("RGBA")

        # Create a mask 
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)

        # Create a new image with an alpha channel
        rounded_image = Image.new("RGBA", image.size)
        rounded_image.paste(image, (0, 0), mask)

        return rounded_image

    def change_to_default(self):
        self.dashboardBtn.configure(fg_color='transparent', text_color=GREY_TEXT)
        self.invoiceBtn.configure(fg_color='transparent', text_color=GREY_TEXT)
        self.transactionBtn.configure(fg_color='transparent', text_color=GREY_TEXT)
        self.reportBtn.configure(fg_color='transparent', text_color=GREY_TEXT)


    def dashboard_btn_callback(self):
        self.master.show_frame(DashboardFrame)
        self.change_to_default()
        self.dashboardBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def invoice_btn_callback(self):
        self.master.show_frame(InvoiceFrame)
        self.change_to_default()
        self.invoiceBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def transaction_btn_callback(self):
        self.master.show_frame(TransactionFrame)
        self.change_to_default()
        self.transactionBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def report_btn_callback(self):
        self.master.show_frame(ReportFrame)
        self.change_to_default()
        self.reportBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def signout_btn_callback(self):
        pass

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label = ctk.CTkLabel(self, text='Dashboard')
        self.label.grid(row=0, column=0, padx=20, pady=20)

class InvoiceFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text='Invoice')
        self.label.grid(row=0, column=0, padx=20, pady=20)

class TransactionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text='Transaction')
        self.label.grid(row=0, column=0, padx=20, pady=20)

class ReportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text='Report')
        self.label.grid(row=0, column=0, padx=20, pady=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x650+25+25")
        self.title("Personal Expense Tracker")
        # self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.configure(fg_color=BLACK)

        ctk.FontManager.load_font('./fonts/Gilroy/Gilroy-Medium.ttf')
        ctk.FontManager.load_font('./fonts/Gilroy/Gilroy-Regular.ttf')
        ctk.FontManager.load_font('./fonts/Gilroy/Gilroy-Bold.ttf')

        self.navbarFrame = NavBarFrame(self)
        self.navbarFrame.grid(row=0, column=0, padx=10, pady=20, sticky='nsew')

        self.current_frame = None
        self.show_frame(DashboardFrame)

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self)
        self.current_frame.grid(row=0, column=1, padx=10, pady=20, sticky='nsew')


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

        self.loginBtn = ctk.CTkButton(self, text="Login", command=self.validate_login)
        self.loginBtn.grid(row=2, column=0, padx=20, pady=20, columnspan=2)
        self.bind('<Return>', self.validate_login)

    def validate_login(self, event=None):
        username = self.userEntry.get()
        password = self.passEntry.get()
        if username=='admin' and password=='admin':
            self.destroy()
            App().mainloop()
        else:
            return False

if __name__=="__main__":
    app = LoginPage()
    app.mainloop()
