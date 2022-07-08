import logging
from datetime import datetime

kinds = {"TASK": 0, "MEETING": 1, "MUST_BE_IN": 2, "LUNCH": 3}
topics = {"CN": "Course Name", "SP": "Sports", "CO": "Country Names", "TO": "General Topics", "MU": "Music Genres",
          "WO": "Work Related"}
DAYS = 7
HOURS = 24
QUARTERS = 4
EPOCHS=4
MIDDLE_OUT = "#1CC0DA"
MIDDLE_FIIL = "#A0E5F0"
TOP_OUT = "#C551E1"
TOP_FIIL = "#F0C4FA"
BUTTON_OUT = "#E53F5D"
BUTTON_FILL = "#EEBAC3"
TITLE_COLOR = "black"
EXPORT_COLOR = "#B676EA"
DOWN_GUI = -30
UP_GUI = 15
THRESHOLD_LOT_OF_MEETS = 7
MIN_DIFFERENCE = 0.01
AMOUNT_STARTING_POINTS = 7
GENETIC_EPOCHS = 10
AMOUNT_TO_DIVIDE = 10
LOG_LEVEL = logging.DEBUG
BASELINE_DAY = datetime.strptime("2022-7-3-+0200", "%Y-%m-%d-%z")
GOOGLE_COLORS = {0: 3, 1: 11, 2: 7, 3: 2}
