import random
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
import re
class BMI:
    def __init__(self, master):
        self.master = master
        self.master.geometry('600x400')
        self.master.title('BMI Calculator')
        self.weight = tk.StringVar()
        self.height = tk.StringVar()
        self.result = 0
        self.output = tk.StringVar()
        self.bmi_category = ''
        self.bmi_category_output = tk.StringVar()
        self.system = tk.IntVar()
        self.unitw = tk.StringVar()
        self.unith = tk.StringVar()
        self.unitw.set('Enter your weight (Kg)')
        self.unith.set('Enter your height (Cm)')
#test



        # Frame 1

        self.frame = ttk.LabelFrame(self.master, text='Please enter your number.')
        self.frame.pack(pady=10, padx=10)

        ttk.Label(self.frame, textvariable= self.unitw).grid(row=0, column=0, padx=10, pady=2)
        ttk.Entry(self.frame, textvariable=self.weight).grid(row=0, column=1, padx=10, pady=2)

        ttk.Label(self.frame, textvariable= self.unith).grid(row=1, column=0, padx=10, pady=2)
        ttk.Entry(self.frame, textvariable=self.height).grid(row=1, column=1, padx=10, pady=2)

        # Frame 2
        self.frame = ttk.LabelFrame(self.master, text='Make your selection')
        self.frame.pack(pady=10, padx=10)

        ttk.Button(self.frame, text='Check BMI', command=self.click).grid(row=0, column=0, padx=10, pady=2)
        ttk.Button(self.frame, text='Clear', command=self.reset).grid(row=0, column=1, padx=10, pady=2)
        ttk.Button(self.frame, text='Exit', command=self.master.destroy).grid(row=0, column=3, padx=10, pady=2)
        ttk.Button(self.frame, text='Change system', command=self.changesys).grid(row=0, column=2, padx=10, pady=2)

        # Frame 3
        self.frame = ttk.LabelFrame(self.master, text='Result')
        self.frame.pack(pady=10, padx=10)

        tk.Label(self.frame, textvariable=self.output, font=('Cambria', 20), width=30).pack(pady=10)
        tk.Label(self.frame, textvariable=self.bmi_category_output, font=('Cambria', 20), width=30).pack(pady=10)

    def bmi_calc(self):
        if self.system.get() == 0:
            return round((float(self.weight.get()) / float(self.height.get()) / float(self.height.get())) * 10000, 2)
        elif self.system.get() == 1:
            return round((float(self.weight.get()) / float(self.height.get()) / float(self.height.get())) * 703, 2)

    def bmi_category_set(self):
        if self.result <= 18.5:
            self.bmi_category = "Underweight"
        elif self.result < 25:
            self.bmi_category = "Normal"
        elif self.result < 30:
            self.bmi_category = "Overweight"
        else:
            self.bmi_category = "Obese"

    def click(self):
        numberw = self.weight.get()
        numberh = self.height.get()
        if len(numberw) == 0 or len(numberh) == 0:
            messagebox.showerror('Error', 'Please enter a Number.')

        elif not re.match("^[0-9]*\.?[0-9]+$", numberh) or not re.match("^[0-9]*\.?[0-9]+$", numberw):
            messagebox.showerror('Error', 'Please enter a Number.')


        else:
            self.result = self.bmi_calc()
            self.bmi_category_set()
            self.output.set('Your BMI is ' + str(self.bmi_calc()))
            self.bmi_category_output.set('Category: ' + str(self.bmi_category))

    def reset(self):
        self.height.set('')
        self.weight.set('')
        self.output.set('')
        self.bmi_category_output.set('')

    def changesys(self):
        if self.system.get() == 0:
            self.system.set(1)
            self.unitw.set('Enter your weight (Lbs)')
            self.unith.set('Enter your height (In)')
        elif self.system.get() == 1:
            self.system.set(0)
            self.unitw.set('Enter your weight (Kg)')
            self.unith.set('Enter your height (Cm)')
if __name__ == '__main__':
    root = tk.Tk()
    app = BMI(root)
    root.mainloop()
