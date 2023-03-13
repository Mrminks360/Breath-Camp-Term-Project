# -*- coding: utf-8 -*-
"""
ITM 360: Advanced Application Development

Project: Customer Relationship Management System

Author: Rachel Z (hzhang@ut.edu)
"""

import tkinter as tk
from tkinter import ttk
from views import AboutFrame, CreateFrame, SearchFrame, UpdateFrame, DeleteFrame, PaymentFrame
from styles import TTK_THEME, COLOR_THEME

class MainPage:
    def __init__(self, master):

        self.master = master
        self.master.geometry("600x420")
        self.master.title("ITM360 CMS - Customer Management System  v1.0.0")
        # initialize the page
        self.create_page()

    def navigation_bar(self):
        # apply the ttk style
        self.style = ttk.Style(self.master)
        self.style.configure("nav.TFrame", background=TTK_THEME['nav.TFrame']['background'])
        self.style.configure("Heading.TLabel", font=TTK_THEME['Heading.TLabel']['font'],
                             foreground=TTK_THEME['Heading.TLabel']['foreground'])

        # top Navigation bar:
        self.topFrame = ttk.Frame(self.master, style="nav.TFrame")
        self.topFrame.pack(side="top", fill=tk.X)

        # Navigation bar
        # Header label text:
        tk.Label(self.topFrame, text="  ", font="Bahnschrift 10", bg=COLOR_THEME['main'], fg=COLOR_THEME['text'],
                 height=2, padx=20).pack(side="right")

        # Navbar button:
        text_command = (('Create', self.show_create), ('Update', self.show_update),
                        ('Payment', self.show_payment), ('Search', self.show_search),
                        ('Delete', self.show_delete), ("About", self.show_about))
        for i in range(len(text_command)):
            tk.Button(self.topFrame, text=text_command[i][0], font="Bahnschrift 10", fg=COLOR_THEME['text'],
                  bg=COLOR_THEME['main'], activebackground=COLOR_THEME['light'],
                  bd=0, padx=20,
                  command=text_command[i][1]).pack(side="left")


    def create_page(self):
        self.navigation_bar()
        self.create_frame = CreateFrame(self.master)
        self.update_frame = UpdateFrame(self.master)
        self.payment_frame = PaymentFrame(self.master)
        self.search_frame = SearchFrame(self.master)
        self.delete_frame = DeleteFrame(self.master)
        self.about_frame = AboutFrame(self.master)

    def show_about(self):
        self.create_frame.pack_forget()
        self.update_frame.pack_forget()
        self.payment_frame.pack_forget()
        self.search_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.about_frame.pack()


    def show_create(self):
        self.create_frame.pack()
        self.search_frame.pack_forget()
        self.update_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.about_frame.pack_forget()
        self.payment_frame.pack_forget()
        

    def show_update(self):
        self.create_frame.pack_forget()
        self.search_frame.pack_forget()
        self.update_frame.pack()
        self.delete_frame.pack_forget()
        self.about_frame.pack_forget()
        self.payment_frame.pack_forget()
    
 
    def show_payment(self):
        self.create_frame.pack_forget()
        self.search_frame.pack_forget()
        self.update_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.about_frame.pack_forget()
        self.payment_frame.pack()
        
        
    def show_search(self):
        self.create_frame.pack_forget()
        self.search_frame.pack()
        self.update_frame.pack_forget()
        self.delete_frame.pack_forget()
        self.about_frame.pack_forget()
        self.payment_frame.pack_forget()

    
    def show_delete(self):
        self.create_frame.pack_forget()
        self.search_frame.pack_forget()
        self.update_frame.pack_forget()
        self.delete_frame.pack()
        self.about_frame.pack_forget()
        self.payment_frame.pack_forget()


if __name__ == '__main__':
    root = tk.Tk()
    MainPage(root)
    root.mainloop()
