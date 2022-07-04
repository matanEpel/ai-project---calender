import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

from assignment import Assignment
from constraint import Constraints
from consts import MIDDLE_OUT, MIDDLE_FIIL, DOWN_GUI, UP_GUI, TOP_FIIL, TOP_OUT
from manager import Manager
from user import User
from time_ import Time

def roundPolygon(canvas, x, y, sharpness, **kwargs):

    # The sharpness here is just how close the sub-points
    # are going to be to the vertex. The more the sharpness,
    # the more the sub-points will be closer to the vertex.
    # (This is not normalized)
    if sharpness < 2:
        sharpness = 2

    ratioMultiplier = sharpness - 1
    ratioDividend = sharpness

    # Array to store the points
    points = []

    # Iterate over the x points
    for i in range(len(x)):
        # Set vertex
        points.append(x[i])
        points.append(y[i])

        # If it's not the last point
        if i != (len(x) - 1):
            # Insert submultiples points. The more the sharpness, the more these points will be
            # closer to the vertex.
            points.append((ratioMultiplier*x[i] + x[i + 1])/ratioDividend)
            points.append((ratioMultiplier*y[i] + y[i + 1])/ratioDividend)
            points.append((ratioMultiplier*x[i + 1] + x[i])/ratioDividend)
            points.append((ratioMultiplier*y[i + 1] + y[i])/ratioDividend)
        else:
            # Insert submultiples points.
            points.append((ratioMultiplier*x[i] + x[0])/ratioDividend)
            points.append((ratioMultiplier*y[i] + y[0])/ratioDividend)
            points.append((ratioMultiplier*x[0] + x[i])/ratioDividend)
            points.append((ratioMultiplier*y[0] + y[i])/ratioDividend)
            # Close the polygon
            points.append(x[0])
            points.append(y[0])

    return canvas.create_polygon(points, **kwargs, smooth=TRUE)

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
            for ass in u.get_all_assignments():
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
            panel = Label(root, text=bamb.get() + "'s assignments", font=('calibre', 50), bg='white', justify='center')
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
                    for part in partici:
                        part.add_assignment(assignment)
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

            canvas = Canvas(root, width=600, height=500)
            roundPolygon(canvas, [170, 440, 440, 170], [340-DOWN_GUI, 340-DOWN_GUI, 425-DOWN_GUI, 425-DOWN_GUI], 10, width=5, outline="#82B366", fill="#D5E8D4")
            roundPolygon(canvas, [50, 560, 560, 50], [190-DOWN_GUI, 190-DOWN_GUI, 320-DOWN_GUI, 320-DOWN_GUI], 10, width=5, outline=MIDDLE_OUT, fill=MIDDLE_FIIL)
            roundPolygon(canvas, [10, 590, 590, 10], [60-UP_GUI, 60-UP_GUI, 220-UP_GUI, 220-UP_GUI], 10, width=5, outline=TOP_OUT, fill=TOP_FIIL)
            canvas.place(x=0, y=0)

            panel = Label(root, text="Edit\\create " + name + "'s data", font=('calibre', 30), justify='center')
            panel.place(x=0, y=0, width=600)
            print(name)


            olmt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap meeting and task', variable=olmt, onvalue=1, offvalue=0,
                                font=('calibre', 18),bg="#D5E8D4")
            c1.place(x=190, y=350-DOWN_GUI)


            olmbt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap must be and task', variable=olmbt, onvalue=1, offvalue=0,
                                font=('calibre', 18),bg="#D5E8D4")
            c1.place(x=190, y=390-DOWN_GUI)

            panel = Label(root, text="lunch start hour", font=('calibre', 15), justify='center', bg=MIDDLE_FIIL)
            panel.place(x=60, y=200-DOWN_GUI)
            lst = IntVar(root)
            w = OptionMenu(root, lst, 10, 11, 12, 13, 14, 15)
            w.config(bg=MIDDLE_FIIL)
            w.place(x=100, y=225-DOWN_GUI)

            panel = Label(root, text="lunch finish hour", font=('calibre', 15), justify='center', bg=MIDDLE_FIIL)
            panel.place(x=240, y=200-DOWN_GUI)
            lft = IntVar(root)
            w = OptionMenu(root, lft, 11, 12, 13, 14, 15, 16, 17)
            w.config(bg=MIDDLE_FIIL)
            w.place(x=280, y=225-DOWN_GUI)

            panel = Label(root, text="lunch duration", font=('calibre', 15), justify='center', bg=MIDDLE_FIIL)
            panel.place(x=445, y=200-DOWN_GUI)
            ld = IntVar(root)
            w = OptionMenu(root, ld, 10, 15, 20, 30, 45, 60)
            w.config(bg=MIDDLE_FIIL)
            w.place(x=480, y=225-DOWN_GUI)

            panel = Label(root, text="break...", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=40-DOWN_GUI-UP_GUI)
            panel = Label(root, text="before", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=80, y=40-DOWN_GUI-UP_GUI)
            panel = Label(root, text="after", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=150, y=40-DOWN_GUI-UP_GUI)
            panel = Label(root, text="meeting", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=80-DOWN_GUI-UP_GUI)
            panel = Label(root, text="task", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=120-DOWN_GUI-UP_GUI)
            panel = Label(root, text="must be", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=160-DOWN_GUI-UP_GUI)

            bbm = IntVar(root)
            bbm.set(0)
            w = OptionMenu(root, bbm, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=80, y=80-DOWN_GUI-UP_GUI)

            bbt = IntVar(root)
            bbt.set(0)
            w = OptionMenu(root, bbt, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=80, y=120-DOWN_GUI-UP_GUI)

            bbmb = IntVar(root)
            bbmb.set(0)
            w = OptionMenu(root, bbmb, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=80, y=160-DOWN_GUI-UP_GUI)

            bam = IntVar(root)
            bam.set(0)
            w = OptionMenu(root, bam, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=150, y=80-DOWN_GUI-UP_GUI)

            bat = IntVar(root)
            bat.set(0)
            w = OptionMenu(root, bat, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=150, y=120-DOWN_GUI-UP_GUI)

            bamb = IntVar(root)
            bamb.set(0)
            w = OptionMenu(root, bamb, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=150, y=160-DOWN_GUI-UP_GUI)

            panel = Label(root, text="start of the day:", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=230, y=40-DOWN_GUI-UP_GUI)
            sotd = IntVar(root)
            sotd.set(8)  # default value
            w = OptionMenu(root, sotd, 6, 7, 8, 9, 10, 11, 12)
            w.config(bg=TOP_FIIL)
            w.place(x=350, y=40-DOWN_GUI-UP_GUI)

            panel = Label(root, text="end of the day:", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=420, y=40-DOWN_GUI-UP_GUI)
            eotd = IntVar(root)
            eotd.set(22)  # default value
            w = OptionMenu(root, eotd, 16, 17, 18, 19, 20, 21, 22, 23, 24)
            w.config(bg=TOP_FIIL)
            w.place(x=535, y=40-DOWN_GUI-UP_GUI)

            sd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='1', variable=sd, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=160, y=290-DOWN_GUI)

            md = tk.IntVar()
            c1 = tk.Checkbutton(root, text='2', variable=md, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=220, y=290-DOWN_GUI)

            tud = tk.IntVar()
            c1 = tk.Checkbutton(root, text='3', variable=tud, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=280, y=290-DOWN_GUI)

            wd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='4', variable=wd, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=340, y=290-DOWN_GUI)

            thd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='5', variable=thd, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=400, y=290-DOWN_GUI)

            Label(root,text="Working days:", font=('calibre', 14), bg=MIDDLE_FIIL).place(x=250,  y=260-DOWN_GUI)

            mact = StringVar(root)
            mact.set(1)
            Label(root, text="meets\nclose\ntogether", font=('calibre', 14), bg=TOP_FIIL).place(x=240, y=90-DOWN_GUI-UP_GUI)
            # mact.set("meetings are close together")  # default value
            w = OptionMenu(root, mact, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=250, y=160-DOWN_GUI-UP_GUI)

            tact = StringVar(root)
            tact.set(1)
            Label(root, text="tasks\nclose\ntogether", font=('calibre', 14), bg=TOP_FIIL).place(x=310, y=90-DOWN_GUI-UP_GUI)
            # tact.set("tasks are close together")  # default value
            w = OptionMenu(root, tact, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=320, y=160-DOWN_GUI-UP_GUI)

            bac = StringVar(root)
            bac.set(1)
            Label(root, text="breaks\nare\ncontinuous", font=('calibre', 14), bg=TOP_FIIL).place(x=375, y=90-DOWN_GUI-UP_GUI)
            # bac.set("breaks are continuous")  # default value
            w = OptionMenu(root, bac, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=390, y=160-DOWN_GUI-UP_GUI)

            fde = StringVar(root)
            fde.set(1)
            # fde.set("finish the day early")  # default value
            Label(root, text="finish\nday\nearly", font=('calibre', 14), bg=TOP_FIIL).place(x=460, y=90-DOWN_GUI-UP_GUI)
            w = OptionMenu(root, fde, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=460, y=160-DOWN_GUI-UP_GUI)

            stdl = StringVar(root)
            stdl.set(1)
            # stdl.set("start the day late")  # default value
            Label(root, text="start\nday\nlate", font=('calibre', 14), bg=TOP_FIIL).place(x=530, y=90-DOWN_GUI-UP_GUI)
            w = OptionMenu(root, stdl, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=530, y=160-DOWN_GUI-UP_GUI)

            def default():
                olmt.set(0)
                olmbt.set(0)
                bbm.set(10)
                bbt.set(10)
                bbmb.set(10)
                bam.set(10)
                bat.set(10)
                bamb.set(10)
                sotd.set(8)
                eotd.set(22)
                sd.set(1)
                md.set(1)
                tud.set(1)
                sd.set(0)
                thd.set(1)
                mact.set(1)
                tact.set(1)
                ld.set(30)
                lft.set(12)
                lst.set(14)
                bac.set(1)
                fde.set(1)
                stdl.set(1)
            def submit_user():
                constraints = Constraints()
                constraints.set_hard_constraint("overlap meeting task", olmt.get())
                constraints.set_hard_constraint("overlap must be task", olmbt.get())
                constraints.set_hard_constraint("break before meeting", Time(m=int(bbm.get())))
                constraints.set_hard_constraint("break before task", Time(m=int(bbt.get())))
                constraints.set_hard_constraint("break before must be", Time(m=int(bbmb.get())))
                constraints.set_hard_constraint("break after meeting", Time(m=int(bam.get())))
                constraints.set_hard_constraint("break after task", Time(m=int(bat.get())))
                constraints.set_hard_constraint("break after must be", Time(m=int(bamb.get())))
                constraints.set_hard_constraint("start of the day", Time(h=int(sotd.get())))
                constraints.set_hard_constraint("end of the day", Time(h=int(eotd.get())))
                constraints.set_hard_constraint("lunch time", (Time(h=lst.get()), Time(h=lft.get()), Time(m=ld.get())))
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
            submit.place(x=460, y=410, width=120, height=70)

            submit = Button(root, text="default", command=default, bd=3, font=('calibre', 25), bg='white')
            submit.place(x=25, y=410, width=120, height=70)

        submit = Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25), bg='white')
        submit.place(x=225, y=310, width=150, height=70)

        # sub_btn = tk.Button(root, text='Submit', command=submit)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
