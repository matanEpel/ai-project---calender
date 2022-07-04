import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

from assignment import Assignment
from constraint import Constraints
from manager import Manager
from user import User
from time_ import Time

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
        filemenu.add_command(label="add\edit specific user", command=self.specific_user)
        filemenu.add_command(label="add assignment to user", command=self.add_assignment)

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

        users = {}
        for u in self.__manager.get_users():
            users[u.get_name()] = u

        bamb = StringVar(root)
        bamb.set("CHOOSE THE USER YOU WANT TO LOOK AT")
        w = OptionMenu(root, bamb, "none", *(users.keys()))
        w.place(x=150, y=100)

        week_var = StringVar(root)
        week_var.set("CHOOSE THE WEEK YOU WANT TO LOOK AT")
        weeks = set()
        for u in self.__manager.get_users():
            for ass in u.all_get_assignments():
                weeks.add(ass.get_week())
        w = OptionMenu(root, week_var, 1, *(weeks))
        w.place(x=150, y=150)

        def submit_func():
            if bamb.get() == "none" or bamb.get() == "CHOOSE THE USER YOU WANT TO LOOK AT":
                self.home()
                return
            for ele in root.winfo_children():
                ele.destroy()
            self.add_menu()
            panel = Label(root, text=bamb.get() + "'s assignments", font=('calibre', 80), bg='white', justify='center')
            panel.place(x=0, y=0, width=600)

            user = None
            name = bamb.get()
            for u in self.__manager.get_users():
                if u.get_name() == name:
                    user = u
            week = int(week_var.get())
            i = 0
            for ass in user.get_assignments(week):
                if ass.get_time():
                    hour = str(ass.get_time().get_hours())
                    minute = str(ass.get_time().get_minutes())
                    panel = Label(root, text="name: " + ass.get_name() + ", duration: " + str(round(float(ass.get_duration()))) + ", start time: " + hour+":"+minute, font=('calibre', 20), bg='white', justify='center')
                    panel.place(x=0, y=100+i*50, width=600)
                else:
                    panel = Label(root, text="name: " + ass.get_name() + ", duration: " + str(
                        float(ass.get_duration())) + ", start time hasn't determined yet", font=('calibre', 20),
                                  bg='white', justify='center')
                    panel.place(x=0, y=100+i * 50, width=600)
                i += 1

        submit = Button(root, text="GO!", command=submit_func, bd=3, font=('calibre', 25), bg='white')
        submit.place(x=225, y=210, width=150, height=70)

        def schedule():
            for week in weeks:
                print("week " + str(week) + " was scheduled!")
                self.__manager.schedule_week(week)
        submit = Button(root, text="SCHEDULE!", command=schedule, bd=3, font=('calibre', 25), bg='white')
        submit.place(x=225, y=310, width=150, height=70)

    def add_assignment(self):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()
        panel = Label(root, text="add assignment to user", font=('calibre', 60), bg='white', justify='center')
        panel.place(x=0, y=0, width=600)

        name_var = tk.StringVar()

        e1 = tk.Entry(root, textvariable=name_var, bd=3, font=('calibre', 25), justify='center')
        e1.place(x=150, y=250, width=300, height=50)

        panel = Label(root, text="enter user name:", font=('calibre', 30), bg='white')
        panel.place(x=180, y=200)

        def submit_func():
            name = name_var.get()
            for ele in root.winfo_children():
                ele.destroy()
            self.add_menu()

            ass_name_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_name_var, bd=3, font=('calibre', 25), justify='center')
            e1.place(x=150, y=50, width=300, height=50)

            panel = Label(root, text="enter assignment name:", font=('calibre', 30), bg='white')
            panel.place(x=150, y=0)

            ass_length_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_length_var, bd=3, font=('calibre', 25), justify='center')
            e1.place(x=150, y=150, width=300, height=50)

            panel = Label(root, text="enter assignment length:", font=('calibre', 30), bg='white')
            panel.place(x=150, y=100)

            ass_week_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_week_var, bd=3, font=('calibre', 25), justify='center')
            e1.place(x=150, y=250, width=300, height=50)

            panel = Label(root, text="enter assignment week:", font=('calibre', 30), bg='white')
            panel.place(x=150, y=200)

            ass_part_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_part_var, bd=3, font=('calibre', 25), justify='center')
            e1.place(x=150, y=350, width=300, height=50)

            panel = Label(root, text="enter assignment participants:", font=('calibre', 30), bg='white')
            panel.place(x=110, y=300)

            def submit_func_ass():
                print(1)
                if name in [u.get_name() for u in self.__manager.get_users()]:
                    user = None
                    for u in self.__manager.get_users():
                        if u.get_name() == name:
                            user = u

                    partici = []
                    for part in ass_part_var.get().split(", "):
                        curr_user = None
                        for u in self.__manager.get_users():
                            if u.get_name() == part:
                                curr_user = u
                        partici.append(curr_user)
                    assignment = Assignment(int(ass_week_var.get()), ass_name_var.get(), int(ass_length_var.get()), participants=partici)
                    user.add_assignment(assignment)
                self.home()
            submit = Button(root, text="Submit", command=submit_func_ass, bd=3, font=('calibre', 25), bg='white')
            submit.place(x=225, y=410, width=150, height=70)

        submit = Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25), bg='white')
        submit.place(x=225, y=310, width=150, height=70)

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
            assignments = []
            if name in [u.get_name() for u in self.__manager.get_users()]:
                user = None
                for u in self.__manager.get_users():
                    if u.get_name() == name:
                        user = u
                self.__manager.del_user(user)

            for ele in root.winfo_children():
                ele.destroy()
            self.add_menu()

            panel = Label(root, text="Edit\\create " + name + "'s data", font=('calibre', 50), justify='center')
            panel.place(x=0, y=0, width=600)
            print(name)

            olm = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlapping meetings', variable=olm, onvalue=1, offvalue=0,
                                font=('calibre', 18))
            c1.place(x=0, y=200)

            olt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlapping tasks', variable=olt, onvalue=1, offvalue=0,
                                font=('calibre', 18))
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
            c1.place(x=0, y=350)

            bbm = StringVar(root)
            bbm.set("break before meeting")  # default value
            w = OptionMenu(root, bbm, 0, 5, 10, 15, 20)
            w.place(x=0, y=80)

            bbt = StringVar(root)
            bbt.set("break before task")  # default value
            w = OptionMenu(root, bbt, 0, 5, 10, 15, 20)
            w.place(x=0, y=120)

            bbmb = StringVar(root)
            bbmb.set("break before must be")  # default value
            w = OptionMenu(root, bbmb, 0, 5, 10, 15, 20)
            w.place(x=0, y=160)

            bam = StringVar(root)
            bam.set("break after meeting")  # default value
            w = OptionMenu(root, bam, 0, 5, 10, 15, 20)
            w.place(x=200, y=80)

            bat = StringVar(root)
            bat.set("break after task")  # default value
            w = OptionMenu(root, bat, 0, 5, 10, 15, 20)
            w.place(x=200, y=120)

            bamb = StringVar(root)
            bamb.set("break after must be")  # default value
            w = OptionMenu(root, bamb, 0, 5, 10, 15, 20)
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
            c1.place(x=380, y=180)

            md = tk.IntVar()
            c1 = tk.Checkbutton(root, text='2', variable=md, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=420, y=180)

            tud = tk.IntVar()
            c1 = tk.Checkbutton(root, text='3', variable=tud, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=460, y=180)

            wd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='4', variable=wd, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=500, y=180)

            thd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='5', variable=thd, onvalue=1, offvalue=0,
                                font=('calibre', 14))
            c1.place(x=540, y=180)

            Label(root,
                  text="Working days:", font=('calibre', 14)).place(x=430,
                                                                    y=155)

            mact = StringVar(root)
            mact.set("meetings are close together")  # default value
            w = OptionMenu(root, mact, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=300, y=230)

            tact = StringVar(root)
            tact.set("tasks are close together")  # default value
            w = OptionMenu(root, tact, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=300, y=260)

            bac = StringVar(root)
            bac.set("breaks are continuous")  # default value
            w = OptionMenu(root, bac, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=300, y=290)

            fde = StringVar(root)
            fde.set("finish the day early")  # default value
            w = OptionMenu(root, fde, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=300, y=320)

            stdl = StringVar(root)
            stdl.set("start the day late")  # default value
            w = OptionMenu(root, stdl, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.place(x=300, y=350)

            def submit_user():
                constraints = Constraints()
                constraints.set_hard_constraint("overlapping meetings", olm.get())
                constraints.set_hard_constraint("overlapping tasks", olt.get())
                constraints.set_hard_constraint("overlapping must be", olmb.get())
                constraints.set_hard_constraint("overlap meeting task", olmt.get())
                constraints.set_hard_constraint("overlap meeting must be", olmmb.get())
                constraints.set_hard_constraint("overlap must be task", olmbt.get())
                constraints.set_hard_constraint("must be is must be", mbimb.get())
                constraints.set_hard_constraint("break before meeting", Time(m=int(bbm.get())))
                constraints.set_hard_constraint("break before task", Time(m=int(bbt.get())))
                constraints.set_hard_constraint("break before must be", Time(m=int(bbmb.get())))
                constraints.set_hard_constraint("break after meeting", Time(m=int(bam.get())))
                constraints.set_hard_constraint("break after task", Time(m=int(bat.get())))
                constraints.set_hard_constraint("break after must be", Time(m=int(bamb.get())))
                constraints.set_hard_constraint("start of the day", Time(h=int(sotd.get())))
                constraints.set_hard_constraint("end of the day", Time(h=int(eotd.get())))
                days = []
                if int(sd.get()):
                    days.append(1)
                if int(md.get()):
                    days.append(2)
                if int(tud.get()):
                    days.append(3)
                if int(wd.get()):
                    days.append(4)
                if int(thd.get()):
                    days.append(5)
                constraints.set_hard_constraint("working days", days)
                constraints.set_soft_constraint("meetings are close together", int(mact.get()))
                constraints.set_soft_constraint("tasks are close together", int(tact.get()))
                constraints.set_soft_constraint("breaks are continuous", int(bac.get()))
                constraints.set_soft_constraint("finish the day early", int(fde.get()))
                constraints.set_soft_constraint("start the day late", int(stdl.get()))
                new_user = User(name, constraints)
                self.__manager.add_user(new_user)
                self.home()

            submit = Button(root, text="Submit", command=submit_user, bd=3, font=('calibre', 25), bg='white')
            submit.place(x=225, y=410, width=150, height=70)

        submit = Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25), bg='white')
        submit.place(x=225, y=310, width=150, height=70)

        # sub_btn = tk.Button(root, text='Submit', command=submit)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
