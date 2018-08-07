from tkinter import *
from tkinter import filedialog
# import sys
# sys.path.append('E:/Projects/MSCognitiveAPI/Emotion')
from .mypkg.detect import run

# print(run())
#
# sys.exit(0)

class BuckyCuttons:

    def __init__(self, master):

        menu = Menu(master)
        master.config(menu=menu)

        submenu = Menu(menu)
        editmenu = Menu(menu)
        menu.add_cascade(label="File", menu=submenu)
        menu.add_cascade(label="Edit", menu=editmenu)

        submenu.add_command(label="New Project...", command=self.print_name)
        submenu.add_separator()
        submenu.add_command(label="Options", command=self.print_name)

        editmenu.add_command(label="Eat", command=self.print_name)
        editmenu.add_separator()
        editmenu.add_command(label="Bark", command=self.print_name)

        frame = Frame(master)
        frame.pack()

        self.label_1 = Label(frame, text="Name")
        self.label_2 = Label(frame, text="Password")
        self.entry_1 = Entry(frame)
        self.entry_2 = Entry(frame)

        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)

        self.check_box = Checkbutton(frame, text="Keep logged on")
        self.check_box.grid(row=2, columnspan=2)

        self.button_print_1 = Button(frame, text="Print my name")
        self.button_print_1.bind("<Button-1>", self.print_name)
        self.button_print_1.grid(row=3)

        self.button_print_2 = Button(frame, text="Quit", command=frame.quit)
        self.button_print_2.grid(row=3, column=1)

        self.button_print_3 = Button(frame, text="Browse")
        self.button_print_3.bind("<Button-1>", self.browsefunc)
        self.button_print_3.grid(row=3, column=3)


    def browsefunc(self, event):
        filename = filedialog.askopenfilename()
        print(filename)

    def print_name(self, event):
        print("Username", self.entry_1.get())
        print("Password", self.entry_2.get())


# create a blank windows
root = Tk()

b = BuckyCuttons(root)

# continue the display
root.mainloop()