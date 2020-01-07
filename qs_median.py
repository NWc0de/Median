"""
        Author: Spencer Little (mrlittle@uw.edu)
        Last edit: 01/06/2020
        A module that reads personal data from csv files and reports median and average statistics using quickselect.
"""

from math import floor
from random import randint
import re
import sys


def compute_stats(file_urls):
    """
    Facillitates the processing of each URL passed by the user. Returns: average age, (median age, name of person with median age), total lines processed).
    """
    file_data = []
    lines_procd = 0
    clm_age = 0
    for url in file_urls:
        total, processed = process_file(url, file_data)
        clm_age += total
        lines_procd += processed
    avg = 0 if lines_procd == 0 else clm_age/lines_procd

    return round(avg, 2), get_median(file_data), lines_procd

def get_median(file_data):
    """
    Computes median and name of entity with median age (if one exists) using QuickSelect on the provided list. Assumes input is list of tuples (age, name).
    """
    if (len(file_data) % 2 == 0):
        med1 = quickselect(file_data, 0, len(file_data) - 1, int(len(file_data)/2))
        med2 = quickselect(file_data, 0, len(file_data) - 1, int((len(file_data)/2) + 1))
        med = (med1[0] + med2[0]) / 2
        med_data = med1 if med == med1[0] else (med, "No entity with true median exists in the list")
    else:
        med_data = quickselect(file_data, 0, len(file_data) - 1, floor(len(file_data)/2))

    return med_data


def process_file(url, file_data):
    """
    Reads all lines from the provided url and passes the resulting list to process_lines for further processing.
    """
    lines = []
    try:
        with open(url, 'r') as filein:
            lines = filein.readlines()
    except FileNotFoundError:
        print("Unable to find url", url, ". Skipping...")
        return (0, 0)
    except OSError as err:
        print("System error while reading file: ", err)
    except:
        print("Unknown error:", sys.exc_info()[1])

    return process_lines(url, lines, file_data)

def process_lines(url, lines, file_data):
    """
    Reads each line in the lines list, checks input format, then appends a new age-name tuple to the cumulative list of file data. Returns cumulative age of every entry in lines and the number of lines processed.
    """
    form = process_head(lines[0].strip("\n"))
    if (form == None):
        print("File at", url, " improperly formatted. Skipping...\n")
        return 0, 0

    lformat = build_regex(form)
    line_num = 1 # already processed line 1
    lines_procd = 0
    total_age = 0
    while (line_num < len(lines)):
        line = lines[line_num]
        if (re.search(lformat, line) == None):
            print("Inproperly formatted input in url, ", url, ", at line ", line_num + 1, ": \n", line)
            line_num += 1
            continue
        udata = line.split(",")
        age = int(udata[form["age"]])
        name = udata[form["lname"]] + ", " + udata[form["fname"]]
        file_data.append((age, name))
        line_num += 1
        lines_procd += 1
        total_age += age

    return total_age, lines_procd

def build_regex(form):
    """Constructs a regex for validation of lines based on the form provided."""
    reg = r"(?i)^"
    for i in range(3):
        elem = list(form.keys())[list(form.values()).index(i)]
        if (elem != "age"):
            reg += r"( ?\w{2,20})"
        else:
            reg += r"( ?\d{1,3})"
        if (i < 2):
            reg += "\,"

    return reg + "$"

def process_head(header):
    """
    Processes the first line of the provided CSV file and returns a dictionary corresponding the order of the lname, fname, and age parameters.
    """
    fdict = {}
    hformat = r"(?i)^( ?\w{2,20}\,){2} ?\w{2,20}$"
    if (re.search(hformat, header) == None):
        return None
    params = [p.strip(" ") for p in header.split(",")]
    try:
        fdict.update({"age" : params.index("age")})
        fdict.update({"fname" : params.index("fname")})
        fdict.update({"lname" : params.index("lname")})
    except ValueError:
        return None

    return fdict

def quickselect(arr, l, r, k):
    """Parition based selection algorithm derived from QuickSort."""
    while (l != r):
        pivind = partition(arr, l, r)

        if (k == pivind):
            return arr[k]
        elif (k > pivind):
            l = pivind + 1
        else:
            r = pivind - 1

    return arr[l]

def partition(arr, l, r):
    """Partitions a list around a random element."""
    pivind = randint(l, r)
    swap(arr, pivind, r)
    piv = arr[r] # pivot element is rightmost - shuffle ?
    lind = l
    for x in range(l, r):
        if (arr[x][0] <= piv[0]):
            swap(arr, x, lind)
            lind+=1
    swap(arr, lind, r)
    return lind


def swap(arr, i, j):
    """A helper method that swaps two elements in an array."""
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp




if __name__=='__main__':
    file_urls = [url for url in sys.argv[1:]]
    avg, med, procd = compute_stats(file_urls)
    print("-"*30, "\nResults:\n")
    print("Average age:", avg, "yrs")
    print("Median age:", med[0], "yrs")
    print("Median entity:", med[1])
    print("Processed:", procd, "lines")
