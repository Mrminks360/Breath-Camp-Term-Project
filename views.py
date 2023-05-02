

import tkinter as tk
from tkinter import ttk, messagebox
from db import DatabaseUti
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime


class RegistrationFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text='Camper Information', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()

        
        self.FirstName = tk.StringVar()
        self.LastName = tk.StringVar()
        self.Birthday = tk.StringVar()
        self.Gender = tk.StringVar()
        self.ArrivalDate = tk.StringVar()
        self.Equipment = tk.BooleanVar()
        self.DepartureDate = tk.StringVar()
        self.CompletedForm = tk.BooleanVar()
        self.CheckedIn = tk.BooleanVar()
        self.MailingAddress = tk.StringVar()
        self.Friends = tk.StringVar()

        self.create_page()
        ttk.Button(self, text='Submit', command=self.create_camper_data).pack(side="right", pady=10, padx=5,
                                                                              anchor=tk.E)
        ttk.Button(self, text='Clear', command=self.clear_create_data).pack(side="right", pady=10, padx=5, anchor=tk.E)

    def create_page(self):
        self.info = ttk.Frame(self)
        self.info.pack()

        # First row
        ttk.Label(self.info, text='First Name(*): ', font=("Calibri 12")).grid(row=0, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.FirstName, width=20).grid(row=0, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Last Name(*): ', font=("Calibri 12")).grid(row=0, column=2, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.LastName, width=20).grid(row=0, column=3, pady=5, sticky=tk.W)

        # Second Row
        # gender menu list
        ttk.Label(self.info, text='Gender(*): ', font=("Calibri 12")).grid(row=1, column=0, pady=5, sticky=tk.W)
        menu_list = ['', 'Female', 'Male']


        self.Gender.set(menu_list[0])
        field_drop = ttk.OptionMenu(self.info, self.Gender, *menu_list)
        field_drop.config(width=15)
        field_drop.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.info, text='Birthday: ', font=("Calibri 12")).grid(row=1, column=2, pady=5, sticky=tk.W)
        self.Birthday = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                                bg="darkblue", fg="white",
                                year=date.today().year, top_level=self.winfo_toplevel())
        self.Birthday.delete(0, "end")
        self.Birthday.grid(row=1, column=3, sticky=tk.W)

        # Third Row

        ttk.Label(self.info, text='Arrival Date: ', font=("Calibri 12")).grid(row=2, column=0, pady=5, sticky=tk.W)
        self.ArrivalDate = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                                    bg="darkblue", fg="white",
                                    year=date.today().year, top_level=self.winfo_toplevel())
        self.ArrivalDate.delete(0, "end")
        self.ArrivalDate.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.info, text='Departure Date: ', font=("Calibri 12")).grid(row=2, column=2, pady=5, sticky=tk.W)
        self.DepartureDate = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                                        bg="darkblue", fg="white",
                                        year=date.today().year, top_level=self.winfo_toplevel())
        self.DepartureDate.delete(0, "end")
        self.DepartureDate.grid(row=2, column=3, sticky=tk.W)

        # Fourth Row

        ttk.Label(self.info, text='Mailing Address: ', font=("Calibri 12")).grid(row=3, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.MailingAddress, width=20).grid(row=3, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Friends: ', font=("Calibri 12")).grid(row=3, column=2, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.Friends, width=20).grid(row=3, column=3, pady=5, sticky=tk.W)

        # Fifth Row

        ttk.Label(self.info, text='Forms: ', font=("Calibri 12")).grid(row=4, column=0, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.CompletedForm, onvalue=True, offvalue=False).grid(row=4, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Equipment: ', font=("Calibri 12")).grid(row=4, column=2, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.Equipment, onvalue=True, offvalue=False).grid(row=4, column=3, pady=5, sticky=tk.W)
        # sixth Row
        ttk.Label(self.info, text='Check-In: ', font=("Calibri 12")).grid(row=5, column=0, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.CheckedIn, onvalue=True, offvalue=False).grid(row=5, column=1, pady=5, sticky=tk.W)

    def create_camper_data(self):
        db = DatabaseUti()
        required_values = [self.FirstName.get(), self.LastName.get(), self.Birthday.get_date()]

        # Check if any required fields are empty
        if '' in required_values:
            tk.messagebox.showerror('Warning!',
                                    "Please complete all the required information")
        else:
            # Check if camper is already registered
            conditions = f"FirstName = '{self.FirstName.get()}' AND LastName = '{self.LastName.get()}' AND Birthday = '{self.Birthday.get_date()}'"
            result = db.query_table_with_condition("camper", "*", conditions)
            if result:
                tk.messagebox.showerror('Error!',
                                        "This Camper is already registered")
                self.clear_create_data()
            else:
                # Insert new camper data into the table
                values = (None, self.FirstName.get(), self.LastName.get(), self.Birthday.get_date(), self.Gender.get(),
                        self.ArrivalDate.get_date(), self.Equipment.get(), self.DepartureDate.get_date(),
                        self.CompletedForm.get(), self.CheckedIn.get(), self.MailingAddress.get(),
                        self.Friends.get())
                status = db.insert_one_record("camper", values)
                if status == False:
                    tk.messagebox.showerror('Error!',
                                            "Failed to register Camper")
                    self.clear_create_data()
                else:
                    tk.messagebox.showinfo('Successful!',
                                        "The Camper has been successfully registered")
                    self.clear_create_data()



    def clear_create_data(self):
        self.FirstName.set('')
        self.LastName.set('')
        self.Birthday.delete(0, "end")
        self.Gender.set('')
        self.ArrivalDate.delete(0, "end")
        self.DepartureDate.delete(0, "end")
        self.CompletedForm.set(False)
        self.Equipment.set(False)
        self.CheckedIn.set(False)
        self.MailingAddress.set('')
        self.Friends.set('')

class CheckinFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text='Checkin Page', font=("Bahnschrift", 16)).pack()

        self.table_view = ttk.Frame()
        self.table_view.pack()
        self.create_page()

        ttk.Button(self, text="Refresh", command=self.show_camper_data).pack(anchor=tk.E, pady=5)

    def create_page(self):

            # Search By Frame
        self.search_by_frame = ttk.LabelFrame(self, text='Search By')
        self.search_by_frame.pack(pady=5, expand=True)

        # contain the treeview!
        self.table_by_frame = ttk.Frame(self)
        self.table_by_frame.pack()

        menu_list = ['', 'FirstName', 'LastName', 'Birthday', 'Gender', 'ArrivalDate', 'Equipment', 'DepartureDate', 'CompletedForm', 'CheckedIn', 'MailingAddress', 'Friends']

        oMenuWidth = len(max(menu_list, key=len))

        self.clicked = tk.StringVar()
        self.clicked.set(menu_list[0])

        field_drop = ttk.OptionMenu(self.search_by_frame, self.clicked, *menu_list)
        field_drop.config(width=oMenuWidth)
        field_drop.grid(row=0, column=0)

        self.field_value = ttk.Entry(self.search_by_frame, width=30)
        self.field_value.grid(row=0, column=1)

        ttk.Button(self.search_by_frame, text="Search", command=self.show_camper_data).grid(row=0, column=2)

        # Table view - to display the search result
        columns = ("CamperID", 'FirstName', 'LastName', 'Birthday', 'Gender', 'ArrivalDate', 'Equipment', 'DepartureDate', 'CompletedForm', 'CheckedIn', 'MailingAddress', 'Friends')
        
        # Create the tree_view first
        self.tree_view = ttk.Treeview(self.table_by_frame, show='headings', selectmode='browse', columns=columns)

        self.tree_view.column("CamperID", width=100, anchor='center')
        self.tree_view.heading("CamperID", text="CamperID")

        for item in columns[1:]:
            self.tree_view.column(item, width=130, anchor='center')
            self.tree_view.heading(item, text=item)

        # add a horizontal scrollbar
        scrollbar_horizontal = ttk.Scrollbar(self.table_by_frame, orient=tk.HORIZONTAL, command=self.tree_view.xview)
        scrollbar_horizontal.pack(side="bottom", fill='x')

        # add a vertical scrollbar
        scrollbar_vertical = ttk.Scrollbar(self.table_by_frame, orient=tk.VERTICAL, command=self.tree_view.yview)
        scrollbar_vertical.pack(side="right", fill='y')

        self.tree_view.configure(xscrollcommand=scrollbar_horizontal.set, yscrollcommand=scrollbar_vertical.set)

        self.tree_view.pack(side="left", fill=tk.BOTH, expand=True)


        #update frame
        self.update_frame = ttk.Frame(self)
        self.update_frame.pack(pady=5)

        ttk.Label(self.update_frame, text="Camper ID:").grid(row=0, column=0)
        self.camper_id_entry = ttk.Entry(self.update_frame, width=10)
        self.camper_id_entry.grid(row=0, column=1)

        self.equipment_var = tk.BooleanVar()
        self.form_var = tk.BooleanVar()
        self.checkin_var = tk.BooleanVar()

        ttk.Checkbutton(self.update_frame, text="Equipment", variable=self.equipment_var).grid(row=1, column=0)
        ttk.Checkbutton(self.update_frame, text="Forms", variable=self.form_var).grid(row=1, column=1)
        ttk.Checkbutton(self.update_frame, text="Check-in", variable=self.checkin_var).grid(row=1, column=2)

        ttk.Button(self.update_frame, text="Update", command=self.update_camper_data).grid(row=2, column=1)

    def show_camper_data(self):
        # delete the old records!
        for _ in map(self.tree_view.delete, self.tree_view.get_children("")):
            pass

        db = DatabaseUti()

        field = self.clicked.get()
        field_value = self.field_value.get()

        if len(field_value) == 0:
            records = db.query_table("camper", "*")
            print(records)
            index = 0
            for record in records[::-1]:
                self.tree_view.insert("", index + 1, values=record)

        else:
            conditions = field + "='" + field_value + "'"
            records = db.query_table_with_condition("camper", "*", conditions)
            if records == False:
                tk.messagebox.showerror('Warning!',
                                        "This record doesn't exist!")
            else:
                index = 0
                for record in records[::-1]:
                    print(record)
                    self.tree_view.insert("", index + 1, values=record)

    def update_camper_data(self):
        camper_id = self.camper_id_entry.get()
        equipment = self.equipment_var.get()
        form = self.form_var.get()
        checkin = self.checkin_var.get()

        if not camper_id:
            tk.messagebox.showerror("Error", "Please enter a Camper ID.")
            return

        db = DatabaseUti()
        db.update_camper_checkin(camper_id, Equipment=equipment, CompletedForm=form, CheckedIn=checkin)
        self.show_camper_data()

class UpdateFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text='Update Page', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()

        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.gender = tk.StringVar()
        self.mobile = tk.StringVar()
        self.address = tk.StringVar()
        self.city = tk.StringVar()
        self.state = tk.StringVar()
        self.zipcode = tk.StringVar()
        self.email = tk.StringVar()

        self.create_page()

    def create_page(self):
        # Search By Frame
        self.search_by_frame = ttk.LabelFrame(self, text='Search Profile By Email')
        self.search_by_frame.pack(pady=5, expand=True)

        ttk.Entry(self.search_by_frame, textvariable=self.email, width=30).grid(row=0, column=1, padx=5)
        ttk.Button(self.search_by_frame, text="Search", command=self.show_customer_data).grid(row=0, column=2, pady=10)

        # Show Customer Frame
        self.info = ttk.LabelFrame(self, text='Customer Profile')
        self.info.pack(pady=5, expand=True)

        # first row
        ttk.Label(self.info, text='First Name(*): ', font=("Calibri 12")).grid(row=0, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.fname, width=20).grid(row=0, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, width=5).grid(row=0, column=2)

        ttk.Label(self.info, text='Last Name(*): ', font=("Calibri 12")).grid(row=0, column=3, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.lname, width=20).grid(row=0, column=4, pady=5, sticky=tk.W)

        # Second Row
        # gender menu list
        ttk.Label(self.info, text='Gender(*): ', font=("Calibri 12")).grid(row=1, column=0, pady=5, sticky=tk.W)
        menu_list = ['', 'Female', 'Male']

        self.gender.set(menu_list[0])
        field_drop = ttk.OptionMenu(self.info, self.gender, *menu_list)
        field_drop.config(width=15)
        field_drop.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.info, width=5).grid(row=1, column=2)

        ttk.Label(self.info, text='Date of Birth: ', font=("Calibri 12")).grid(row=1, column=3, pady=5, sticky=tk.W)
        # self.dob entry!
        self.dob = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                             bg="darkblue", fg="white",
                             year=date.today().year)
        self.dob.delete(0, "end")
        self.dob.grid(row=1, column=4, sticky=tk.W)

        # Thrid Row
        ttk.Label(self.info, text='Email(*)', state = 'disabled', font=("Calibri 12")).grid(row=2, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.email, state = 'disabled', width=20).grid(row=2, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, width=5).grid(row=2, column=2)

        ttk.Label(self.info, text='Mobile(*)', font=("Calibri 12")).grid(row=2, column=3, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.mobile, width=20).grid(row=2, column=4, pady=5, sticky=tk.W)

        # Fourth Row
        ttk.Label(self.info, text='Address', font=("Calibri 12")).grid(row=3, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.address, width=20).grid(row=3, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, width=5).grid(row=3, column=2)

        ttk.Label(self.info, text='City ', font=("Calibri 12")).grid(row=3, column=3, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.city, width=20).grid(row=3, column=4, pady=5, sticky=tk.W)

        # Fifth Row
        ttk.Label(self.info, text='State: ', font=("Calibri 12")).grid(row=4, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.state, width=20).grid(row=4, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, width=5).grid(row=4, column=2)

        ttk.Label(self.info, text='Zipcode', font=("Calibri 12")).grid(row=4, column=3, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.zipcode, width=20).grid(row=4, column=4, pady=5, sticky=tk.W)

        ttk.Button(self.info, text='Clear', command=self.clear_customer_data).grid(row=5, column=3, sticky=tk.W)
        ttk.Button(self.info, text='submit', command=self.update_customer_data).grid(row=5, column=4, sticky=tk.W)

    def show_customer_data(self):
        db = DatabaseUti()
        condition = f"email = '{self.email.get()}'"
        result = db.query_table_with_condition("customers", "*", condition)
        print(result)
        if len(result)== 0:
            tk.messagebox.showerror('Warning!',
                                    "This email address doesn't exist!")
        else:
            self.fname.set(result[0][0])
            self.lname.set(result[0][1])
            self.gender.set(result[0][2])
            if len(result[0][3]) != 0:
                self.dob.set_date(result[0][3])
            self.mobile.set(result[0][4])
            self.address.set(result[0][5])
            self.city.set(result[0][6])
            self.state.set(result[0][7])
            self.zipcode.set(result[0][8])

    def clear_customer_data(self):
        self.fname.set("")
        self.lname.set("")
        self.gender.set("")
        self.dob.delete(0, "end")
        self.mobile.set("")
        self.address.set("")
        self.city.set("")
        self.state.set("")
        self.zipcode.set("")
        self.email.set("")

    def update_customer_data(self):
        db = DatabaseUti()

        if self.email.get() == '':
            tk.messagebox.showerror('Warning!',
                                    "This email address doesn't exist!")

        else:
            flag = db.update_customer_table(self.fname.get(), self.lname.get(), self.gender.get(),
                                            self.dob.get(), self.mobile.get(), self.address.get(),
                                            self.city.get(), self.state.get(), self.zipcode.get(),
                                            self.email.get())
            if flag == False:
                tk.messagebox.showerror('Warning!',
                                        "This email address doesn't exist!")
            else:
                tk.messagebox.showinfo('Successful!',
                                       "The customer profile has been successfully updated")
            self.clear_customer_data()

class PaymentFrame(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text = 'Payment Page', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()
        
        self.email = tk.StringVar()
        self.p_amount = tk.StringVar()
        
        self.create_page()

        ttk.Button(self, text = 'Submit', command= self.create_payment_data).pack(pady = 10, anchor = tk.E)
        
    
    def create_page(self):
        
        self.payment = ttk.Frame(self)
        self.payment.pack()
        
        ttk.Label(self.payment, text = "Email Address: ", font = ("Calibri 12")).grid(row=0, column=0, pady=10, sticky = tk.W)
        ttk.Entry(self.payment, textvariable = self.email, width = 30).grid(row=0, column=1, pady=10, sticky = tk.W)
        
        ttk.Label(self.payment, text = "Payment Amount: ", font = ("Calibri 12")).grid(row=1, column=0, pady=10, sticky = tk.W)
        ttk.Entry(self.payment, textvariable = self.p_amount, width = 30).grid(row=1, column=1, pady=10, sticky = tk.W)
        
        ttk.Label(self.payment, text = "Payment Date: ", font = ("Calibri 12")).grid(row=2, column=0, pady=10, sticky = tk.W)
        self.p_date = DateEntry(self.payment, width = 20, date_pattern='yyyy-mm-dd',  
                             bg="darkblue",fg="white",  year = date.today().year)
        self.p_date.grid(row=2, column=1, sticky = tk.W)
        
    
    
    def create_payment_data(self):
        
        db = DatabaseUti()
        values = (self.email.get(), self.p_date.get(), self.p_amount.get())
        if "" in values:
            tk.messagebox.showerror('Warning!',
                                    "Please complete all the required information")
        else:
            status = db.insert_one_record("payments(email, payment_date, payment_amount)", values)
            
            if status == False:
                tk.messagebox.showerror('Error!',
                                        "This email address doesn't exist!")
            else:
                tk.messagebox.showinfo('Successful!',
                                       "The payment information has been successfully processing")
    

            self.email.set("")
            self.p_amount.set("")

class SearchFrame(ttk.Frame):
   def __init__(self, master):
       super().__init__(master)
       ttk.Label(self).pack()
       ttk.Label(self, text='Search Payment Page', font=("Bahnschrift", 16)).pack()


       self.table_view = ttk.Frame()
       self.table_view.pack()
       self.create_page()


       ttk.Button(self, text="Refund", command=self.issue_refund).pack(anchor=tk.W, pady=5)
       ttk.Button(self, text="Verify", command=self.verify_payment).pack(anchor=tk.W, pady=5)
       ttk.Button(self, text='Submit', command=self.process_camper_payments).pack(pady=10, anchor=tk.E)

   def create_page(self):
       # Search By Frame
       self.search_by_frame = ttk.LabelFrame(self, text='Search By')
       self.search_by_frame.pack(pady=5, expand=True)


       # contain the treeview!
       self.table_by_frame = ttk.Frame(self)
       self.table_by_frame.pack()


       menu_list = ['', 'email', 'payment_date', 'payment_amount']


       oMenuWidth = len(max(menu_list, key=len))


       self.clicked = tk.StringVar()
       self.clicked.set(menu_list[0])


       field_drop = ttk.OptionMenu(self.search_by_frame, self.clicked, *menu_list)
       field_drop.config(width=oMenuWidth)
       field_drop.grid(row=0, column=0)


       self.field_value = ttk.Entry(self.search_by_frame, width=30)
       self.field_value.grid(row=0, column=1)


       ttk.Button(self.search_by_frame, text="Search", command=self.show_payment_data).grid(row=0, column=2)


       # Table view - to display the search result
       columns = ("Transaction_id", 'Emai', "Payment Date", "Payment Amount")
       self.tree_view = ttk.Treeview(self.table_by_frame, show='headings',
                                     selectmode='browse', columns=columns)


       self.tree_view.column("Transaction_id", width=100, anchor='center')
       self.tree_view.heading("Transaction_id", text="Transaction_id")


       for item in columns[1:]:
           self.tree_view.column(item, width=130, anchor='center')
           self.tree_view.heading(item, text=item)


       self.tree_view.pack(side="left", fill=tk.BOTH, expand=True)


       # add a scrollbar
       scrollbar = ttk.Scrollbar(self.table_by_frame, orient=tk.VERTICAL, command=self.tree_view.yview)
       self.tree_view.configure(yscroll=scrollbar.set)
       scrollbar.pack(side="right", fill='y')

   def process_camper_payments(self):
       db = DatabaseUti()
       required_values = [self.Email.get(), self.PaymentDate.get_date(), self.PaymentAmount.get()]

       # Check if any required fields are empty
       if '' in required_values:
           tk.messagebox.showerror('Warning!',
                                   "Please complete all the required information")
       else:
           # Check if camper exists
           conditions = f"Email = '{self.Email.get()}' AND PaymentDate = '{self.PaymentDate.get_date()}' AND PaymentAmount = '{self.PaymentAmount.get()}'"
           result = db.query_table_with_condition("payments", "*", conditions)
           if result:
               tk.messagebox.showerror('Error!',
                                       "This Payment is already processed")
               self.clear_payment_data()
           else:
               # Insert new payment data into the table
               values = (None, self.Email.get(), self.PaymentDate.get_date(), self.PaymentAmount.get())
               status = db.insert_one_record("payments", values)
               if status == False:
                   tk.messagebox.showerror('Error!',
                                           "Failed to process Payment")
                   self.clear_payment_data()
               else:
                   tk.messagebox.showinfo('Successful!',
                                          "The Payment has been successfully processed")
                   self.clear_payment_data()

   def issue_refund(self):
       item = self.tree_view.selection()[0]
       values = self.tree_view.item(item, "values")
       transaction_id = values[0]
       email = values[1]
       p_amount = values[3]

       if messagebox.askyesno("Confirm", f"Do you want to refund {email} the amount of {p_amount}?"):
           db = DatabaseUti()
           db.update_payment_status(transaction_id, "Refunded")
           messagebox.showinfo("Success", "Refund Issued.")
           self.show_payment_data()

   def show_payment_data(self):
       # delete the old records!
       for _ in map(self.tree_view.delete, self.tree_view.get_children("")):
           pass


       db = DatabaseUti()


       field = self.clicked.get()
       field_value = self.field_value.get()


       if len(field_value) == 0:
           records = db.query_table("payments", "*")
           print(records)
           index = 0
           for record in records[::-1]:
               rowid = record[0]
               email = record[1]
               p_date = record[2]
               p_amount = record[3]
               self.tree_view.insert("", index + 1, values=(rowid, email, p_date, p_amount))


       else:
           conditions = field + "='" + field_value + "'"
           records =  db.query_table("payments", "*", conditions)
       if len(records) == 0:
           messagebox.showerror("Error", "No matching record found!")
       else:
           for record in records:
               rowid = record[0]
               email = record[1]
               p_date = record[2]
               p_amount = record[3]
               self.tree_view.insert("", "", values = (rowid, email, p_date, p_amount))

   def verify_payment(self, email):
       db = DatabaseUti()

       # check if there's any pending payment for this email
       records = db.query_table("payments", "*", f"email='{email}'")
       if len(records) > 0:
           messagebox.showwarning("Payment Pending", f"There's a pending payment for {email}!")
           return False

           # check if the latest payment is between 8 and 2 months before the camp start date
           records = db.query_table("payments", "*", f"email='{email}'", order_by="payment_date DESC", limit=1)
           if len(records) == 0:
               messagebox.showwarning("No Payment Found", f"No payment found for {email}!")
               return False

               latest_payment_date = datetime.strptime(records[0][2], '%Y-%m-%d')
               camp_start_date = datetime.strptime('2023-07-01', '%Y-%m-%d')
               delta = camp_start_date - latest_payment_date
               if delta.days < 60 or delta.days > 240:
                   messagebox.showwarning("Payment Not Timely",
                                          f"Payment for {email} was made on {latest_payment_date.date()}, "
                                          f"which is not between 8 and 2 months prior to the camp start date!")
                   return False

               # all checks passed
               return True


class DeleteFrame(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text = 'Delete Page', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()
        ttk.Label(self, text = "Waiting for future development!").pack()

class AboutFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text = 'About Page', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()
        ttk.Label(self, text = 'About Product: Created by Tkinter').pack()
        ttk.Label(self, text = 'About Author: Rachel Z').pack()
        ttk.Label(self, text = "All Rights Reserved for the use of UT ITM360").pack()

class AssignmentFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DatabaseUti()

        ttk.Label(self, text='Assignment Page', font=("Bahnschrift", 16)).pack()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tree_views = [None] * 6
        self.bunkhouse_tabs = [None] * 6

        for i in range(6):
            bunkhouse_id = i + 1
            self.bunkhouse_tabs[i] = ttk.Frame(self.notebook)
            self.notebook.add(self.bunkhouse_tabs[i], text=f"Bunkhouse {bunkhouse_id}")

            columns = ("CamperID", "FirstName", "LastName", "Gender", "Age")

            self.tree_views[i] = ttk.Treeview(self.bunkhouse_tabs[i], show='headings', selectmode='browse', columns=columns)

            for col in columns:
                self.tree_views[i].column(col, width=130, anchor='center')
                self.tree_views[i].heading(col, text=col)

            scrollbar_horizontal = ttk.Scrollbar(self.bunkhouse_tabs[i], orient=tk.HORIZONTAL, command=self.tree_views[i].xview)
            scrollbar_horizontal.pack(side="bottom", fill='x')

            scrollbar_vertical = ttk.Scrollbar(self.bunkhouse_tabs[i], orient=tk.VERTICAL, command=self.tree_views[i].yview)
            scrollbar_vertical.pack(side="right", fill='y')

            self.tree_views[i].configure(xscrollcommand=scrollbar_horizontal.set, yscrollcommand=scrollbar_vertical.set)
            self.tree_views[i].pack(side="left", fill=tk.BOTH, expand=True)

            self.load_bunkhouse_data(bunkhouse_id, self.tree_views[i])

        ttk.Button(self, text="Auto Assign Camper", command=self.auto_assign_camper).pack(pady=5)

    def load_bunkhouse_data(self, bunkhouse_id, tree_view):
        records = self.db.get_bunkhouse_assignments(bunkhouse_id)
        for record in records:
            age = self.calculate_age(record[3])
            tree_view.insert("", "end", values=(record[0], record[1], record[2], record[4], age))

    def auto_assign_camper(self):
        # Call the insert_camper_bunkhouse method to auto-assign campers
        self.db.insert_camper_bunkhouse()

        # Refresh the bunkhouse data displayed in the tree views
        for i in range(6):
            bunkhouse_id = i + 1
            self.tree_views[i].delete(*self.tree_views[i].get_children())
            self.load_bunkhouse_data(bunkhouse_id, self.tree_views[i])

    def calculate_age(self, birthdate):
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

