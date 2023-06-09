import tkinter as tk
from tkinter import ttk
from views import AboutFrame, ManageFrame, PaymentFrame, AcceptanceNoticeFrame, CheckinFrame, AssignmentFrame, TribeFrame
from styles import TTK_THEME, COLOR_THEME


class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1700x900")
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
        self.manage_frame = ManageFrame(self.notebook)
        self.notebook.add(self.manage_frame, text="Camper Management")

        self.acceptance_notice_frame = AcceptanceNoticeFrame(self.notebook)
        self.notebook.add(self.acceptance_notice_frame, text="Acceptance Notice")

        self.assignment_frame = AssignmentFrame(self.notebook)
        self.notebook.add(self.assignment_frame, text="Bunkhouse Assignment")

        self.tribe_frame = TribeFrame(self.notebook)
        self.notebook.add(self.tribe_frame, text="Tribe Assignment")

        self.payment_frame = PaymentFrame(self.notebook)
        self.notebook.add(self.payment_frame, text="Payment")

        self.about_frame = AboutFrame(self.notebook)
        self.notebook.add(self.about_frame, text="About")


if __name__ == '__main__':
    root = tk.Tk()
    app = MainPage(root)
    root.mainloop()