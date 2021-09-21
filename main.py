import tkinter as tk
from tkinter import *
import tkinter.messagebox
import time
import os
import math
import webbrowser
from tkinter import messagebox

calculator_version = "Calculator v1.3"

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
splash_screen_Calculator_png = path + "\Icons\Splash_Screen.png"
whats_new_icon = path + "\Icons\What's new.ico"
bmi_icon = path + "\Icons\BMI.ico"

v1_3_what_new_list = "- BMI Calculator Section added under Options Tab\n- BMI Calculator added\n- Some bug fixed\n" \
                     "- Update History Feature"

v1_2_what_new_list = "- Splash Screen added\n- Standard Calculator position fixed" \
                     "\n- Scientific Calculator position fixed\n- \"What's New\" tab added"


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


def whats_new():
    whats_new_window = tk.Tk()
    whats_new_window.title("What's new?")
    whats_new_window.wm_iconbitmap(about_icon)
    whats_new_window.geometry("400x300")
    whats_new_window.resizable(0, 0)
    whats_new_window.iconbitmap(whats_new_icon)

    lbl1 = Label(whats_new_window, text="What's new?", justify=LEFT, font=('Arial', 18, "bold"))

    v1_3 = Label(whats_new_window, text="Version 1.3", justify=LEFT, font=("Arial", 14), relief=FLAT, state=ACTIVE)
    v1_3_what_new_label = Label(whats_new_window, text=v1_3_what_new_list, justify=LEFT, font=("Arial", 11),
                                relief=FLAT, state=ACTIVE)

    v1_2 = Label(whats_new_window, text="Version 1.2", justify=LEFT, font=("Arial", 14), relief=FLAT, state=DISABLED)
    v1_2_what_new_label = Label(whats_new_window, text=v1_2_what_new_list, justify=LEFT, font=("Arial", 11),
                                relief=FLAT, state=DISABLED)

    lbl1.place(x=10)
    v1_3.place(x=10, y=40)
    v1_3_what_new_label.place(x=10, y=70)

    v1_2.place(x=10, y=150)
    v1_2_what_new_label.place(x=10, y=180)

    def update_history():
        webbrowser.open("https://github.com/Sayad-Uddin-Tahsin/Simple-Calculator/blob/main/Update%20History")

    copy_button = Button(whats_new_window, text="Update History",
                         command=update_history, state=ACTIVE)
    copy_button.place(x=300, y=270)


splash_screen = Tk()
splash_screen.geometry("320x478+500+120")

img = PhotoImage(file=splash_screen_Calculator_png)
img_label = Label(splash_screen, image=img)
img_label.place(x=30, y=90)

splash_screen.overrideredirect(True)
splash_screen.after(1000, lambda: [splash_screen.destroy()])


class Standard_Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("320x478+500+120")
        self.window.resizable(0, 0)
        self.window.title("Calculator by Tahsin")
        self.window.iconbitmap(calculator_icon)

        menubar1 = Menu(self.window)

        self.window.config(menu=menubar1)
        self.fileMenu = Menu(menubar1, tearoff=0)
        self.fileMenu.add_command(label="Scientific Calculator",
                                  command=lambda: [self.window.destroy(), Scientific_Calculator()])
        self.fileMenu.add_command(label="BMI Calculator",
                                  command=lambda: [self.window.destroy(), BMI_Calculator()])

        menubar1.add_cascade(label="Options", menu=self.fileMenu)

        self.fileMenu = Menu(menubar1, tearoff=0)
        self.fileMenu.add_command(label="What's new?", command=whats_new)
        self.fileMenu.add_separator()
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
    root.geometry("650x400+400+120")
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
    fileMenu.add_command(label="BMI Calculator", command=lambda: [root.destroy(), BMI_Calculator()])
    menubar1.add_cascade(label="Options", menu=fileMenu)

    # fileMenu = Menu(menubar1, tearoff=0)
    # fileMenu.add_command(label="Check for Update", command=check_for_update)
    # menubar1.add_cascade(label="Update", menu=fileMenu)

    fileMenu = Menu(menubar1, tearoff=0)
    fileMenu.add_command(label="What's new?", command=whats_new)
    fileMenu.add_separator()
    fileMenu.add_command(label="About", command=about)
    menubar1.add_cascade(label="More", menu=fileMenu)

    root.mainloop()


def BMI_Calculator():
    def reset_entry():
        age_tf.delete(0, 'end')
        height_tf.delete(0, 'end')
        weight_tf.delete(0, 'end')
        var.set(0)

    def calculate_bmi(event):
        kg = int(weight_tf.get())
        m = int(height_tf.get()) / 100
        bmi = kg / (m * m)
        bmi = round(bmi, 1)
        bmi_index(bmi)

    def calculate_bmi_button():
        kg = int(weight_tf.get())
        m = int(height_tf.get()) / 100
        bmi = kg / (m * m)
        bmi = round(bmi, 1)
        bmi_index(bmi)

    def bmi_index(bmi):
        if bmi < 18.5:
            messagebox.showinfo('BMI Result', f'BMI = {bmi} is Underweight')
        elif (bmi > 18.5) and (bmi < 24.9):
            messagebox.showinfo('BMI Result', f'BMI = {bmi} is Healthy')
        elif (bmi > 24.9) and (bmi < 29.9):
            messagebox.showinfo('BMI Result', f'BMI = {bmi} is Overweight')
        else:
            messagebox.showinfo('BMI Result', f'BMI = {bmi} is Obese')

    ws = Tk()
    ws.title('BMI Calculator by Tahsin')
    ws.geometry('550x395+500+180')
    ws.iconbitmap(bmi_icon)
    ws.config(bg='#F5F5F5')
    ws.resizable(0, 0)

    what_is_bmi = "Body mass index (BMI) is a value \nderived from the mass (weight)\nand height of a " \
                  "person. The BMI is \ndefined as the body mass divided \nby the square of the body height, \n" \
                  "and is expressed in units of kg/m². \nIt can broadly categorize a person \nas underweight, " \
                  "normal weight, \noverweight, or obese based on \ntissue mass (muscle, fat, and \nbone) and height."

    bmi_scale = "\n\nBelow 18.5              : Underweight   \n" \
                "18.5 - 24.9	: Healthy\n" \
                "25.0 - 29.9	: Overweight\n" \
                "30.0 and Above	: Obese"

    bmi_scale_label = Label(ws, text=bmi_scale, font=("Arial", 11), justify=LEFT)
    bmi_scale_label.place(x=320, y=245)

    bmi_scale_label = Label(ws, text="BMI Scale", font=("Arial", 12, "bold"), justify=LEFT)
    bmi_scale_label.place(x=380, y=245)

    text_frame = Frame(
        ws,
        padx=15,
        pady=10
    )
    text_frame.place(x=315, y=-5)

    what_is_bmi_label = Label(text_frame, text="What is BMI?", font=("Arial", 12, "bold"), justify=CENTER)
    what_is_bmi_label.pack()

    what_is_bmi_label = Label(text_frame, text=what_is_bmi, font=("Arial", 10), justify=LEFT)
    what_is_bmi_label.pack()

    var = IntVar()

    frame = Frame(
        ws,
        padx=15,
        pady=10
    )
    frame.pack(side=LEFT, padx=10)

    age_lb = Label(
        frame,
        text="Age (2 - 120)"
    )
    age_lb.grid(row=1, column=1)

    age_tf = Entry(
        frame,
    )
    age_tf.grid(row=1, column=2, pady=5)

    gen_lb = Label(
        frame,
        text='Gender'
    )
    gen_lb.grid(row=2, column=1)

    frame2 = Frame(
        frame
    )
    frame2.grid(row=2, column=2, pady=5)

    male_rb = Radiobutton(
        frame2,
        text='Male',
        variable=var,
        value=1
    )
    male_rb.pack(side=LEFT)

    female_rb = Radiobutton(
        frame2,
        text='Female',
        variable=var,
        value=2
    )
    female_rb.pack(side=RIGHT)

    height_lb = Label(
        frame,
        text="Height (cm)  "
    )
    height_lb.grid(row=3, column=1)

    weight_lb = Label(
        frame,
        text="Weight (kg)  ",

    )
    weight_lb.grid(row=4, column=1)

    height_tf = Entry(
        frame,
    )
    height_tf.grid(row=3, column=2, pady=5)

    weight_tf = Entry(
        frame,
    )
    weight_tf.grid(row=4, column=2, pady=5)

    frame3 = Frame(
        frame
    )
    frame3.grid(row=5, columnspan=4, padx=20, pady=20)

    cal_btn = Button(
        frame,
        text='Calculate',
        command=calculate_bmi_button

    )

    cal_btn.place(x=75, y=130)

    ws.bind("<Return>", calculate_bmi)

    reset_btn = Button(
        frame,
        text='Reset',
        command=reset_entry
    )
    reset_btn.place(x=160, y=130)

    menubar1 = Menu(ws)

    ws.config(menu=menubar1)
    fileMenu = Menu(menubar1, tearoff=0)
    fileMenu.add_command(label="Standard Calculator", command=lambda: [ws.destroy(), Standard_Calculator()])
    fileMenu.add_command(label="Scientific Calculator", command=lambda: [ws.destroy(), Scientific_Calculator()])
    menubar1.add_cascade(label="Options", menu=fileMenu)

    fileMenu = Menu(menubar1, tearoff=0)
    fileMenu.add_command(label="What's new?", command=whats_new)
    fileMenu.add_separator()
    fileMenu.add_command(label="About", command=about)
    menubar1.add_cascade(label="More", menu=fileMenu)

    ws.mainloop()


if __name__ == "__main__":
    splash_screen.mainloop()
    calc = Standard_Calculator()
    calc.run()
