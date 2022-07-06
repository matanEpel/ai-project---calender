import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import tkmacosx
from assignment import Assignment
from constraint import Constraints
from consts import MIDDLE_OUT, MIDDLE_FIIL, DOWN_GUI, UP_GUI, TOP_FIIL, TOP_OUT, BUTTON_OUT, BUTTON_FILL, TITLE_COLOR, \
    kinds
from manager import Manager
from user import User
from time_ import Time


def default_users(manager):
    c = Constraints()
    c.set_soft_constraint("meetings are close together", 10000)
    # c.set_soft_constraint("meetings are close together", 100)
    c.set_soft_constraint("start the day late", 3000)
    # c.set_soft_constraint("breaks are continuous", -100)
    ofir = User("Ofir", c)
    matan = User("matan", c)
    amit = User("amit", c)

    a1 = Assignment(week=1, name="ex1", duration=Time(h=1), kind=kinds["TASK"], day=3,time=Time(h=10, m=30))
    a2 = Assignment(week=1, name="ex2", duration=Time(h=1), kind=kinds["TASK"], day=3,time=Time(h=12, m=30))
    a3 = Assignment(week=1, name="ex3", duration=Time(h=0,m=45), kind=kinds["TASK"], day=3,time=Time(h=16, m=30))
    a4 = Assignment(week=1, name="ex4", duration=Time(h=1), kind=kinds["TASK"], day=3,time=Time(h=19, m=30))
    a5 = Assignment(week=1, name="ex5", duration=Time(h=1), kind=kinds["TASK"], day=4,time=Time(h=10, m=30))
    a6 = Assignment(week=1, name="ex6", duration=Time(h=2), kind=kinds["TASK"], day=4, time=Time(h=20, m=30))
    a7 = Assignment(week=1, name="ex7", duration=Time(h=1), kind=kinds["TASK"], day=4, time=Time(h=22, m=30))
    a8 = Assignment(week=1, name="ex8", duration=Time(h=2), kind=kinds["TASK"], day=4, time=Time(h=13, m=30))
    a9 = Assignment(week=1, name="ex9", duration=Time(h=1), kind=kinds["TASK"], day=5, time=Time(h=10, m=30))
    a10 = Assignment(week=1, name="ex10", duration=Time(h=1), kind=kinds["TASK"], day=5, time=Time(h=12, m=30))
    a11 = Assignment(week=1, name="ex11", duration=Time(h=5), kind=kinds["TASK"], day=5, time=Time(h=13, m=30))

    b1 = Assignment(week=1, name="m1", duration=Time(h=2), kind=kinds["MEETING"], participants=[ofir], day=4,
                    time=Time(h=19, m=15))
    a12 = Assignment(week=1, name="ex12", duration=Time(h=5), kind=kinds["MUST_BE_IN"], day=1, time=Time(h=6, m=0))
    a13 = Assignment(week=1, name="ex13", duration=Time(h=1), kind=kinds["MUST_BE_IN"], day=1, time=Time(h=11, m=0))
    # a14 = Assignment(week=1, name="ex14", duration=Time(h=2), kind=kinds["LUNCH"], day=1, time=Time(h=12, m=30))
    # a11 = Assignment(week=1, name="ex15", duration=Time(h=5), kind=kinds["MUST_BE_IN"], day=5, time=Time(h=6, m=0))
    # a11 = Assignment(week=1, name="ex16", duration=Time(h=5), kind=kinds["MUST_BE_IN"], day=5, time=Time(h=6, m=0))
    # a11 = Assignment(week=1, name="ex17", duration=Time(h=5), kind=kinds["MUST_BE_IN"], day=5, time=Time(h=6, m=0))
    b2 = Assignment(week=1, name="m2", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir], day=3,
                    time=Time(h=21, m=0))
    b3 = Assignment(week=1, name="m3", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir], day=3,
                    time=Time(h=15, m=0))
    b4 = Assignment(week=1, name="m4", duration=Time(h=2), kind=kinds["MEETING"], participants=[ofir], day=3,
                    time=Time(h=17, m=0))
    b5 = Assignment(week=1, name="m5", duration=Time(h=2), kind=kinds["MEETING"], participants=[ofir], day=4,
                    time=Time(h=15, m=0))
    b6 = Assignment(week=1, name="m6", duration=Time(h=2), kind=kinds["MEETING"], participants=[ofir], day=5,
                    time=Time(h=10, m=0))
    b7 = Assignment(week=1, name="m7", duration=Time(h=2), kind=kinds["MEETING"], participants=[ofir], day=5,
                    time=Time(h=14, m=30))
    mb1 = Assignment(week=1, name="mb1", duration=Time(h=2, m=30), kind=kinds["MUST_BE_IN"], day=1,
                     time=Time(h=9, m=30))
    mb2 = Assignment(week=1, name="mb2", duration=Time(h=2), kind=kinds["MUST_BE_IN"], day=2, time=Time(h=17, m=0))
    mb3 = Assignment(week=1, name="mb3", duration=Time(h=2), kind=kinds["MUST_BE_IN"], day=1, time=Time(h=22, m=0))

    ofir.add_assignment(a1)
    ofir.add_assignment(a2)
    ofir.add_assignment(a3)
    ofir.add_assignment(a4)
    ofir.add_assignment(a5)
    ofir.add_assignment(a6)
    # ofir.add_assignment(a7)
    # ofir.add_assignment(a8)
    # ofir.add_assignment(a9)
    # ofir.add_assignment(a10)
    # ofir.add_assignment(a11)
    # ofir.add_assignment(a12)
    # ofir.add_assignment(a13)
    # ofir.add_assignment(a14)
    ofir.add_assignment(mb1)
    ofir.add_assignment(mb2)
    ofir.add_assignment(b1)
    ofir.add_assignment(b2)
    ofir.add_assignment(b3)
    ofir.add_assignment(b4)
    ofir.add_assignment(b5)
    # ofir.add_assignment(b6)
    # ofir.add_assignment(b7)
    # ofir.add_assignment(b4)
    # print(ofir.schedule_week(1))
    # print(ofir)
    manager.add_user(ofir)


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
            points.append((ratioMultiplier * x[i] + x[i + 1]) / ratioDividend)
            points.append((ratioMultiplier * y[i] + y[i + 1]) / ratioDividend)
            points.append((ratioMultiplier * x[i + 1] + x[i]) / ratioDividend)
            points.append((ratioMultiplier * y[i + 1] + y[i]) / ratioDividend)
        else:
            # Insert submultiples points.
            points.append((ratioMultiplier * x[i] + x[0]) / ratioDividend)
            points.append((ratioMultiplier * y[i] + y[0]) / ratioDividend)
            points.append((ratioMultiplier * x[0] + x[i]) / ratioDividend)
            points.append((ratioMultiplier * y[0] + y[i]) / ratioDividend)
            # Close the polygon
            points.append(x[0])
            points.append(y[0])

    return canvas.create_polygon(points, **kwargs, smooth=TRUE)


class App:
    def __init__(self, root):
        self.__manager = Manager()
        default_users(self.__manager)
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

        canvas = Canvas(root, width=610, height=500, bg="black")
        roundPolygon(canvas, [90 + 10, 505 + 10, 505 + 10, 90 + 10], [80, 80, 200, 200], 10,
                     width=5, outline=TOP_OUT, fill=TOP_FIIL)

        FIRST = 100
        SEC = 350
        roundPolygon(canvas, [15 + 10 + FIRST, 150 + FIRST + 10, 15 + 10 + FIRST], [280, 325, 370], 8, width=5,
                     outline=BUTTON_OUT,
                     fill=BUTTON_FILL)
        roundPolygon(canvas, [15 + 10 + SEC, 150 + SEC + 10, 15 + 10 + SEC], [280, 325, 370], 8, width=5,
                     outline=BUTTON_OUT,
                     fill=BUTTON_FILL)
        canvas.place(x=0 - 10, y=0)

        panel = Label(root, text="All users", font=('calibre', 30), bg=TITLE_COLOR, justify='center', fg="white")
        panel.place(x=0, y=0, width=600)

        users = {}
        for u in self.__manager.get_users():
            users[u.get_name()] = u

        bamb = StringVar(root)
        bamb.set("none")
        Label(root, text="The user you want to look at:", font=('calibre', 25), bg=TOP_FIIL, justify='center').place(
            x=100, y=100)
        w = OptionMenu(root, bamb, "none", *(users.keys()))
        w.config(bg=TOP_FIIL)
        w.place(x=430, y=108)

        week_var = StringVar(root)
        Label(root, text="The week you want to look at:", font=('calibre', 25), bg=TOP_FIIL, justify='center').place(
            x=100, y=150)
        weeks = set()
        for u in self.__manager.get_users():
            for ass in u.get_all_assignments():
                weeks.add(ass.get_week())
        week_var.set("none")
        w = OptionMenu(root, week_var, "none", *(weeks))
        w.config(bg=TOP_FIIL)
        w.place(x=430, y=158)

        def submit_func():
            # TODO: look good
            if bamb.get() == "none" or bamb.get() == "CHOOSE THE USER YOU WANT TO LOOK AT":
                self.home()
                return
            for ele in root.winfo_children():
                ele.destroy()
            self.add_menu()
            user = None
            name = bamb.get()
            for u in self.__manager.get_users():
                if u.get_name() == name:
                    user = u
            week = int(week_var.get())
            if not user.has_schedule(week):
                canvas = Canvas(root, width=610, height=500, bg="black")
                roundPolygon(canvas, [220, 420, 420, 220], [10, 10, 450, 450], 8, width=5,
                             outline=TOP_OUT,
                             fill=TOP_FIIL)
                canvas.place(x=-10, y=40)
                panel = Label(root, text=bamb.get() + "'s assignments - haven't scheduled yet :)", font=('calibre', 30),
                              bg=TITLE_COLOR, justify='center', fg="white")
                panel.place(x=0, y=0, width=600)

                i = 0
                count = 0
                for ass in user.get_assignments(week):
                    count += 1
                    panel = Label(root, text=str(count) + ". " + ass.get_name() + ", duration: " + str(
                        str(ass.get_duration())), font=('calibre', 15),
                                  bg=TOP_FIIL, justify='center')
                    panel.place(x=235, y=70 + i * 30)
                    i += 1
            else:
                self.calender_page(user, week)

        submit = tkmacosx.Button(root, text="GO!", command=submit_func, bd=3, font=('calibre', 13),
                                 highlightbackground=BUTTON_FILL)
        submit.config(bg=BUTTON_FILL)
        submit.place(x=120, y=310, width=70, height=30)

        def schedule():
            # TODO: look good
            for week in weeks:
                print("week " + str(week) + " was scheduled!")
                self.__manager.schedule_week(week)

        submit = tkmacosx.Button(root, text="SCHEDULE!", command=schedule, bd=3, font=('calibre', 13),
                                 highlightbackground=BUTTON_FILL)
        submit.config(bg=BUTTON_FILL)
        submit.place(x=370, y=310, width=78, height=30)

    def add_assignment(self):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()

        canvas = Canvas(root, width=610, height=500, bg="black", bd=0, relief='ridge')
        roundPolygon(canvas, [140 + 10, 460 + 10, 460 + 10, 140 + 10], [160, 160, 290, 290], 10,
                     width=5, outline="#82B366", fill="#D5E8D4")
        WIDTH = 215
        HEIGHT = 69
        roundPolygon(canvas, [15 + WIDTH, 150 + WIDTH + 10, 15 + WIDTH],
                     [280 + HEIGHT - 10, 325 + HEIGHT, 370 + HEIGHT + 10], 8, width=5,
                     outline=BUTTON_OUT,
                     fill=BUTTON_FILL)
        canvas.place(x=-10, y=0)

        panel = Label(root, text="Add assignment to user", font=('calibre', 30), bg=TITLE_COLOR, justify='center',
                      fg='white')
        panel.place(x=0, y=0, width=600)

        name_var = tk.StringVar()
        e1 = tk.Entry(root, textvariable=name_var, bd=0, font=('calibre', 25), justify='center', bg="#D5E8D4",
                      highlightbackground="black", highlightthickness=2)
        e1.place(x=155, y=220, width=290, height=50)

        panel = Label(root, text="enter user name:", font=('calibre', 30), bg="#D5E8D4")
        panel.place(x=180, y=170)

        def submit_func():
            # TODO: look good
            name = name_var.get()
            for ele in root.winfo_children():
                ele.destroy()
            self.add_menu()

            canvas = Canvas(root, width=610, height=500, bg="black")
            C_H = 20
            roundPolygon(canvas, [60 + 10, 280 + 10, 280 + 10, 60 + 10], [120 - C_H, 120 - C_H, 340 - C_H, 340 - C_H],
                         10,
                         width=5, outline=TOP_OUT, fill=TOP_FIIL)
            roundPolygon(canvas, [60 + 260 + 10, 280 + 260 + 10, 280 + 260 + 10, 60 + 260 + 10],
                         [120 - C_H, 120 - C_H, 340 - C_H, 340 - C_H], 10,
                         width=5, outline=MIDDLE_OUT, fill=MIDDLE_FIIL)
            WIDTH = 215
            HEIGHT = 69
            roundPolygon(canvas, [15 + WIDTH, 150 + WIDTH + 10, 15 + WIDTH],
                         [280 + HEIGHT - 10, 325 + HEIGHT, 370 + HEIGHT + 10], 8, width=5,
                         outline=BUTTON_OUT,
                         fill=BUTTON_FILL)
            canvas.place(x=-10, y=0)

            panel = Label(root, text="Assignment metadata", font=('calibre', 30), justify='center', bg=TITLE_COLOR,
                          fg="white")
            panel.place(x=0, y=0, width=600)

            ass_name_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_name_var, bd=0, font=('calibre', 20), justify='center', bg=TOP_FIIL,
                          highlightbackground="black", highlightthickness=2)
            e1.place(x=70, y=170 - C_H, width=200, height=50)

            panel = Label(root, text="name:", font=('calibre', 20), bg=TOP_FIIL)
            panel.place(x=140, y=130 - C_H)

            ass_length_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_length_var, bd=0, font=('calibre', 20), justify='center', bg=TOP_FIIL,
                          highlightbackground="black", highlightthickness=2)
            e1.place(x=70, y=270 - C_H, width=200, height=50)

            panel = Label(root, text="length:", font=('calibre', 20), bg=TOP_FIIL)
            panel.place(x=135, y=230 - C_H)

            ass_week_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_week_var, bd=0, font=('calibre', 20), justify='center', bg=MIDDLE_FIIL,
                          highlightbackground="black", highlightthickness=2)
            e1.place(x=330, y=170 - C_H, width=200, height=50)

            panel = Label(root, text="week:", font=('calibre', 20), bg=MIDDLE_FIIL)
            panel.place(x=400, y=130 - C_H)

            ass_part_var = tk.StringVar()
            e1 = tk.Entry(root, textvariable=ass_part_var, bd=0, font=('calibre', 20), justify='center', bg=MIDDLE_FIIL,
                          highlightbackground="black", highlightthickness=2)
            e1.place(x=330, y=270 - C_H, width=200, height=50)

            panel = Label(root, text="participants:", font=('calibre', 20), bg=MIDDLE_FIIL)
            panel.place(x=380, y=230 - C_H)

            def submit_func_ass():
                print(1)
                if name in [u.get_name() for u in self.__manager.get_users()]:
                    user = None
                    for u in self.__manager.get_users():
                        if u.get_name() == name:
                            user = u

                    partici = []
                    print(partici)
                    for part in ass_part_var.get().split(", "):
                        curr_user = None
                        for u in self.__manager.get_users():
                            if u.get_name() == part:
                                curr_user = u
                        if curr_user:
                            partici.append(curr_user)
                    minutes = int(ass_length_var.get())
                    assignment = Assignment(int(ass_week_var.get()), ass_name_var.get(), Time(h=minutes//60,m=minutes%60),
                                            participants=partici)
                    for part in partici:
                        part.add_assignment(assignment)
                    user.add_assignment(assignment)
                self.home()

            submit = tkmacosx.Button(root, text="Submit", command=submit_func_ass, bd=3, font=('calibre', 25),
                                     highlightbackground=BUTTON_FILL)
            submit.config(bg=BUTTON_FILL)
            submit.place(x=225, y=380, width=90, height=30)

        photo = PhotoImage(file=r"resources/all.png")
        submit = tkmacosx.Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25),
                                 highlightbackground=BUTTON_FILL)
        submit.config(bg=BUTTON_FILL)
        submit.place(x=225, y=380, width=90, height=30)

    def specific_user(self):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()

        canvas = Canvas(root, width=610, height=500, bg="black")
        roundPolygon(canvas, [140 + 10, 460 + 10, 460 + 10, 140 + 10], [160, 160, 290, 290], 10,
                     width=5, outline="#82B366", fill="#D5E8D4")
        WIDTH = 215
        HEIGHT = 69
        roundPolygon(canvas, [15 + WIDTH, 150 + WIDTH + 10, 15 + WIDTH],
                     [280 + HEIGHT - 10, 325 + HEIGHT, 370 + HEIGHT + 10], 8, width=5,
                     outline=BUTTON_OUT,
                     fill=BUTTON_FILL)
        canvas.place(x=0 - 10, y=0)

        panel = Label(root, text="Edit\\add user", font=('calibre', 30), bg=TITLE_COLOR, justify='center', fg="white")
        panel.place(x=0, y=0, width=600)

        name_var = tk.StringVar()
        e1 = tk.Entry(root, textvariable=name_var, bd=0, font=('calibre', 25), justify='center', bg="#D5E8D4",
                      highlightbackground="black", highlightthickness=2)
        e1.place(x=155, y=220, width=290, height=50)

        panel = Label(root, text="enter user name:", font=('calibre', 30), bg="#D5E8D4")
        panel.place(x=180, y=170)

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

            canvas = Canvas(root, width=610, height=500, bg="black")
            roundPolygon(canvas, [170 + 10, 440 + 10, 440 + 10, 170 + 10],
                         [340 - DOWN_GUI, 340 - DOWN_GUI, 425 - DOWN_GUI, 425 - DOWN_GUI],
                         10, width=5, outline="#82B366", fill="#D5E8D4")
            roundPolygon(canvas, [50 + 10, 560 + 10, 560 + 10, 50 + 10],
                         [190 - DOWN_GUI, 190 - DOWN_GUI, 320 - DOWN_GUI, 320 - DOWN_GUI],
                         10, width=5, outline=MIDDLE_OUT, fill=MIDDLE_FIIL)
            roundPolygon(canvas, [10 + 10, 590 + 10, 590 + 10, 10 + 10],
                         [60 - UP_GUI, 60 - UP_GUI, 220 - UP_GUI, 220 - UP_GUI], 10,
                         width=5, outline=TOP_OUT, fill=TOP_FIIL)
            roundPolygon(canvas, [15 + 10, 150 + 10, 15 + 10], [400, 445, 490], 8, width=5, outline=BUTTON_OUT,
                         fill=BUTTON_FILL)
            roundPolygon(canvas, [445 + 15 + 10, 445 + 150 + 10, 445 + 15 + 10], [400, 445, 490], 8, width=5,
                         outline=BUTTON_OUT,
                         fill=BUTTON_FILL)
            canvas.place(x=0 - 10, y=0)

            panel = Label(root, text="Edit\\create " + name + "'s data", font=('calibre', 30), justify='center',
                          bg=TITLE_COLOR, fg="white")
            panel.place(x=0, y=0, width=600)
            print(name)

            olmt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap meeting and task', variable=olmt, onvalue=1, offvalue=0,
                                font=('calibre', 18), bg="#D5E8D4")
            c1.place(x=190, y=350 - DOWN_GUI)

            olmbt = tk.IntVar()
            c1 = tk.Checkbutton(root, text='overlap must be and task', variable=olmbt, onvalue=1, offvalue=0,
                                font=('calibre', 18), bg="#D5E8D4")
            c1.place(x=190, y=390 - DOWN_GUI)

            panel = Label(root, text="lunch start hour", font=('calibre', 15), justify='center', bg=MIDDLE_FIIL)
            panel.place(x=60, y=200 - DOWN_GUI)
            lst = IntVar(root)
            w = OptionMenu(root, lst, 10, 11, 12, 13, 14, 15)
            w.config(bg=MIDDLE_FIIL)
            w.place(x=100, y=225 - DOWN_GUI)

            panel = Label(root, text="lunch finish hour", font=('calibre', 15), justify='center', bg=MIDDLE_FIIL)
            panel.place(x=240, y=200 - DOWN_GUI)
            lft = IntVar(root)
            w = OptionMenu(root, lft, 11, 12, 13, 14, 15, 16, 17)
            w.config(bg=MIDDLE_FIIL)
            w.place(x=280, y=225 - DOWN_GUI)

            panel = Label(root, text="lunch duration", font=('calibre', 15), justify='center', bg=MIDDLE_FIIL)
            panel.place(x=445, y=200 - DOWN_GUI)
            ld = IntVar(root)
            w = OptionMenu(root, ld, 10, 15, 20, 30, 45, 60)
            w.config(bg=MIDDLE_FIIL)
            w.place(x=480, y=225 - DOWN_GUI)

            panel = Label(root, text="break...", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=40 - DOWN_GUI - UP_GUI)
            panel = Label(root, text="before", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=80, y=40 - DOWN_GUI - UP_GUI)
            panel = Label(root, text="after", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=150, y=40 - DOWN_GUI - UP_GUI)
            panel = Label(root, text="meeting", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=80 - DOWN_GUI - UP_GUI)
            panel = Label(root, text="task", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=120 - DOWN_GUI - UP_GUI)
            panel = Label(root, text="must be", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=20, y=160 - DOWN_GUI - UP_GUI)

            bbm = IntVar(root)
            bbm.set(0)
            w = OptionMenu(root, bbm, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=80, y=80 - DOWN_GUI - UP_GUI)

            bbt = IntVar(root)
            bbt.set(0)
            w = OptionMenu(root, bbt, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=80, y=120 - DOWN_GUI - UP_GUI)

            bbmb = IntVar(root)
            bbmb.set(0)
            w = OptionMenu(root, bbmb, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=80, y=160 - DOWN_GUI - UP_GUI)

            bam = IntVar(root)
            bam.set(0)
            w = OptionMenu(root, bam, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=150, y=80 - DOWN_GUI - UP_GUI)

            bat = IntVar(root)
            bat.set(0)
            w = OptionMenu(root, bat, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=150, y=120 - DOWN_GUI - UP_GUI)

            bamb = IntVar(root)
            bamb.set(0)
            w = OptionMenu(root, bamb, 0, 5, 10, 15, 20)
            w.config(bg=TOP_FIIL)
            w.place(x=150, y=160 - DOWN_GUI - UP_GUI)

            panel = Label(root, text="start of the day:", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=230, y=40 - DOWN_GUI - UP_GUI)
            sotd = IntVar(root)
            sotd.set(8)  # default value
            w = OptionMenu(root, sotd, 6, 7, 8, 9, 10, 11, 12)
            w.config(bg=TOP_FIIL)
            w.place(x=350, y=40 - DOWN_GUI - UP_GUI)

            panel = Label(root, text="end of the day:", font=('calibre', 15), justify='center', bg=TOP_FIIL)
            panel.place(x=420, y=40 - DOWN_GUI - UP_GUI)
            eotd = IntVar(root)
            eotd.set(22)  # default value
            w = OptionMenu(root, eotd, 16, 17, 18, 19, 20, 21, 22, 23, 24)
            w.config(bg=TOP_FIIL)
            w.place(x=535, y=40 - DOWN_GUI - UP_GUI)

            sd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='1', variable=sd, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=160, y=290 - DOWN_GUI)

            md = tk.IntVar()
            c1 = tk.Checkbutton(root, text='2', variable=md, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=220, y=290 - DOWN_GUI)

            tud = tk.IntVar()
            c1 = tk.Checkbutton(root, text='3', variable=tud, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=280, y=290 - DOWN_GUI)

            wd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='4', variable=wd, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=340, y=290 - DOWN_GUI)

            thd = tk.IntVar()
            c1 = tk.Checkbutton(root, text='5', variable=thd, onvalue=1, offvalue=0,
                                font=('calibre', 14), bg=MIDDLE_FIIL)
            c1.place(x=400, y=290 - DOWN_GUI)

            Label(root, text="Working days:", font=('calibre', 14), bg=MIDDLE_FIIL).place(x=250, y=260 - DOWN_GUI)

            mact = StringVar(root)
            mact.set(1)
            Label(root, text="meets\nclose\ntogether", font=('calibre', 14), bg=TOP_FIIL).place(x=240,
                                                                                                y=90 - DOWN_GUI - UP_GUI)
            # mact.set("meetings are close together")  # default value
            w = OptionMenu(root, mact, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=250, y=160 - DOWN_GUI - UP_GUI)

            tact = StringVar(root)
            tact.set(1)
            Label(root, text="tasks\nclose\ntogether", font=('calibre', 14), bg=TOP_FIIL).place(x=310,
                                                                                                y=90 - DOWN_GUI - UP_GUI)
            # tact.set("tasks are close together")  # default value
            w = OptionMenu(root, tact, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=320, y=160 - DOWN_GUI - UP_GUI)

            bac = StringVar(root)
            bac.set(1)
            Label(root, text="breaks\nare\ncontinuous", font=('calibre', 14), bg=TOP_FIIL).place(x=375,
                                                                                                 y=90 - DOWN_GUI - UP_GUI)
            # bac.set("breaks are continuous")  # default value
            w = OptionMenu(root, bac, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=390, y=160 - DOWN_GUI - UP_GUI)

            fde = StringVar(root)
            fde.set(1)
            # fde.set("finish the day early")  # default value
            Label(root, text="finish\nday\nearly", font=('calibre', 14), bg=TOP_FIIL).place(x=460,
                                                                                            y=90 - DOWN_GUI - UP_GUI)
            w = OptionMenu(root, fde, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=460, y=160 - DOWN_GUI - UP_GUI)

            stdl = StringVar(root)
            stdl.set(1)
            # stdl.set("start the day late")  # default value
            Label(root, text="start\nday\nlate", font=('calibre', 14), bg=TOP_FIIL).place(x=530,
                                                                                          y=90 - DOWN_GUI - UP_GUI)
            w = OptionMenu(root, stdl, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
            w.config(bg=TOP_FIIL)
            w.place(x=530, y=160 - DOWN_GUI - UP_GUI)

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

            submit = tkmacosx.Button(root, text="Submit", command=submit_user, bd=3, font=('calibre', 20),
                                     highlightbackground=BUTTON_FILL, relief=FLAT)
            submit.config(bg=BUTTON_FILL)
            submit.place(x=470, y=430, width=70, height=30)

            submit = tkmacosx.Button(root, text="default", command=default, bd=3, font=('calibre', 20),
                                     highlightbackground=BUTTON_FILL, relief=FLAT)
            submit.config(bg=BUTTON_FILL)
            submit.place(x=25, y=430, width=70, height=30)

        submit = tkmacosx.Button(root, text="Submit", command=submit_func, bd=3, font=('calibre', 25),
                                 highlightbackground=BUTTON_FILL)
        submit.config(bg=BUTTON_FILL)
        submit.place(x=225, y=380, width=90, height=30)

        # sub_btn = tk.Button(root, text='Submit', command=submit)

    def calender_page(self, user, week):
        for ele in root.winfo_children():
            ele.destroy()
        self.add_menu()
        canvas = Canvas(root, width=610, height=500, bg="black")
        canvas.create_line(20, 105, 600, 105,  fill="#C8C9C9", dash=(5,5))
        canvas.create_line(80 + 40, 60, 80 + 40, 490, fill="white")
        canvas.create_line(200 + 40, 60, 200 + 40, 490, fill="white")
        canvas.create_line(320 + 40, 60, 320 + 40, 490, fill="white")
        canvas.create_line(440 + 40, 60, 440 + 40, 490, fill="white")

        canvas.create_line(20, 233-5, 600, 233-5, fill="#C8C9C9", dash=(5,5))
        canvas.create_line(20, 366-5, 600, 366-5, fill="#C8C9C9", dash=(5,5))
        canvas.create_line(20, 470-2, 600, 470-2, fill="#C8C9C9", dash=(5,5))

        for ass in user.get_schedule(week):
            name = ass.get_name()
            day = ass.get_day()
            quarters = ass.get_duration().get_hours() * 4 + ass.get_duration().get_minutes() // 15
            start_quarters = ass.get_time().get_hours() * 4 + ass.get_time().get_minutes() // 15
            kind = ass.get_kind()
            color_dict = {0: (TOP_FIIL, TOP_OUT), 1: (BUTTON_FILL, BUTTON_OUT), 2: (MIDDLE_FIIL, MIDDLE_OUT),
             3: ("#D5E8D4", "#82B366")}
            fill, out = color_dict[kind]
            if day == 1:
                roundPolygon(canvas, [15 + (day - 1) * 120, 15 + (day - 1) * 120 + 100, 15 + (day - 1) * 120 + 100,
                                      15 + (day - 1) * 120],
                             [100 + (start_quarters - 22) * 5, 100 + (start_quarters - 22) * 5,
                              95 + (start_quarters + quarters - 22) * 5, 95 + (start_quarters + quarters - 22) * 5], 10,
                             width=2, outline=out, fill=fill)
            else:
                roundPolygon(canvas, [10+(day-1)*120,10+(day-1)*120+100,10+(day-1)*120+100,10+(day-1)*120], [100+(start_quarters-22)*5,100+(start_quarters-22)*5,95+(start_quarters+quarters-22)*5,95+(start_quarters+quarters-22)*5], 10,
                         width=2, outline=out, fill=fill)

        canvas.place(x=0 - 10, y=0)

        Label(root, text=user.get_name() + "'s week " + str(week) + " calender", font=('calibre', 30), bg="black",
              fg="white").place(x=0, y=0, width=600)
        Label(root, text="Sunday", font=('calibre', 15), bg="black",
              fg="white").place(x=20, y=65)
        Label(root, text="Monday", font=('calibre', 15), bg="black",
              fg="white").place(x=140, y=65)
        Label(root, text="Tuesday", font=('calibre', 15), bg="black",
              fg="white").place(x=260, y=65)
        Label(root, text="Wednesday", font=('calibre', 15), bg="black",
              fg="white").place(x=370, y=65)
        Label(root, text="Thursday", font=('calibre', 15), bg="black",
              fg="white").place(x=490, y=65)
        for ass in user.get_schedule(week):
            name = ass.get_name()
            day = ass.get_day()
            quarters = ass.get_duration().get_hours() * 4 + ass.get_duration().get_minutes() // 15
            start_quarters = ass.get_time().get_hours() * 4 + ass.get_time().get_minutes() // 15
            kind = ass.get_kind()
            color_dict = {0: (TOP_FIIL, TOP_OUT), 1: (BUTTON_FILL, BUTTON_OUT), 2: (MIDDLE_FIIL, MIDDLE_OUT),
             3: ("#D5E8D4", "#82B366")}
            fill, out = color_dict[kind]
            if quarters >= 4:
                if day == 1:
                    x = 15 + (day - 1) * 120
                    y = 100 + (start_quarters - 22) * 5
                    Label(root, text=name, font=('calibre', 8), bg=fill,
                          fg="black").place(x=x, y=y+5, height=8)
                else:
                    x = 10+(day-1)*120
                    y = 100+(start_quarters-22)*5
                    Label(root, text=name, font=('calibre', 8), bg=fill,
                          fg="black").place(x=x, y=y+5, height=8)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
