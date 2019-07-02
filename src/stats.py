import sys
import subprocess
import time
import pandas as pd
import numpy as np

def skeleton():
    raw_list = sys.argv[1:]
    if len(raw_list) != 1:
        print("Enter only one number to run corresponding data.")
        return
    n = 0
    try:
        n = int(raw_list[0])
    except ValueError:
        print("Please enter one INTEGER!")
        return
    if n <= 2:
        print("Please enter an integer larger than 2.")
        return
    print(n)


skeleton()
