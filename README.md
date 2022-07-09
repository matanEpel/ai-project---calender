# ai project - calender
AI project for automated calender creation.

Look at the file `"ai project paper.pdf"` for more details and explanation about the project.

##running the code
Firstly, e suggest using `python 3.8` as it is the version we wrote the code with.

Before you run them please install the requirements in the 
requirements file using the command:

`pip install -r requirements.txt`

Then, you can run each file using the command:

`python <file name>`

There are 3 files that includes code you can run:
1. GUI.py
2. benchmarks.py
3. classify.py
 
Here is an explanation for what you should expect when running each of the files:
1. GUI.py - the "core" of the project. As explained in the video and in the paper, 
you have the option to add users and to give them assignments, to create meetings, and the main part - 
   schedule the weeks for all the users together. The GUI comes with 2 default users with 3 shared meetings, 3 must be events and 5
   tasks each. You can edit their constraint in the "create user" page.
   ***NOTE - when running on windows\linux the GUI looks pretty bad. For best performances run over Macos***
2. benchmarks.py - the file we used to create the graphs in the paper. You can use it to test our code easily. Note that the consts in consts.py
was changed a bit for the final product (for the GUI to run smoothly) so the results may be a bit different.
3. classify.py - since the classification of event type used tensoflow and keras which caused problems on our macs (classification part was written on windows but the GUI on mac) - the classification parts was
not incorporated into the GUI. So, in order to check it simply run the classify.py file and the result is self explainable.