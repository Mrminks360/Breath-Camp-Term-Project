
"""
ITM 360: Advanced Application Development

Project: Gila breath Camp Application

Author: Andrew MinksWinberg jjj
"""

import tkinter as tk
from tkinter import ttk
from views import AboutFrame, RegistrationFrame, SearchFrame, UpdateFrame, DeleteFrame, PaymentFrame,CheckinFrame, AssignmentFrame
from styles import TTK_THEME, COLOR_THEME


class MainPage:
    def __init__(self, master):

        self.master = master
        self.master.geometry("900x500")
        self.master.title("ITM360  - Gila Breath Camp  v1.0.0")
        
        # initialize the page
        self.create_page()

    def create_page(self):
        # apply the ttk style
        self.style = ttk.Style(self.master)
        self.style.configure("nav.TFrame", background=TTK_THEME['nav.TFrame']['background'])
        self.style.configure("Heading.TLabel", font=TTK_THEME['Heading.TLabel']['font'],
                             foreground=TTK_THEME['Heading.TLabel']['foreground'])
        
        # create a notebook widget
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True)
        
        # create the frames for each tab
        self.registration_frame = RegistrationFrame(self.notebook)
        self.notebook.add(self.registration_frame, text="Registration")

        self.checkin_frame = CheckinFrame(self.notebook)
        self.notebook.add(self.checkin_frame, text="Check-In")

        self.assignment_frame = AssignmentFrame(self.notebook)
        self.notebook.add(self.assignment_frame, text="Assignment")

        self.payment_frame = SearchFrame(self.notebook)
        self.notebook.add(self.payment_frame, text="Payment")

        self.cancellation_frame = DeleteFrame(self.notebook)
        self.notebook.add(self.cancellation_frame, text="Cancellation")

        self.about_frame = AboutFrame(self.notebook)
        self.notebook.add(self.about_frame, text="About")

        
if __name__ == '__main__':
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()