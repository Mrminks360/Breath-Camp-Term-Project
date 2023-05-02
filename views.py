import tkinter as tk
from tkinter import ttk, messagebox
from db import DatabaseUti
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime
from collections import defaultdict

import tkinter as tk

class ManageFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        ttk.Label(self, text='Camper Management', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()

        # Create the search table
        self.checkin_frame = CheckinFrame(self)
        self.checkin_frame.pack()

        # Create the notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True)

        # Create the tabs
        self.register_tab = RegisterCamper(self.notebook)
        self.update_tab = UpdateCamper(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.register_tab, text='Register', )
        self.notebook.add(self.update_tab, text='Update')

class RegisterCamper(ttk.Frame):

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
                # Check if there are available slots for the new camper
                if db.check_availability(self.ArrivalDate.get_date(), self.DepartureDate.get_date(), self.Gender.get()):
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
                else:
                    tk.messagebox.showerror('Error!',
                                            "No available slots for the selected dates")
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

class UpdateCamper(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text='Camper Information', font=("Bahnschrift", 16)).pack()
        
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
        self.CamperID = tk.StringVar()
        self.AcceptanceNotice = tk.BooleanVar()
        self.IsCancelled = tk.BooleanVar()

        self.create_page()
        ttk.Button(self, text='Submit', command=self.update_camper_data).pack(side="right", pady=10, padx=5,
                                                                              anchor=tk.E)
        ttk.Button(self, text='Clear', command=self.clear_create_data).pack(side="right", pady=10, padx=5, anchor=tk.E)

    def create_page(self):
        self.info = ttk.Frame(self)
        self.info.pack()

        ttk.Label(self.info, text='Camper ID(*): ', font=("Calibri 12")).grid(row=0, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.CamperID, width=20).grid(row=0, column=1, pady=5, sticky=tk.W)
        
        # First row
        ttk.Label(self.info, text='First Name: ', font=("Calibri 12")).grid(row=1, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.FirstName, width=20).grid(row=1, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Last Name: ', font=("Calibri 12")).grid(row=1, column=2, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.LastName, width=20).grid(row=1, column=3, pady=5, sticky=tk.W)

        # Second Row
        # gender menu list
        ttk.Label(self.info, text='Gender: ', font=("Calibri 12")).grid(row=2, column=0, pady=5, sticky=tk.W)
        menu_list = ['', 'Female', 'Male']

        self.Gender.set(menu_list[0])
        field_drop = ttk.OptionMenu(self.info, self.Gender, *menu_list)
        field_drop.config(width=15)
        field_drop.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.info, text='Birthday: ', font=("Calibri 12")).grid(row=2, column=2, pady=5, sticky=tk.W)
        self.Birthday = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                                bg="darkblue", fg="white",
                                year=date.today().year, top_level=self.winfo_toplevel())
        self.Birthday.delete(0, "end")
        self.Birthday.grid(row=2, column=3, sticky=tk.W)

        # Third Row

        ttk.Label(self.info, text='Arrival Date: ', font=("Calibri 12")).grid(row=3, column=0, pady=5, sticky=tk.W)
        self.ArrivalDate = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                                    bg="darkblue", fg="white",
                                    year=date.today().year, top_level=self.winfo_toplevel())
        self.ArrivalDate.delete(0, "end")
        self.ArrivalDate.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(self.info, text='Departure Date: ', font=("Calibri 12")).grid(row=3, column=2, pady=5, sticky=tk.W)
        self.DepartureDate = DateEntry(self.info, width=20, date_pattern='yyyy-mm-dd',
                                        bg="darkblue", fg="white",
                                        year=date.today().year, top_level=self.winfo_toplevel())
        self.DepartureDate.delete(0, "end")
        self.DepartureDate.grid(row=3, column=3, sticky=tk.W)

        # Fourth Row

        ttk.Label(self.info, text='Mailing Address: ', font=("Calibri 12")).grid(row=4, column=0, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.MailingAddress, width=20).grid(row=4, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Friends: ', font=("Calibri 12")).grid(row=4, column=2, pady=5, sticky=tk.W)
        ttk.Entry(self.info, textvariable=self.Friends, width=20).grid(row=4, column=3, pady=5, sticky=tk.W)

        # Fifth Row

        ttk.Label(self.info, text='Forms: ', font=("Calibri 12")).grid(row=5, column=0, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.CompletedForm, onvalue=True, offvalue=False).grid(row=5, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Equipment: ', font=("Calibri 12")).grid(row=5, column=2, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.Equipment, onvalue=True, offvalue=False).grid(row=5, column=3, pady=5, sticky=tk.W)

        # Sixth Row
        ttk.Label(self.info, text='Check-In: ', font=("Calibri 12")).grid(row=6, column=0, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.CheckedIn, onvalue=True, offvalue=False).grid(row=6, column=1, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Acceptance Notice: ', font=("Calibri 12")).grid(row=6, column=2, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.AcceptanceNotice, onvalue=True, offvalue=False).grid(row=6, column=3, pady=5, sticky=tk.W)

        ttk.Label(self.info, text='Cancel: ', font=("Calibri 12")).grid(row=0, column=2, pady=5, sticky=tk.W)
        ttk.Checkbutton(self.info, variable=self.IsCancelled, onvalue=True, offvalue=False).grid(row=0, column=3, pady=5, sticky=tk.W)

        def populate_fields(self):
            db = DatabaseUti()
            camper_id = self.CamperID.get()

            if not camper_id:
                tk.messagebox.showerror('Warning!', "Please enter a Camper ID")
                return

            result = db.query_table_with_condition("camper", "*", f"CamperID = {camper_id}")
            if not result:
                tk.messagebox.showerror('Error!', "Camper not found")
                return

            camper_data = result[0]

    def update_camper_data(self):
        db = DatabaseUti()
        camper_id = self.CamperID.get()

        if not camper_id:
            tk.messagebox.showerror('Warning!', "Please enter a Camper ID")
            return

        # Get the updated values from form fields
        kwargs = {}

        if self.FirstName.get():
            kwargs["FirstName"] = self.FirstName.get()
        if self.LastName.get():
            kwargs["LastName"] = self.LastName.get()
        if self.Birthday.get_date():
            kwargs["Birthday"] = self.Birthday.get_date()
        if self.Gender.get():
            kwargs["Gender"] = self.Gender.get()
        if self.ArrivalDate.get_date():
            kwargs["ArrivalDate"] = self.ArrivalDate.get_date()
        if self.Equipment.get():
            kwargs["Equipment"] = self.Equipment.get()
        if self.DepartureDate.get_date():
            kwargs["DepartureDate"] = self.DepartureDate.get_date()
        if self.CompletedForm.get():
            kwargs["CompletedForm"] = self.CompletedForm.get()
        if self.CheckedIn.get():
            kwargs["CheckedIn"] = self.CheckedIn.get()
        if self.MailingAddress.get():
            kwargs["MailingAddress"] = self.MailingAddress.get()
        if self.Friends.get():
            kwargs["Friends"] = self.Friends.get()
        if self.AcceptanceNotice.get() is not None:
            kwargs["AcceptedNotice"] = self.AcceptanceNotice.get()
            if self.AcceptanceNotice.get():
                kwargs["AcceptedNoticeDate"] = date.today().strftime("%Y-%m-%d")
            else:
                kwargs["AcceptedNoticeDate"] = None
        if self.IsCancelled.get() is not None:
            kwargs["IsCancelled"] = self.IsCancelled.get()
            if self.IsCancelled.get():
                kwargs["CancellationDate"] = date.today().strftime("%Y-%m-%d")
                kwargs["RefundPercentage"] = self.calculate_refund(kwargs["AcceptedNoticeDate"],
                                                                   kwargs["CancellationDate"])
            else:
                kwargs["CancellationDate"] = None
                kwargs["RefundPercentage"] = None

        status = db.update_camper_checkin(camper_id, **kwargs)
        if status == False:
            tk.messagebox.showerror('Error!', "Failed to update Camper")
            self.clear_create_data()
        else:
            tk.messagebox.showinfo('Successful!', "The Camper has been successfully updated")
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
        self.AcceptanceNotice.set(False)

    def calculate_refund(self, accept_date, cancel_date):
        if not accept_date:
            return 0.9
        else:
            accept_year = int(accept_date[0:4])
            accept_month = int(accept_date[5:7])
            accept_day = int(accept_date[8:10])
            cancel_year = int(cancel_date[0:4])
            cancel_month = int(cancel_date[5:7])
            cancel_day = int(cancel_date[8:10])
            accept = date(accept_year, accept_month, accept_day)
            cancel = date(cancel_year, cancel_month, cancel_day)

            result = (cancel - accept).days//7

            if result <= 3:
                return 0.9
            elif result <= 6:
                return 0.45
            else:
                return 0

class CheckinFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

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

        menu_list = ['', 'FirstName', 'LastName', 'Birthday', 'Gender', 'ArrivalDate', 'Equipment',
                     'DepartureDate', 'CompletedForm', 'CheckedIn', 'MailingAddress', 'Friends',
                     'AcceptedNotice', 'AcceptedNoticeDate', 'IsCancelled', 'CancellationDate', 'RefundPercentage']

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
        columns = ("CamperID", 'FirstName', 'LastName', 'Birthday', 'Gender', 'ArrivalDate', 'Equipment',
                   'DepartureDate', 'CompletedForm', 'CheckedIn', 'MailingAddress', 'Friends', 'AcceptedNotice',
                   'AcceptedNoticeDate', 'IsCancelled', 'CancellationDate', 'RefundPercentage')

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

class AcceptanceNoticeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.db = DatabaseUti()

        # Create a canvas to hold the table
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Create a frame to hold the table's rows
        self.table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor='nw')

        self.populate_table()

    def populate_table(self):
        unnotified_campers = self.db.get_unnotified_campers()

        for index, camper in enumerate(unnotified_campers):
            self.create_table_row(index, camper)

    def create_table_row(self, index, camper):
        # Create camper data labels and entries
        id_label = tk.Label(self.table_frame, text=camper[0], width=5)
        first_name_entry = tk.Entry(self.table_frame, width=15)
        last_name_entry = tk.Entry(self.table_frame, width=15)
        mailing_address_entry = tk.Entry(self.table_frame, width=30)

        first_name_entry.insert(0, camper[1])
        last_name_entry.insert(0, camper[2])
        mailing_address_entry.insert(0, camper[3])

        # Create "Sent" button
        sent_button = tk.Button(self.table_frame, text="Send", command=lambda camper_id=camper[0], row_index=index: self.send_acceptance_notice(camper_id, row_index))

        # Place widgets in the table frame
        id_label.grid(row=index, column=0, padx=5, pady=5)
        first_name_entry.grid(row=index, column=1, padx=5, pady=5)
        last_name_entry.grid(row=index, column=2, padx=5, pady=5)
        mailing_address_entry.grid(row=index, column=3, padx=5, pady=5)
        sent_button.grid(row=index, column=4, padx=5, pady=5)

    def send_acceptance_notice(self, camper_id, row_index):
        self.db.update_acceptance_notice(camper_id, True, date.today().strftime("%Y-%m-%d"))
        messagebox.showinfo("Success", "Acceptance notice sent.")
        self.remove_table_row(row_index)
        self.refresh_table()

    def refresh_table(self):
        for widget in self.table_frame.grid_slaves():
            widget.destroy()

        self.populate_table()

    def remove_table_row(self, row_index):
        for widget in self.table_frame.grid_slaves(row=row_index):
            widget.destroy()

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

        ttk.Button(self, text="Refresh", command=self.show_payment_data).pack(anchor=tk.E, pady=5)

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
        columns = ("Transaction_id", 'Email', "Payment Date", "Payment Amount")
        self.tree_view = ttk.Treeview(self.table_by_frame, show='headings',
                                      selectmode='browse', columns=columns)

        self.tree_view.column("Transaction_id", width=100, anchor='center')
        self.tree_view.heading("Transaction_id", text="Transaction_id")

        for item in columns[1:]:
            self.tree_view.column(item, width=130, anchor='center')
            self.tree_view.heading(item, text=item)

        self.tree_view.pack(side = "left", fill=tk.BOTH, expand=True)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.table_by_frame, orient=tk.VERTICAL, command=self.tree_view.yview)
        self.tree_view.configure(yscroll=scrollbar.set)
        scrollbar.pack(side= "right", fill ='y')

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
            records = db.query_table_with_condition("payments", "*", conditions)
            if records == False:
                tk.messagebox.showerror('Warning!',
                                        "This record doesn't exist!")
            else:
                index = 0
                for record in records[::-1]:
                    rowid = record[0]
                    email = record[1]
                    p_date = record[2]
                    p_amount = record[3]
                    print(record)
                    self.tree_view.insert("", index + 1, values=(rowid, email, p_date, p_amount))


class AboutFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self).pack()
        ttk.Label(self, text = 'About Page', font=("Bahnschrift", 16)).pack()
        ttk.Label(self).pack()
        ttk.Label(self, text = 'About Product: Created by Tkinter').pack()
        ttk.Label(self, text = 'About Authors: Maison Anderson, Santiago Londono, Andrew Minkswinberg, and Jamal Warren-March').pack()
        ttk.Label(self, text = "All Rights Reserved for the use of UT ITM360").pack()
        #self.image = tk.PhotoImage(file=r"C:\Users\SantiagoLondono\Documents\GitHub\Breath-Camp-Term-Project\CatCrying.jpg")
        #ttk.Label(self, image=self.image).pack()

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


class TribeFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = DatabaseUti()

        ttk.Label(self, text='Tribe Assignment Page', font=("Bahnschrift", 16)).pack()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tree_views = [None] * 6
        self.tribe_tabs = [None] * 6
        tribe_names = ["Torchbearers", "Firestarters", "Island Pioneers", "Marooned Marvels", "Castaway Conquerors", "Expedition Explorers"]

        for i in range(6):
            tribe_id = tribe_names[i]
            self.tribe_tabs[i] = ttk.Frame(self.notebook)
            self.notebook.add(self.tribe_tabs[i], text=f"{tribe_id}")

            columns = ("CamperID", "FirstName", "LastName", "Gender", "Age", "Friends")

            self.tree_views[i] = ttk.Treeview(self.tribe_tabs[i], show='headings', selectmode='browse', columns=columns)

            for col in columns:
                self.tree_views[i].column(col, width=130, anchor='center')
                self.tree_views[i].heading(col, text=col)

            scrollbar_horizontal = ttk.Scrollbar(self.tribe_tabs[i], orient=tk.HORIZONTAL,
                                                 command=self.tree_views[i].xview)
            scrollbar_horizontal.pack(side="bottom", fill='x')

            scrollbar_vertical = ttk.Scrollbar(self.tribe_tabs[i], orient=tk.VERTICAL, command=self.tree_views[i].yview)
            scrollbar_vertical.pack(side="right", fill='y')

            self.tree_views[i].configure(xscrollcommand=scrollbar_horizontal.set, yscrollcommand=scrollbar_vertical.set)
            self.tree_views[i].pack(side="left", fill=tk.BOTH, expand=True)

            self.load_tribe_data(tribe_id, self.tree_views[i])

        ttk.Button(self, text="Auto Assign Camper", command=self.aggin_campers).pack(pady=5)

    def load_tribe_data(self, tribe_id, tree_view):
        records = self.db.get_tribe_assignments(tribe_id)
        for record in records:
            age = self.get_camper_age(record[3])
            tree_view.insert("", "end", values=(record[0], record[1], record[2], record[4], age))

    def aggin_campers(self):
        self.db.insert_camper_tribe()
        for i in range(6):
            tribe_id = i + 1
            self.tree_views[i].delete(*self.tree_views[i].get_children())
            self.load_tribe_data(tribe_id, self.tree_views[i])

    def get_camper_age(self, birthdate):
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
