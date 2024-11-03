#importing required modules
import customtkinter as ctk
from PIL import Image, ImageDraw
from mysql.connector import Error, connection
import os
import datetime
import csv
import random

#setting constants for future use
BLACK = "#0F0F0F"
GREY = "#262625"
GREY_TEXT = "#A9A9A9"
GREEN = "#5C8D7B"
ORANGE = "#F58F36"
ORANGE_HOVER = "#F7831E"
WHITE = "#FFF"
BOLD_FONT = ("Gilroy-Bold", 24)
MEDIUM_FONT = ('Gilroy-Medium', 20)
REGULAR_FONT = ('Gilroy-Regular', 20)

userId = None

baseDir = os.getcwd()       #baseDir of the current executing folder

class NavBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color=GREY, corner_radius=16)
        self.grid_rowconfigure(8, weight=1)

        self.btnWidth = 200
        self.btnHeight = 48

        self.dashboardIcon = ctk.CTkImage(Image.open(os.path.join(baseDir,'images/dashboard_white.png')))
        self.invoiceIcon = ctk.CTkImage(Image.open(os.path.join(baseDir,'images/invoice_white.png')))
        self.transactionIcon = ctk.CTkImage(Image.open(os.path.join(baseDir,'images/transaction_white.png')))
        self.reportIcon = ctk.CTkImage(Image.open(os.path.join(baseDir,'images/report_white.png')))


        self.userFrame = ctk.CTkFrame(self)
        self.userFrame.grid(row=0, column=0, pady=(20, 40))

        self.userFrame.grid_rowconfigure(1,minsize=20)
        self.userFrame.configure(fg_color="transparent")

        image = self.add_corners(os.path.join(baseDir,'images/avatar.jpg'), 80)
        photo = ctk.CTkImage(image, size=(60, 60))

        self.image_label = ctk.CTkLabel(self.userFrame,
                                        text='', 
                                        image=photo, 
                                        corner_radius=16)
        self.image_label.grid(row=0, column=0)

        self.text_label = ctk.CTkLabel(self.userFrame, 
                                       text="Hi, Mayank", 
                                       text_color='#fff', 
                                       font=BOLD_FONT)
        self.text_label.grid(row=2, column=0)

        self.separator = ctk.CTkProgressBar(self.userFrame, height=2, width=175)
        self.separator.configure(progress_color='#ff0000', fg_color="#ff0000")
        self.separator.grid(row=3, column=0, pady=(50,0))

        self.adminLabel = ctk.CTkLabel(self, text="Administration", text_color="#fff", font=MEDIUM_FONT)
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
                                    font=REGULAR_FONT,
                                    command=self.dashboard_btn_callback)

        self.dashboardBtn.grid(row=2, column=0, padx=(30,10), pady=(4,10))

        self.managementLabel = ctk.CTkLabel(self, text="Management", text_color="#fff", font=MEDIUM_FONT)
        self.managementLabel.grid(row=3, column=0, padx=10, sticky='w')

        self.transactionBtn = ctk.CTkButton(self, text="Transactions", 
                                    width=self.btnWidth, 
                                    height=self.btnHeight, 
                                    image=self.transactionIcon, 
                                    anchor='w', 
                                    corner_radius=8, 
                                    fg_color='transparent', 
                                    hover_color=ORANGE_HOVER,
                                    text_color=GREY_TEXT,
                                    font=REGULAR_FONT,
                                    command=self.transaction_btn_callback)

        self.transactionBtn.grid(row=5, column=0, padx=(30,10), pady=(2,10))

        self.accountingLabel = ctk.CTkLabel(self, text="Accounting", text_color="#fff", font=MEDIUM_FONT)
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
                                       font=REGULAR_FONT,
                                       command=self.report_btn_callback)
        
        self.reportBtn.grid(row=7, column=0, padx=(30,10), pady=(4,20))

        self.signoutBtn = ctk.CTkButton(self,
                                        text='Sign Out',
                                        width=self.btnWidth,
                                        height=self.btnHeight,
                                        corner_radius=10,
                                        fg_color='#fff',
                                        text_color='#000',
                                        font=REGULAR_FONT,
                                        command=self.signout_btn_callback)
        self.signoutBtn.grid(row=9, column=0, pady=(0,10))

    # function to add rounded corners to image
    def add_corners(self, image_path, radius=80):
        image = Image.open(image_path).convert("RGBA")
        # Create a mask 
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, image.width, image.height), radius=radius, fill=255)

        # Create a new image with an alpha channel
        rounded_image = Image.new("RGBA", image.size)
        rounded_image.paste(image, (0, 0), mask)

        return rounded_image

    # change the color values of navbar buttons to default
    def change_to_default(self):
        self.dashboardBtn.configure(fg_color='transparent', text_color=GREY_TEXT)
        self.transactionBtn.configure(fg_color='transparent', text_color=GREY_TEXT)
        self.reportBtn.configure(fg_color='transparent', text_color=GREY_TEXT)


    def dashboard_btn_callback(self):
        self.master.show_frame(DashboardFrame)
        self.change_to_default()
        self.dashboardBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def transaction_btn_callback(self):
        self.master.show_frame(TransactionFrame)
        self.change_to_default()
        self.transactionBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def report_btn_callback(self):
        self.master.show_frame(ReportFrame)
        self.change_to_default()
        self.reportBtn.configure(fg_color=ORANGE, text_color=WHITE)

    def signout_btn_callback(self):
        self.master.destroy()
        LoginPage().mainloop()

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.addIcon = ctk.CTkImage(Image.open(os.path.join(baseDir, 'images/add_white.png')), size=(24,24))

        self.addTransactionBtn = ctk.CTkButton(self, fg_color=ORANGE, width=50, height=50, corner_radius=12, text='', image=self.addIcon, hover_color=ORANGE_HOVER, command=self.add_transaction_btn_callback)
        self.addTransactionBtn.grid(row=0, column=0, padx=20, pady=(10,0), columnspan=4, sticky='e')
        
        self.topFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.topFrame.grid(row=1, column=0, padx=20, pady=(0,20), sticky='ew', columnspan=2)

        self.titleTop = ctk.CTkLabel(self.topFrame, text='Our services', font=BOLD_FONT, text_color=WHITE)
        self.titleTop.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.btnFrame1 = ctk.CTkFrame(self.topFrame, fg_color='#f19882', height=200, corner_radius=16)
        self.btnFrame1.grid(row=1, column=0, padx=(10,0), pady=10)
 
        self.btnIcon1 = ctk.CTkLabel(self.btnFrame1,
                                        text='', 
                                        image=ctk.CTkImage(Image.open(os.path.join(baseDir, 'images/transaction_black.png')), size=(50, 50)), 
                                        corner_radius=16)
        self.btnIcon1.grid(row=0, column=0, padx=30, pady=(30,20))

        self.btnText1 = ctk.CTkLabel(self.btnFrame1, 
                                       text="View All\nTransactions", 
                                       text_color='#fff', 
                                       font=REGULAR_FONT)
        self.btnText1.grid(row=2, column=0, padx=20, pady=20)


        self.btnFrame2 = ctk.CTkFrame(self.topFrame, fg_color='#d82746', corner_radius=16)
        self.btnFrame2.grid(row=1, column=1, padx=(10,0), pady=10)

        self.btnIcon2 = ctk.CTkLabel(self.btnFrame2,
                                        text='', 
                                        image=ctk.CTkImage(Image.open(os.path.join(baseDir, 'images/report_black.png')), size=(50, 50)), 
                                        corner_radius=16)
        self.btnIcon2.grid(row=0, column=0, padx=30, pady=(30,20))

        self.btnText2 = ctk.CTkLabel(self.btnFrame2, 
                                       text="Generate\nReport", 
                                       text_color='#fff', 
                                       font=REGULAR_FONT)
        self.btnText2.grid(row=2, column=0, padx=20, pady=20)

        self.btnFrame1.bind('<Button-1>', self.transaction_btn_callback)
        self.btnFrame2.bind('<Button-1>', self.report_btn_callback)

        self.connector = App.create_connection(self)
        self.cursor = self.connector.cursor()
        query = f"SELECT date, amount, category FROM transactions WHERE type='expense' AND user_id={userId} ORDER BY date desc, id DESC LIMIT 5"
        self.cursor.execute(query)
        expense = self.cursor.fetchall()

        self.grid_columnconfigure(2, weight=1)
        self.recentExpenseFrame = ctk.CTkFrame(self, fg_color='#0a0a0a')
        self.recentExpenseFrame.grid(row=2, column=0, padx=20, pady=20, sticky='ew', columnspan=2)

        self.titleRecentExpense = ctk.CTkLabel(self.recentExpenseFrame, text='Recent Expenses', font=BOLD_FONT, text_color=WHITE)
        self.titleRecentExpense.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        for pos, i in enumerate(expense):
            date = i[0].strftime("%d/%m/%Y")
            self.data = ctk.CTkLabel(self.recentExpenseFrame, text=f"{date} \t {i[1]} \t {i[2]}", font=REGULAR_FONT, text_color=WHITE)
            self.data.grid(row=pos+1, column=0, padx=5, pady=5, columnspan=2, sticky='w')
            
        query = f"SELECT date, amount, category FROM transactions WHERE type='income' AND user_id={userId} ORDER BY date DESC, id desc LIMIT 5"
        self.cursor.execute(query)
        income = self.cursor.fetchall()

        self.recentIncomeFrame = ctk.CTkFrame(self, fg_color='#0a0a0a')
        self.recentIncomeFrame.grid(row=2, column=2, padx=(0,20), pady=20, sticky='nsew', columnspan=2)

        self.titleRecentIncome = ctk.CTkLabel(self.recentIncomeFrame, text='Recent Income', font=BOLD_FONT, text_color=WHITE)
        self.titleRecentIncome.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        for pos, i in enumerate(income):
            date = i[0].strftime("%d/%m/%Y")
            self.data = ctk.CTkLabel(self.recentIncomeFrame, text=f"{date} \t {i[1]} \t {i[2]}", font=REGULAR_FONT, text_color=WHITE)
            self.data.grid(row=pos+1, column=0, padx=5, pady=5, columnspan=2, sticky='w')

    def transaction_btn_callback(self, event=None):
        self.nav = NavBarFrame(self.master)
        self.nav.transaction_btn_callback()

    def report_btn_callback(self, event=None):
        self.nav = NavBarFrame(self.master)
        self.nav.report_btn_callback()

    def add_transaction_btn_callback(self):
        self.master.show_frame(AddTransactionFrame)

class AddTransactionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(3, weight=1)

        self.title = ctk.CTkLabel(self, text='Add New Transaction', font=BOLD_FONT, text_color=WHITE)
        self.title.grid(row=0, column=0, padx=20, pady=20)

        self.amountLabel = ctk.CTkLabel(self, text="Enter Amount", font=REGULAR_FONT, text_color=WHITE)
        self.amountEntry = ctk.CTkEntry(self)
        self.amountValidLabel = ctk.CTkLabel(self, text="Can't be Empty.", font=REGULAR_FONT, text_color='#f00')
        self.amountLabel.grid(row=1, column=0, padx=20, pady=20, sticky='w')
        self.amountEntry.grid(row=1, column=2, padx=(30,20), pady=20)
        self.amountValidLabel.grid(row=1, column=3, padx=20, pady=20)
        self.amountEntry.bind('<KeyRelease>', self.validate_amount)

        self.typeLabel = ctk.CTkLabel(self, text="Enter Type", font=REGULAR_FONT, text_color=WHITE)
        self.typeEntry = ctk.CTkOptionMenu(self, values=["Expense", "Income"])
        self.typeLabel.grid(row=2, column=0, padx=20, pady=20,sticky='w')
        self.typeEntry.grid(row=2, column=2, padx=(30,20), pady=20)

        self.categoryLabel = ctk.CTkLabel(self, text="Enter category", font=REGULAR_FONT, text_color=WHITE)
        self.categoryEntry = ctk.CTkEntry(self)
        self.categoryValidLabel = ctk.CTkLabel(self, text="Can't be Empty.", font=REGULAR_FONT, text_color="#f00")
        self.categoryLabel.grid(row=3, column=0, padx=20, pady=20, sticky='w')
        self.categoryEntry.grid(row=3, column=2, padx=(30, 20), pady=20)
        self.categoryValidLabel.grid(row=3, column=3, padx=20, pady=20)
        self.categoryEntry.bind('<KeyRelease>', self.validate_category)

        self.dateLabel = ctk.CTkLabel(self, text="Enter Date", font=REGULAR_FONT, text_color=WHITE)
        self.dateEntry = ctk.CTkEntry(self, placeholder_text="Enter like 09-01-2020")
        self.dateValidLabel = ctk.CTkLabel(self, text="Can't be Empty.", font=REGULAR_FONT, text_color='#f00')
        self.dateLabel.grid(row=4, column=0, padx=20, pady=20, sticky='w')
        self.dateEntry.grid(row=4, column=2, padx=(30, 20), pady=20)
        self.dateValidLabel.grid(row=4, column=3, padx=20, pady=20)
        self.dateEntry.bind('<KeyRelease>', self.validate_date)

        self.descLabel = ctk.CTkLabel(self, text="Enter description", font=REGULAR_FONT, text_color=WHITE)
        self.descEntry = ctk.CTkEntry(self)
        self.descLabel.grid(row=5, column=0, padx=20, pady=20, sticky='w')
        self.descEntry.grid(row=5, column=2, padx=(30,20), pady=20)

        self.addBtn = ctk.CTkButton(self, text="Add", font=REGULAR_FONT, text_color=WHITE, fg_color=ORANGE, command=self.add_btn_callback)
        self.addErrorLabel = ctk.CTkLabel(self, text='', font=REGULAR_FONT, text_color='#f00')
        self.addBtn.grid(row=6, column=0, padx=20, pady=20, columnspan=4)
        self.addErrorLabel.grid(row=7, column=0, padx=20, pady=20, columnspan=4)

    def validate_date(self, event=None):
        text = self.dateEntry.get()
        if text != '':
            res = True
            try:
                res = bool(datetime.datetime.strptime(text, '%d-%m-%Y'))
            except ValueError:
                res = False
            
            if res:
                self.dateValidLabel.configure(text='')
            else:
                self.dateValidLabel.configure(text='Not A valid Date.\nFormat should be dd-mm-yyyy')
        else:
            self.dateValidLabel.configure(text="Can't be Empty.")

    def validate_amount(self, event=None):
        text = self.amountEntry.get()
        if text != '':
            if text.isdigit():
                self.amountValidLabel.configure(text='')
            else:
                self.amountValidLabel.configure(text='Not a valid Amount.\nMust be numeric.')
        else:
            self.amountValidLabel.configure(text="Can't be Empty.")
            
    def validate_category(self, event=None):
        text = self.categoryEntry.get()

        if text:
            self.categoryValidLabel.configure(text='')
        else:
            self.categoryValidLabel.configure(text="Can't be Empty.")

    def add_btn_callback(self):
        try:
            amount = self.amountEntry.get()
            type = self.typeEntry.get()
            category = self.categoryEntry.get()
            category = category.capitalize()
            date = self.dateEntry.get()
            date = datetime.datetime.strptime(date, '%d-%m-%Y').strftime("%Y-%m-%d")
            desc = self.descEntry.get()

            validAmount = bool(self.amountValidLabel.cget('text'))
            validDate = bool(self.dateValidLabel.cget('text'))
            validCategory = bool(self.categoryValidLabel.cget('text'))

            if not(validAmount) and not(validDate) and not(validCategory):
                connector = App.create_connection(self)
                if connector:
                    cursor = connector.cursor()
                    query = "SELECT id from transactions order by id desc"
                    cursor.execute(query)
                    id = cursor.fetchall()[0][0] + 1

                    query = f"insert into transactions value({id}, {userId}, '{type}', '{category}', {amount}, '{date}', description='{desc}')"
                    cursor.execute(query)
                    connector.commit()
                    connector.close()

                    self.master.show_frame(DashboardFrame)

        except:
            self.addErrorLabel.configure(text='Data Invalid.\nPlease enter correct data.', text_color="#f00")

class TransactionFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self.expenseTitle = ctk.CTkLabel(self, text="All Expense", font=BOLD_FONT, text_color=WHITE)
        self.expenseTitle.grid(row=0, column=0, padx=20, pady=20, sticky='w')

        self.expenseFrame = ctk.CTkScrollableFrame(self, fg_color="#0a0a0a", label_text="Date \t\t Amount \t\t Category \t\t Description", label_font=BOLD_FONT, label_anchor="w")
        self.expenseFrame.grid(row=1, column=0, padx=20, pady=20, sticky='we')

        self.incomeTitle = ctk.CTkLabel(self, text="All Income", font=BOLD_FONT, text_color=WHITE)
        self.incomeTitle.grid(row=2, column=0, padx=20, pady=20, sticky='w')

        self.incomeFrame = ctk.CTkScrollableFrame(self, fg_color="#0a0a0a")
        self.incomeFrame.grid(row=3, column=0, padx=20, pady=20, sticky='we')

        connector = App.create_connection(self)
        if connector:
            cursor = connector.cursor()
            query = f"SELECT date, amount, category, description FROM transactions WHERE type='expense' AND user_id={userId} ORDER BY date DESC"
            cursor.execute(query)
            expense = cursor.fetchall()

            for pos, i in enumerate(expense):
                date = i[0].strftime("%d/%m/%Y")
                self.data = ctk.CTkLabel(self.expenseFrame, text=f"{date} \t\t {i[1]} \t\t {i[2]} \t\t {i[3]}", font=REGULAR_FONT, text_color=WHITE)
                self.data.grid(row=pos, column=0, columnspan=4, sticky='w')

            query = f"SELECT date, amount, category, description FROM transactions WHERE type='income' AND user_id={userId} ORDER BY date DESC"
            cursor.execute(query)
            income = cursor.fetchall()

            for pos, i in enumerate(income):
                date = i[0].strftime("%d/%m/%Y")
                self.data = ctk.CTkLabel(self.incomeFrame, text=f"{date} \t\t {i[1]} \t\t {i[2]} \t\t {i[3]}", font=REGULAR_FONT, text_color=WHITE)
                self.data.grid(row=pos, column=0, padx=5, pady=5, columnspan=4, sticky='w')

class ReportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self.generateDateReportTitle = ctk.CTkLabel(self, text='Generate Datewise Report', font=BOLD_FONT, text_color=WHITE)
        self.generateDateReportTitle.grid(row=0, column=0, padx=20, pady=20, sticky='w')
        
        self.dateLabel = ctk.CTkLabel(self, text='Enter Date interval', font=REGULAR_FONT, text_color=WHITE)
        self.startDate = ctk.CTkEntry(self, placeholder_text="Start Date")
        self.to = ctk.CTkLabel(self, text='to', font=REGULAR_FONT, text_color=WHITE)
        self.endDate = ctk.CTkEntry(self, placeholder_text="End Date")
        self.generateDateReportBtn = ctk.CTkButton(self, text="Generate", font=REGULAR_FONT, command=self.generate_report)
        self.dateValidLabel = ctk.CTkLabel(self, text="", font=REGULAR_FONT, text_color="#f00")
        self.dateLabel.grid(row=1, column=0, padx=20, pady=20, sticky='w')
        self.startDate.grid(row=1, column=1, padx=5, pady=20)
        self.to.grid(row=1, column=2, padx=5, pady=20)
        self.endDate.grid(row=1, column=3, padx=5, pady=20)
        self.generateDateReportBtn.grid(row=1, column=4, padx=20, pady=20)
        self.dateValidLabel.grid(row=2, column=0, padx=20, pady=20, columnspan=5)

        self.generateCategoryReportTitle = ctk.CTkLabel(self, text="Generate Category-wise Report", font=BOLD_FONT, text_color=WHITE)
        self.generateCategoryReportTitle.grid(row=3, padx=20, pady=(50,20))

        self.startDate.bind("<KeyRelease>", self.validate_date_date)
        self.endDate.bind("<KeyRelease>", self.validate_date_date)

        connector = App.create_connection(self)
        if connector:
            cursor = connector.cursor()
            query = "SELECT DISTINCT category FROM transactions;"
            cursor.execute(query)
            values = [x[0] for x in cursor.fetchall()]
            connector.close()

        self.selectCategoryLabel = ctk.CTkLabel(self, text="Select Category", font=REGULAR_FONT, text_color=WHITE)
        self.selectCategoryOption = ctk.CTkOptionMenu(self, values=values)
        self.selectCategoryLabel.grid(row=4, column=0, padx=20, pady=20, sticky='w')
        self.selectCategoryOption.grid(row=4, column=1, padx=5, pady=20)

        self.categoryDateLabel = ctk.CTkLabel(self, text='Enter Date interval', font=REGULAR_FONT, text_color=WHITE)
        self.categoryStartDate = ctk.CTkEntry(self, placeholder_text="Start Date")
        self.to2 = ctk.CTkLabel(self, text='to', font=REGULAR_FONT, text_color=WHITE)
        self.categoryEndDate = ctk.CTkEntry(self, placeholder_text="End Date")
        self.generateCategoryReportBtn = ctk.CTkButton(self, text="Generate", font=REGULAR_FONT, command=self.generate_category_report)
        self.categoryDateValidLabel = ctk.CTkLabel(self, text="", font=REGULAR_FONT, text_color="#f00")
        self.categoryDateLabel.grid(row=5, column=0, padx=20, pady=20, sticky='w')
        self.categoryStartDate.grid(row=5, column=1, padx=5, pady=20)
        self.to2.grid(row=5, column=2, padx=5, pady=20)
        self.categoryEndDate.grid(row=5, column=3, padx=5, pady=20)
        self.generateCategoryReportBtn.grid(row=5, column=4, padx=20, pady=20)
        self.categoryDateValidLabel.grid(row=6, column=0, padx=20, pady=20, columnspan=5)

        self.categoryStartDate.bind("<KeyRelease>", self.validate_date_category)
        self.categoryEndDate.bind("<KeyRelease>", self.validate_date_category)

    def validate_date_date(self, event=None):
        startDate = self.startDate.get()
        endDate = self.endDate.get()

        if startDate != '' or endDate !='':
            resStart = True
            resEnd = True
            try:
                resStart = bool(datetime.datetime.strptime(startDate, '%d-%m-%Y'))
                resEnd = bool(datetime.datetime.strptime(endDate, '%d-%m-%Y'))
            except ValueError:
                resStart = False
                resEnd = False
            
            if resStart==True and resEnd==True:
                self.dateValidLabel.configure(text='')
            else:
                self.dateValidLabel.configure(text='Not A valid Date.\nFormat should be dd-mm-yyyy')
        else:
            self.dateValidLabel.configure(text="")

    def validate_date_category(self, event=None):
        startDate = self.categoryStartDate.get()
        endDate = self.categoryEndDate.get()
        if startDate != '' or endDate !='':
            resStart = True
            resEnd = True
            try:
                resStart = bool(datetime.datetime.strptime(startDate, '%d-%m-%Y'))
                resEnd = bool(datetime.datetime.strptime(endDate, '%d-%m-%Y'))
            except ValueError:
                resStart = False
                resEnd = False
            
            if resStart==True and resEnd==True:
                self.categoryDateValidLabel.configure(text='')
            else:
                self.categoryDateValidLabel.configure(text='Not A valid Date.\nFormat should be dd-mm-yyyy')
        else:
            self.categoryDateValidLabel.configure(text="")

    def generate_report(self):
        startDate = self.startDate.get()
        endDate = self.endDate.get()
        connector = App.create_connection(self)
        if connector:
            cursor = connector.cursor()
            if startDate != '' and endDate != '':
                startDate = datetime.datetime.strptime(startDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                endDate = datetime.datetime.strptime(endDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                query = f"SELECT * FROM transactions WHERE date BETWEEN '{startDate}' AND '{endDate}' AND user_id={userId}"
            elif startDate == '' and endDate != '':
                endDate = datetime.datetime.strptime(endDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                query = f"SELECT * FROM transactions WHERE date < '{endDate}' AND user_id={userId}"
            elif startDate != '' and endDate == '':
                startDate = datetime.datetime.strptime(startDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                query = f"SELECT * FROM transactions WHERE date > '{startDate}' AND user_id={userId}"
            else:
                query = f"SELECT * FROM transactions WHERE user_id={userId}"

            cursor.execute(query)

            result = cursor.fetchall()

            column_names = [i[0] for i in cursor.description]
            fileName = f'Report_{random.randint(1,999999)}.csv'
            fp = open(fileName, 'w')
            myFile = csv.writer(fp, lineterminator = '\n') #use lineterminator for windows
            myFile.writerow(column_names)
            myFile.writerows(result)
            fp.close()

            connector.close()
            self.dateValidLabel.configure(text=f"Report Generated.\n Saved as {fileName}", text_color="#0f0")

    def generate_category_report(self):
        startDate = self.categoryStartDate.get()
        endDate = self.categoryEndDate.get()
        category = self.selectCategoryOption.get()
        connector = App.create_connection(self)
        if connector:
            cursor = connector.cursor()
            if startDate != '' and endDate != '':
                startDate = datetime.datetime.strptime(startDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                endDate = datetime.datetime.strptime(endDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                query = f"SELECT * FROM transactions WHERE date BETWEEN '{startDate}' AND '{endDate}' AND category='{category}' AND user_id={userId}"
            elif startDate == '' and endDate != '':
                endDate = datetime.datetime.strptime(endDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                query = f"SELECT * FROM transactions WHERE date < '{endDate}' AND category='{category}' AND user_id={userId}"
            elif startDate != '' and endDate == '':
                startDate = datetime.datetime.strptime(startDate, '%d-%m-%Y').strftime("%Y-%m-%d")
                query = f"SELECT * FROM transactions WHERE date > '{startDate}' AND category='{category}' AND user_id={userId}"
            else:
                query = f"SELECT * FROM transactions WHERE category='{category}' AND user_id={userId}"

            cursor.execute(query)

            result = cursor.fetchall()

            column_names = [i[0] for i in cursor.description]
            fileName = f'Report_{category}_{random.randint(1,999999)}.csv'
            fp = open(fileName, 'w')
            myFile = csv.writer(fp, lineterminator = '\n') #use lineterminator for windows
            myFile.writerow(column_names)
            myFile.writerows(result)
            fp.close()

            connector.close()
            self.categoryDateValidLabel.configure(text=f"Report Generated.\n Saved as {fileName}", text_color="#0f0")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x700+25+0")
        self.title("Personal Expense Tracker")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.configure(fg_color=BLACK)

        ctk.FontManager.load_font(os.path.join(baseDir, 'fonts/Gilroy/Gilroy-Medium.ttf'))
        ctk.FontManager.load_font(os.path.join(baseDir, 'fonts/Gilroy/Gilroy-Regular.ttf'))
        ctk.FontManager.load_font(os.path.join(baseDir, 'fonts/Gilroy/Gilroy-Bold.ttf'))

        self.navbarFrame = NavBarFrame(self)
        self.navbarFrame.grid(row=0, column=0, padx=10, pady=20, sticky='nsew')

        self.current_frame = None
        self.show_frame(DashboardFrame)

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self)
        self.current_frame.grid(row=0, column=1, padx=10, pady=20, sticky='nsew')

    def create_connection(self):
        try:
            connector = connection.MySQLConnection(host='localhost',
                                                user='root',
                                                password='root',
                                                database='expense_tracker')
            if connector.is_connected():
                return connector
        except Error as e:
            print(f'Error: {e}')
            return None

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

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

        self.invalidLabel = ctk.CTkLabel(self, text='', text_color='#f00')
        self.invalidLabel.grid(row=3, column=0, padx=10, pady=10, columnspan=2)


    def validate_login(self, event=None):
        global userId
        username = self.userEntry.get()
        password = self.passEntry.get()
        connector = App.create_connection(self)
        if connector:
            cursor = connector.cursor()

            query = f"SELECT * FROM users WHERE username='{username}' and password='{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            connector.close()

            if user:
                userId = user[0]
                self.destroy()
                App().mainloop()
            else:
                self.invalidLabel.configure(text='Invalid Credentials')

if __name__=="__main__":
    app = LoginPage()
    app.mainloop()