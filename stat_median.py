"""
        Author: Spencer Little (mrlittle@uw.edu)
        Last edit: 01/06/2020
        Computes median and average over a set of URLs using pythons standard library statistics module.
"""

import re
import statistics
import sys

def compute_stats(file_urls):
    """
    Facillitates the processing of each URL passed by the user. Returns: average age, (median age, name of person with median age), total lines processed).
    """
    all_ages = []
    age_name = {}
    for url in file_urls:
        process_file(url, all_ages, age_name)

    med = statistics.median(all_ages)
    med_data = (med, age_name[med][0]) if age_name[med] != None else (med, "There is no entity with the median age in the provided data.")

    return round(statistics.mean(all_ages), 2), med_data, len(all_ages)


def process_file(url, all_ages, age_name):
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

    process_lines(url, lines, all_ages, age_name)

def process_lines(url, lines, all_ages, age_name):
    """
    Processes one URL by iterating through each line in the file, adding age to the cumulative list and name to the name-age dict, then returning the total age in years of all lines and the total lines processed.
    """
    form = process_head(lines[0].strip("\n"))
    if (form == None):
        print("File at", url, " improperly formatted. Skipping...\n")
        return 0, 0
    lformat = build_regex(form)
    line_num = 1 # already processed line 1
    total_age = 0
    while (line_num < len(lines)):
        line = lines[line_num]
        if (re.search(lformat, line) == None):
            print("Inproperly formatted input in url, ", url, ", at line ", line_num + 1, ": \n", line)
            line_num += 1
            continue
        udata = line.split(",")
        add_datapoint(age_name, all_ages, udata, form)
        line_num += 1

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

def add_datapoint(age_name, all_ages, udata, form):
    """
    Extracts line data, updates the age-name pair in the provided dictionary and adds the age to the cumulative list.
    """
    age = int(udata[form["age"]])
    name = udata[form["lname"]].strip("\n") + ", " + udata[form["fname"]].strip("\n")
    if (age in age_name): # maintain dict { age - [names...] }
        age_name[age].append(name)
    else:
        age_name.update({age : [name]})
    all_ages.append(age)

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


if __name__=='__main__':
    file_urls = [url for url in sys.argv[1:]]
    avg, med, procd = compute_stats(file_urls)
    print("-"*30, "\nResults:\n")
    print("Average age:", avg, "yrs")
    print("Median age:", med[0], "yrs")
    print("Median entity:", med[1])
    print("Processed:", procd, "lines")
