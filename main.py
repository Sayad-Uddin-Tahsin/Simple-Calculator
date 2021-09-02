import tkinter as tk
from tkinter import *
import tkinter.messagebox
import time
import os
import math

calculator_version = "Calculator v1.1"

LARGE_FONT_STYLE = ("Arial", 28, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

path = os.path.abspath(os.getcwd())
calculator_icon = path + "\Icons\Calculator.ico"
about_icon = path + "\Icons\Info.ico"
s_Calculator = path + "\Icons\Scientific Calculator.ico"


def check_for_update():
    updator = tk.Tk()
    updator.title("Calculator by Tahsin Updater")
    updator.wm_iconbitmap(about_icon)
    updator.geometry("400x120")
    updator.resizable(0, 0)

    lbl1 = Label(updator, text="Checking for Updates...", font=('Arial', 20))
    lbl1.place(x=50, y=30)


def about():
    about = tk.Tk()
    about.title("About")
    about.wm_iconbitmap(about_icon)
    about.geometry("320x120")
    about.resizable(0, 0)

    lbl1 = Label(about, text="About", font=('Arial', 20))
    year = time.strftime("%Y")
    if "2021" < year:
        lbl2 = Label(about, text=calculator_version + "\n\n© 2021 - " + year + " Tahsin. All Rights Reserved",
                     justify=LEFT, font=('Arial', 12))
    else:
        lbl2 = Label(about, text=calculator_version + "\n\n© 2021 Tahsin. All Rights Reserved", justify=LEFT,
                     font=('Arial', 12))

    lbl1.place(x=10)
    lbl2.place(x=10, y=40)


class Standard_Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("320x478")
        self.window.resizable(0, 0)
        self.window.title("Calculator by Tahsin")
        self.window.iconbitmap(calculator_icon)

        menubar1 = Menu(self.window)

        self.window.config(menu=menubar1)
        self.fileMenu = Menu(menubar1, tearoff=0)
        self.fileMenu.add_command(label="Scientific Calculator",
                                  command=lambda: [self.window.destroy(), Scientific_Calculator()])
        menubar1.add_cascade(label="Options", menu=self.fileMenu)

        self.fileMenu = Menu(menubar1, tearoff=0)
        self.fileMenu.add_command(label="About", command=about)
        menubar1.add_cascade(label="More", menu=self.fileMenu)

        # self.fileMenu = Menu(menubar1, tearoff=0)
        # self.fileMenu.add_command(label="Check for Update", command=check_for_update)
        # menubar1.add_cascade(label="Update", menu=self.fileMenu)

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()


def Scientific_Calculator():
    root = Tk()
    root.geometry("650x400+300+300")
    root.iconbitmap(s_Calculator)
    root.title("Scientific Calculator By Tahsin")
    root.resizable(0, 0)

    switch = None

    def btn1_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '1')

    def btn2_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '2')

    def btn3_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '3')

    def btn4_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '4')

    def btn5_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '5')

    def btn6_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '6')

    def btn7_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '7')

    def btn8_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '8')

    def btn9_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '9')

    def btn0_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, '0')

    def key_event(*args):
        if disp.get() == '0':
            disp.delete(0, END)

    def btnp_clicked():
        pos = len(disp.get())
        disp.insert(pos, '+')

    def btnm_clicked():
        pos = len(disp.get())
        disp.insert(pos, '-')

    def btnml_clicked():
        pos = len(disp.get())
        disp.insert(pos, '*')

    def btnd_clicked():
        pos = len(disp.get())
        disp.insert(pos, '/')

    def btnc_clicked(*args):
        disp.delete(0, END)
        disp.insert(0, '0')

    def sin_clicked():
        try:
            ans = float(disp.get())
            if switch is True:
                ans = math.sin(math.radians(ans))
            else:
                ans = math.sin(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def cos_clicked():
        try:
            ans = float(disp.get())
            if switch is True:
                ans = math.cos(math.radians(ans))
            else:
                ans = math.cos(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def tan_clicked():
        try:
            ans = float(disp.get())
            if switch is True:
                ans = math.tan(math.radians(ans))
            else:
                ans = math.tan(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def arcsin_clicked():
        try:
            ans = float(disp.get())
            if switch is True:
                ans = math.degrees(math.asin(ans))
            else:
                ans = math.asin(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def arccos_clicked():
        try:
            ans = float(disp.get())
            if switch is True:
                ans = math.degrees(math.acos(ans))
            else:
                ans = math.acos(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def arctan_clicked():
        try:
            ans = float(disp.get())
            if switch is True:
                ans = math.degrees(math.atan(ans))
            else:
                ans = math.atan(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def pow_clicked():
        pos = len(disp.get())
        disp.insert(pos, '**')

    def round_clicked():
        try:
            ans = float(disp.get())
            ans = round(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def logarithm_clicked():
        try:
            ans = float(disp.get())
            ans = math.log10(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def fact_clicked():
        try:
            ans = float(disp.get())
            ans = math.factorial(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def sqr_clicked():
        try:
            ans = float(disp.get())
            ans = math.sqrt(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def dot_clicked():
        pos = len(disp.get())
        disp.insert(pos, '.')

    def pi_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, str(math.pi))

    def e_clicked():
        if disp.get() == '0':
            disp.delete(0, END)
        pos = len(disp.get())
        disp.insert(pos, str(math.e))

    def bl_clicked():
        pos = len(disp.get())
        disp.insert(pos, '(')

    def br_clicked():
        pos = len(disp.get())
        disp.insert(pos, ')')

    def del_clicked():
        pos = len(disp.get())
        display = str(disp.get())
        if display == '':
            disp.insert(0, '0')
        elif display == ' ':
            disp.insert(0, '0')
        elif display == '0':
            pass
        else:
            disp.delete(0, END)
            disp.insert(0, display[0:pos - 1])

    def conv_clicked():
        global switch
        if switch is None:
            switch = True
            conv_btn['text'] = "Deg"
        else:
            switch = None
            conv_btn['text'] = "Rad"

    def ln_clicked():
        try:
            ans = float(disp.get())
            ans = math.log(ans)
            disp.delete(0, END)
            disp.insert(0, str(ans))
        except Exception:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    def mod_clicked():
        pos = len(disp.get())
        disp.insert(pos, '%')

    def btneq_clicked():
        try:
            ans = disp.get()
            ans = eval(ans)
            disp.delete(0, END)
            disp.insert(0, ans)

        except:
            tkinter.messagebox.showerror("Value Error", "Check your values and operators")

    data = StringVar()

    disp = Entry(root, font="Verdana 20", fg="#25265E", bg="#F5F5F5", bd=0, justify=RIGHT,
                 insertbackground="#abbab1",
                 cursor="arrow")
    disp.bind("<Return>", btneq_clicked)
    disp.bind("<Escape>", btnc_clicked)
    disp.bind("<Key-1>", key_event)
    disp.bind("<Key-2>", key_event)
    disp.bind("<Key-3>", key_event)
    disp.bind("<Key-4>", key_event)
    disp.bind("<Key-5>", key_event)
    disp.bind("<Key-6>", key_event)
    disp.bind("<Key-7>", key_event)
    disp.bind("<Key-8>", key_event)
    disp.bind("<Key-9>", key_event)
    disp.bind("<Key-0>", key_event)
    disp.bind("<Key-.>", key_event)
    disp.insert(0, '0')
    disp.focus_set()
    disp.pack(expand=TRUE, fill=BOTH)

    # Row 1 Buttons

    btnrow1 = Frame(root, bg="#000000")
    btnrow1.pack(expand=TRUE, fill=BOTH)

    pi_btn = Button(btnrow1, text="π", font="Segoe 18", relief=GROOVE, bd=0, command=pi_clicked, fg="#25265E",
                    bg="#F8FAFF")
    pi_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    fact_btn = Button(btnrow1, text=" x! ", font="Segoe 18", relief=GROOVE, bd=0, command=fact_clicked,
                      fg="#25265E",
                      bg="#F8FAFF")
    fact_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    sin_btn = Button(btnrow1, text="sin", font="Segoe 18", relief=GROOVE, bd=0, command=sin_clicked, fg="#25265E",
                     bg="#F8FAFF")
    sin_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    cos_btn = Button(btnrow1, text="cos", font="Segoe 18", relief=GROOVE, bd=0, command=cos_clicked, fg="#25265E",
                     bg="#F8FAFF")
    cos_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    tan_btn = Button(btnrow1, text="tan", font="Segoe 18", relief=GROOVE, bd=0, command=tan_clicked, fg="#25265E",
                     bg="#F8FAFF")
    tan_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn1 = Button(btnrow1, text="1", font="Segoe 23", relief=GROOVE, bd=0, command=btn1_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn1.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn2 = Button(btnrow1, text="2", font="Segoe 23", relief=GROOVE, bd=0, command=btn2_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn2.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn3 = Button(btnrow1, text="3", font="Segoe 23", relief=GROOVE, bd=0, command=btn3_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn3.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btnp = Button(btnrow1, text="+", font="Segoe 23", relief=GROOVE, bd=0, command=btnp_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btnp.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btnrow2 = Frame(root)
    btnrow2.pack(expand=TRUE, fill=BOTH)

    e_btn = Button(btnrow2, text="e", font="Segoe 18", relief=GROOVE, bd=0, command=e_clicked, fg="#25265E",
                   bg="#F8FAFF")
    e_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    sqr_btn = Button(btnrow2, text=" √x ", font="Segoe 18", relief=GROOVE, bd=0, command=sqr_clicked, fg="#25265E",
                     bg="#F8FAFF")
    sqr_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    sinh_btn = Button(btnrow2, text="sin−1", font="Segoe 11 bold", relief=GROOVE, bd=0, command=arcsin_clicked,
                      fg="#25265E", bg="#F8FAFF")
    sinh_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    cosh_btn = Button(btnrow2, text="cos-1", font="Segoe 11 bold", relief=GROOVE, bd=0, command=arccos_clicked,
                      fg="#25265E", bg="#F8FAFF")
    cosh_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    tanh_btn = Button(btnrow2, text="tan-1", font="Segoe 11 bold", relief=GROOVE, bd=0, command=arctan_clicked,
                      fg="#25265E", bg="#F8FAFF")
    tanh_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn4 = Button(btnrow2, text="4", font="Segoe 23", relief=GROOVE, bd=0, command=btn4_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn4.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn5 = Button(btnrow2, text="5", font="Segoe 23", relief=GROOVE, bd=0, command=btn5_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn5.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn6 = Button(btnrow2, text="6", font="Segoe 23", relief=GROOVE, bd=0, command=btn6_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn6.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btnm = Button(btnrow2, text="-", font="Segoe 23", relief=GROOVE, bd=0, command=btnm_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btnm.pack(side=LEFT, expand=TRUE, fill=BOTH)

    # Row 3 Buttons

    btnrow3 = Frame(root)
    btnrow3.pack(expand=TRUE, fill=BOTH)

    conv_btn = Button(btnrow3, text="Rad", font="Segoe 12 bold", relief=GROOVE, bd=0, command=conv_clicked,
                      fg="#25265E",
                      bg="#F8FAFF")
    conv_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    round_btn = Button(btnrow3, text="round", font="Segoe 10 bold", relief=GROOVE, bd=0, command=round_clicked,
                       fg="#25265E", bg="#F8FAFF")
    round_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    ln_btn = Button(btnrow3, text="ln", font="Segoe 18", relief=GROOVE, bd=0, command=ln_clicked, fg="#25265E",
                    bg="#F8FAFF")
    ln_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    logarithm_btn = Button(btnrow3, text="log", font="Segoe 17", relief=GROOVE, bd=0, command=logarithm_clicked,
                           fg="#25265E", bg="#F8FAFF")
    logarithm_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    pow_btn = Button(btnrow3, text="x^y", font="Segoe 17", relief=GROOVE, bd=0, command=pow_clicked, fg="#25265E",
                     bg="#F8FAFF")
    pow_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn7 = Button(btnrow3, text="7", font="Segoe 23", relief=GROOVE, bd=0, command=btn7_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn7.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn8 = Button(btnrow3, text="8", font="Segoe 23", relief=GROOVE, bd=0, command=btn8_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn8.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn9 = Button(btnrow3, text="9", font="Segoe 23", relief=GROOVE, bd=0, command=btn9_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn9.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btnml = Button(btnrow3, text="*", font="Segoe 23", relief=GROOVE, bd=0, command=btnml_clicked, fg="#25265E",
                   bg="#FFFFFF")
    btnml.pack(side=LEFT, expand=TRUE, fill=BOTH)

    # Row 4 Buttons

    btnrow4 = Frame(root)
    btnrow4.pack(expand=TRUE, fill=BOTH)

    mod_btn = Button(btnrow4, text="%", font="Segoe 21", relief=GROOVE, bd=0, command=mod_clicked, fg="#25265E",
                     bg="#FFFFFF")
    mod_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    bl_btn = Button(btnrow4, text=" ( ", font="Segoe 21", relief=GROOVE, bd=0, command=bl_clicked, fg="#25265E",
                    bg="#FFFFFF")
    bl_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    br_btn = Button(btnrow4, text=" ) ", font="Segoe 21", relief=GROOVE, bd=0, command=br_clicked, fg="#25265E",
                    bg="#FFFFFF")
    br_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    dot_btn = Button(btnrow4, text=" • ", font="Segoe 21", relief=GROOVE, bd=0, command=dot_clicked, fg="#25265E",
                     bg="#FFFFFF")
    dot_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btnc = Button(btnrow4, text="C", font="Segoe 23", relief=GROOVE, bd=0, command=btnc_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btnc.pack(side=LEFT, expand=TRUE, fill=BOTH)

    del_btn = Button(btnrow4, text="⌫", font="Segoe 20", relief=GROOVE, bd=0, command=del_clicked, fg="#25265E",
                     bg="#FFFFFF")
    del_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btn0 = Button(btnrow4, text="0", font="Segoe 23", relief=GROOVE, bd=0, command=btn0_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btn0.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btneq = Button(btnrow4, text="=", font="Segoe 23", relief=GROOVE, bd=0, command=btneq_clicked, fg="#25265E",
                   bg="#FFFFFF")
    btneq.pack(side=LEFT, expand=TRUE, fill=BOTH)

    btnd = Button(btnrow4, text="/", font="Segoe 23", relief=GROOVE, bd=0, command=btnd_clicked, fg="#25265E",
                  bg="#FFFFFF")
    btnd.pack(side=LEFT, expand=TRUE, fill=BOTH)

    menubar1 = Menu(root)

    root.config(menu=menubar1)
    fileMenu = Menu(menubar1, tearoff=0)
    fileMenu.add_command(label="Standard Calculator", command=lambda: [root.destroy(), Standard_Calculator()])
    menubar1.add_cascade(label="Options", menu=fileMenu)

    # fileMenu = Menu(menubar1, tearoff=0)
    # fileMenu.add_command(label="Check for Update", command=check_for_update)
    # menubar1.add_cascade(label="Update", menu=fileMenu)

    fileMenu = Menu(menubar1, tearoff=0)
    fileMenu.add_command(label="About", command=about)
    menubar1.add_cascade(label="More", menu=fileMenu)

    root.mainloop()


if __name__ == "__main__":
    calc = Standard_Calculator()
    calc.run()
