"""
        Author: Spencer Little (mrlittle@uw.edu)
        Last edit: 01/05/2020
        Generates csv files in the test format (fname, lname, age).
"""

from faker import Faker
from random import randint

def gen_testfile(count, fname):
    """
    Generates a test file with <count> lines in the test format (fname, lname, age)
    """
    fake = Faker()
    with open(fname, "w+") as testf:
        testf.write('fname, lname, age\n') # filter names w/ more than two components
        for x in range(count):
            name = fake.name()
            while (len(name.split(" ")) != 2):
                name = fake.name()
            line = ", ".join(name.split(" ")) + ", " + str(randint(1, 100)) + "\n"
            testf.write(line


if __name__=="__main__":
    gen_testfile(100000, "test1.csv")
    gen_testfile(1000000, "test2.csv")
    gen_testfile(10000000, "test3.csv")
