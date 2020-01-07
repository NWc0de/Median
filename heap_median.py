"""
        Author: Spencer Little (mrlittle@uw.edu)
        Last edit: 01/06/2020
        A module that reads personal data from csv files and reports median and average statistics using the min/max heap algorithm.
"""

from heapq import heappop, heappush
import re
import sys


def compute_stats(file_urls):
    """
    Facillitates the processing of each URL passed by the user. Returns: average age, (median age, name of person with median age), total lines processed).
    """
    min_heap = []
    max_heap = []
    lines_procd = 0
    clm_age = 0
    for url in file_urls:
        total, processed = process_file(url, min_heap, max_heap)
        clm_age += total
        lines_procd += processed
    avg = 0 if lines_procd == 0 else round(clm_age/lines_procd, 2)

    return avg, get_median(min_heap, max_heap), lines_procd


def process_file(url, min_heap, max_heap):
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

    return process_lines(url, lines, min_heap, max_heap)

def process_lines(url, lines, min_heap, max_heap):
    """
    Reads each line in the lines list, checks input format, then inserts
    a new age-name pair into the set of median heaps if the format is valid. Returns cumulative age of every entry in lines and the number of lines processed.
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
        name = udata[form["lname"]].strip("\n") + ", " + udata[form["fname"]].strip("\n")
        insert_age(min_heap, max_heap, age, name)
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

def insert_age(min_heap, max_heap, age, name):
    """Inserts a new age-name pair into the set of min/max heaps."""
    lmax = age+1 if len(max_heap) == 0 else abs(max_heap[0][0])
    if (age<=lmax):
        heappush(max_heap, (0-age, name)) # negate ages for max heap
    else:
        heappush(min_heap, (age, name))

    balance_heaps(min_heap, max_heap)

def balance_heaps(min_heap, max_heap):
    """
    Balances two ordered heaps by moving the root of the max heap to the min heap (or vice versa) if necessary.
    """
    if (len(min_heap) - len(max_heap) >= 2):
        shift = heappop(min_heap)
        heappush(max_heap, (0 - shift[0], shift[1]))
    elif (len(max_heap) - len(min_heap) >= 2):
        shift = heappop(max_heap)
        heappush(min_heap, (abs(shift[0]), shift[1]))

def get_median(min_heap, max_heap):
    """Retrieves the median from a pair of balanced, ordered min/max heaps."""
    if (len(min_heap) == 0 and len(max_heap) == 0):
        med = (0, "Median does not exist, no data processed.")
    elif (len(min_heap) > len(max_heap)):
        med = min_heap[0]
    elif (len(min_heap) < len(max_heap)):
        med = (abs(max_heap[0][0]), max_heap[0][1])
    elif (abs(max_heap[0][0]) == min_heap[0][0]):
        # if even count, average will only be in set if roots are equal
        med = min_heap[0]
    else:
        med_avg = (min_heap[0][0] + abs(max_heap[0][0])) / 2
        med_dne = "No entity exist in the provided list with the median age, outcome was between " + max_heap[0][1] + " at "  + str(max_heap[0][0]) + " years and " + min_heap[0][1] + " at " + str(min_heap[0][0]) + " years."
        med = (med_avg, med_dne)

    return med




if __name__=='__main__':
    file_urls = [url for url in sys.argv[1:]]
    avg, med, procd = compute_stats(file_urls)
    print("-"*30, "\nResults:\n")
    print("Average age:", avg, "yrs")
    print("Median age:", med[0], "yrs")
    print("Median entity:", med[1])
    print("Processed:", procd, "lines")
