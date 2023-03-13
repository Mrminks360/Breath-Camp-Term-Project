# -*- coding: utf-8 -*-
"""
ITM 360: Advanced Application Development

Project: Customer Management System

Author: Rachel Z (hzhang@ut.edu)
"""


import tkinter as tk
from tkinter import ttk, messagebox
from db import DatabaseUti
from mainpage import MainPage

class LoginPage:
    
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x180")
        self.master.title("ITM360 CMS - Login")
        
        # variable
        self.username = tk.StringVar()
        self.password = tk.StringVar()
    
    
        
        self.page = ttk.Frame(self.master)
        self.page.pack()
        
        
        ttk.Label(self.page).grid(row=0, column = 0)
        
        ttk.Label(self.page, text = 'Username: ').grid(row=1, column = 1)
        ttk.Entry(self.page, textvariable = self.username).grid(row = 1, column = 2)
        
        ttk.Label(self.page, text = "Password: ").grid(row=2, column = 1, pady = 10)
        ttk.Entry(self.page, textvariable = self.password, show= '*').grid(row = 2, column = 2)
        
        ttk.Button(self.page, text= 'Login', command = self.login_btn).grid(row = 3, column=1, pady = 10)
        ttk.Button(self.page, text = 'Exit', command = self.master.destroy).grid(row = 3, column = 2)
        


    def login_btn(self):
        #if self.username.get() == "admin" and self.password.get() == "1234":
         #   print("login successful!")     # until not talking about the datamodel
         
        db = DatabaseUti()
        if db.check_login(self.username.get(), self.password.get()) == True:
            messagebox.showinfo(title = "Successful",
                                   message = "Login Successful!")
            
        # Go to the main page
            self.page.destroy()
            MainPage(self.master)
         
        else:
            messagebox.showwarning(title = 'Alert',
                                   message = "Login failure. \nPlease try again")
            self.username.set("")
            self.password.set("")



if __name__ == "__main__":

    root = tk.Tk()
    
    # need the azure.tcl file to set the theme
    #root.tk.call("source", "azure.tcl")
    #root.tk.call("set_theme", "light")
    LoginPage(root)
    root.mainloop()
