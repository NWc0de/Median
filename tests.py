"""
        Author: Spencer Little
        Last edit: 01/05/2020
        Computes median and average over a set of URLs using pythons standard library statistics module, then compares with heap_median and qs_median.
"""

import heap_median
import qs_median
import stat_median
import re
import statistics
import sys

def compute_stats(file_urls):
    """
    Facillitates the processing of each URL passed by the user. Returns: average age, (median age, name of person with median age), total lines processed).
    """
    all_ages = []
    for url in file_urls:
        process_file(url, all_ages)

    return round(statistics.mean(all_ages), 2), statistics.median(all_ages), len(all_ages)


def process_file(url, all_ages):
    """
    Processes one URL by iterating through each line in the file, adding a tuple of (age, name) to the respective set of heaps, and returning the total age in years of all lines and the total lines processed.
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

    process_lines(url, lines, all_ages)

def process_lines(url, lines, all_ages):
    """
    Reads each line in the lines list, checks input format, then inserts
    a new age-name pair into the set of median heaps if the format is valid. Returns cumulative age of every entry in lines and the number of lines processed.
    """
    lformat = r"(?i)^( ?\w{2,20}\,){2} ?\d{1,3}$" # (0-1 spaces, 2-20 chars, a comma)x2 then 0-1 spaces, 1-3 digits
    form = process_head(lines[0].strip("\n"))
    if (form == None):
        print("File at", url, " improperly formatted. Skipping...\n")
        return 0, 0
    line_num = 1 # already processed line 1
    total_age = 0
    while (line_num < len(lines)):
        line = lines[line_num]
        if (re.search(lformat, line) == None):
            print("Inproperly formatted input in url, ", url, ", at line ", line_num + 1, ": \n", line)
            line_num += 1
            continue
        udata = line.split(",")
        age = int(udata[form["age"]])
        all_ages.append(age)
        line_num += 1

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
    tavg, tmed, tprocd = compute_stats(file_urls)
    savg, smed, sprocd = stat_median.compute_stats(file_urls)
    havg, hmed, hprocd = heap_median.compute_stats(file_urls)
    qavg, qmed, qprocd = qs_median.compute_stats(file_urls)
    print("-"*30, "\nResults:\n")
    print("Average test passed: ", (tavg==havg and havg==qavg and qavg==savg))
    print("Median test passed: ", (tmed==hmed[0]) and hmed[0]==qmed[0] and qmed[0]==smed[0])
    print("-"*30)
    print("Python std library - statistics results:\n")
    print("Average: ", tavg, " Median: ", tmed)
    print("-"*30)
    print("Heap results:\n")
    print("Average: ", havg, " Median: ", hmed[0])
    print("-"*30)
    print("QuickSelect results:\n")
    print("Average: ", qavg, " Median: ", qmed[0])
    print("-"*30)
    print("TimSort (same of std library - statistics) resutls:")
    print("Average: ", savg, " Median: ", smed[0])
