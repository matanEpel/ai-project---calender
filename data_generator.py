import random
import names
import numpy as np
import pandas as pd
import xlsxwriter
import re
from tqdm import tqdm

from consts import kinds, topics


def generate_names(n):
    return [generate_name() for i in range(n)]


def generate_name():
    if random.random() > 0.5:
        return names.get_full_name()
    return names.get_first_name()


def generate_topic_from_sheet(worksheet):
    xls = pd.ExcelFile('data_generation/topics.xlsx')
    df = pd.read_excel(xls, worksheet)
    return df.sample().values[0]


def generate_random_topic():
    rand_worksheet = random.choice(list(topics.values()))
    return generate_topic_from_sheet(rand_worksheet)


def get_random_line_from_file(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        return random.choice(lines)


def handle_percentage(line):
    word = [t for t in line.split() if t.startswith('%')][0]
    if word == "%":
        replacement = generate_random_topic()[0]
    else:
        tops = word[1:].split("_")
        replacement = random.choice([generate_topic_from_sheet(topics[top]) for top in tops])[0]
    return line.replace(word, replacement, 1)


def handle_line(line):
    # replace names
    while line.count("$") > 0:
        line = line.replace("$", generate_name(), 1)
    while line.count("%") > 0:
        line = handle_percentage(line)
    return line


def generate_length(i):
    if i == 0:
        return 0.25 * int(np.random.rayleigh(2 * np.sqrt(2 / np.pi), 1)[0])
    if i == 1:
        return 0.25 * int(np.random.rayleigh(4 * np.sqrt(2 / np.pi), 1)[0]) + 0.25
    if i == 2:
        return 0.25 * int(np.random.rayleigh(6 * np.sqrt(2 / np.pi), 1)[0]) + 0.25


def generate_title(i):
    if i == 0:
        return handle_line(get_random_line_from_file("data_generation/Task_Format.txt"))
    if i == 1:
        return handle_line(get_random_line_from_file("data_generation/Meeting_Format.txt"))
    if i == 2:
        return handle_line(get_random_line_from_file("data_generation/MustDo_Format.txt"))


def generate_data():
    i = random.choice([0, 1, 2])
    return i, generate_title(i), generate_length(i)


def write_to_excel(n):
    workbook = xlsxwriter.Workbook('generated_data.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "TYPE")
    worksheet.write(0, 1, "TITLE")
    worksheet.write(0, 2, "LENGTH")
    worksheet.write(0, 3, "LABEL")

    for i in tqdm(range(1, n)):
        k = random.choice(list(kinds.keys()))
        j = kinds[k]
        worksheet.write(i, 0, k)
        worksheet.write(i, 1, generate_title(j))
        worksheet.write(i, 2, generate_length(j))
        worksheet.write(i, 3, j)
    workbook.close()


write_to_excel(500000)