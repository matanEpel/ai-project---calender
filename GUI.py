import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

from manager import Manager

class App:
    def __init__(self, root):
        self.__manager = Manager()
        # setting title
        self.__root = root
        root.title("calender")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.home()

    def add_menu(self):
        menubar = Menu(self.__root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="home", command=self.home)
        filemenu.add_command(label="see all users", command=self.all_users)
        filemenu.add_command(label="choose specific user", command=self.specific_user)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="options", menu=filemenu)

        self.__root.config(menu=menubar)

    def home(self):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()
        img = Image.open("resources/calender.png")
        img = img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=250, y=100)

        img = Image.open("resources/title.png")
        img = img.resize((482, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=70, y=0)

        img = Image.open("resources/description.png")
        img = img.resize((600, 263), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=0, y=220)

    def all_users(self):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()
        panel = Label(root, text="All users", font=('calibre', 80), bg='white', justify='center')
        panel.place(x=0, y=0, width=600)

    def specific_user(self):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()
        panel = Label(root, text="Edit\\add user", font=('calibre', 80), bg='white', justify='center')
        panel.place(x=0, y=0, width=600)

        name_var = tk.StringVar()

        e1 = tk.Entry(root, textvariable=name_var, bd=3, font=('calibre', 25), justify='center')
        e1.place(x=150, y=250, width=300, height=50)

        panel = Label(root, text="enter user name:", font=('calibre', 30), bg='white')
        panel.place(x=180, y=200)

        def submit_func():
            name = name_var.get()
            hard_constraints = dict()
            soft_constraints = dict()
            assignments = []
            if name in [u.get_name() for u in self.__manager.get_users()]:
                user = None
                for u in self.__manager.get_users():
                    if u.get_name() == name:
                        user = u
                assignments += user.get_assignments()
                hard_constraints["overlapping meetings"] = user.get_constraints.get_hard_constraints("overlapping meetings")
                hard_constraints["overlapping tasks"] = user.get_constraints.get_hard_constraints("overlapping tasks")
                hard_constraints["overlapping must be"] = user.get_constraints.get_hard_constraints("overlapping must be")
                hard_constraints["overlap meeting task"] = user.get_constraints.get_hard_constraints("overlap meeting task")
                hard_constraints["overlap meeting must be"] = user.get_constraints.get_hard_constraints("overlap meeting must be")
                hard_constraints["overlap must be task"] = user.get_constraints.get_hard_constraints("overlap must be task")
                hard_constraints["must be is must be"] = user.get_constraints.get_hard_constraints("must be is must be")
                hard_constraints["break before meeting"] = user.get_constraints.get_hard_constraints("break before meeting")
                hard_constraints["break before task"] = user.get_constraints.get_hard_constraints("break before task")
                hard_constraints["break before must be"] = user.get_constraints.get_hard_constraints("break before must be")
                hard_constraints["break after meeting"] = user.get_constraints.get_hard_constraints("break after meeting")
                hard_constraints["break after task"] = user.get_constraints.get_hard_constraints("break after task")
                hard_constraints["break after must be"] = user.get_constraints.get_hard_constraints("break after must be")
                hard_constraints["start of the day"] = user.get_constraints.get_hard_constraints("start of the day")
                hard_constraints["end of the day"] = user.get_constraints.get_hard_constraints("end of the day")
                hard_constraints["working days"] = user.get_constraints.get_hard_constraints("working days")
                soft_constraints["meetings are close together"] = user.get_constraints.get_soft_constraints("meetings are close together")
                soft_constraints["tasks are close together"] = user.get_constraints.get_soft_constraints("tasks are close together")
                soft_constraints["breaks are continuous"] = user.get_constraints.get_soft_constraints("breaks are continuous")
                soft_constraints["finish the day early"] = user.get_constraints.get_soft_constraints("finish the day early")
                soft_constraints["start the day late"] = user.get_constraints.get_soft_constraints("start the day late")
                self.__manager.del_user(user)
            else:
                hard_constraints["overlapping meetings"] = False
                hard_constraints["overlapping tasks"] = False
                hard_constraints["overlapping must be"] = False
                hard_constraints["overlap meeting task"] = False
                hard_constraints["overlap meeting must be"] = False
                hard_constraints["overlap must be task"] = False
                hard_constraints["must be is must be"] = True
                hard_constraints["break before meeting"] = 0
                hard_constraints["break before task"] = 0
                hard_constraints["break before must be"] = 0
                hard_constraints["break after meeting"] = 0
                hard_constraints["break after task"] = 0
                hard_constraints["break after must be"] = 0
                hard_constraints["start of the day"] = 8
                hard_constraints["end of the day"] = 22
                hard_constraints["working days"] = [1,2,3,4,5]
                soft_constraints["meetings are close together"] = 1
                soft_constraints["tasks are close together"] = 1
                soft_constraints["breaks are continuous"] = 1
                soft_constraints["finish the day early"] = 1
                soft_constraints["start the day late"] = 1
            for ele in root.winfo_children():
                ele.destroy()
            self.add_menu()

            panel = Label(root, text = "Edit\\create " + name +"'s data", font=('calibre', 50), justify='center')
            panel.place(x=0, y=0,width=600)
            print(name)

            submit = Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25), bg='white')
            submit.place(x=225, y=410, width=150, height=70)

            olm = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlapping meetings', variable=olm, onvalue=1, offvalue=0, font=('calibre', 18))
            c1.place(x=0, y=200)

            olt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlapping tasks', variable=olt, onvalue=1, offvalue=0, font=('calibre', 18))
            c1.place(x=0, y=225)

            olmb = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlapping must be', variable=olmb, onvalue=1, offvalue=0,
                                font=('calibre', 18))
            c1.place(x=0, y=250)

            olmt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap meeting task', variable=olmt, onvalue=1, offvalue=0,
                                font=('calibre', 18))
            c1.place(x=0, y=275)

            olmmb = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap meeting must be', variable=olmmb, onvalue=1, offvalue=0,
                                font=('calibre', 18))
            c1.place(x=0, y=300)

            olmbt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap must be task', variable=olmbt, onvalue=1, offvalue=0,
                                font=('calibre', 18))
            c1.place(x=0, y=325)

            mbimb = tk.IntVar()
            c1 = tk.Checkbutton(root, text='must be is must be', variable=mbimb, onvalue=1, offvalue=0,
                                font=('calibre', 18))
            c1.place(x=0, y=325)

            bbm = StringVar(root)
            bbm.set("break before meeting")  # default value
            w = OptionMenu(root, bbm, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=0, y=80)

            bbt = StringVar(root)
            bbt.set("break before task")  # default value
            w = OptionMenu(root, bbt, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=0, y=120)

            bbmb = StringVar(root)
            bbmb.set("break before must be")  # default value
            w = OptionMenu(root, bbmb, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=0, y=160)

            bam = StringVar(root)
            bam.set("break after meeting")  # default value
            w = OptionMenu(root, bam, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=200, y=80)

            bat = StringVar(root)
            bat.set("break after task")  # default value
            w = OptionMenu(root, bat, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=200, y=120)

            bamb = StringVar(root)
            bamb.set("break after must be")  # default value
            w = OptionMenu(root, bamb, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=200, y=160)

            sotd = StringVar(root)
            sotd.set("start of the day")  # default value
            w = OptionMenu(root, sotd, 6, 7, 8, 9, 10, 11, 12)
            w.place(x=400, y=80)

            eotd = StringVar(root)
            eotd.set("end of the day")  # default value
            w = OptionMenu(root, eotd, 16, 17, 18, 19, 20, 21, 22, 23, 24)
            w.place(x=400, y=120)

            sd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='1', variable=sd, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=400, y=170)

            md = tk.IntVar()
            c1 = tk.Checkbutton(root, text='2', variable=md, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=400, y=180)

            tud = tk.IntVar()
            c1 = tk.Checkbutton(root, text='3', variable=tud, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=400, y=190)

        submit = Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25), bg='white')
        submit.place(x=225,y=310, width = 150, height=70)

        # sub_btn = tk.Button(root, text='Submit', command=submit)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
