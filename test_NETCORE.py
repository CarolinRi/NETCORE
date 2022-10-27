"""
Test the NETCORE algorithm with example datasets
Version: 1.0
Python 3.9+
Date created: October 26th, 2022
Date modified: -


HOW TO RUN THIS ALGORITHM
    - Load the test datasets from https://github.com/CarolinRi/NETCORE
    - Unzip the file and place the folder into the same directory in which the test_NETCORE.py file is located (alternatively, you can change the list containing the filenames (line 22) to include the respective directories)
    - Make sure you have the NETCORE algorithm installed (easiest way: load NETCORE.py from https://github.com/CarolinRi/NETCORE and have it in the same directory as the test_NETCORE.py file)
    - if necessary, install the required packages (mainly networkx and pandas) or directly use the anaconda environment accessible at https://github.com/CarolinRi/NETCORE. (easiest way is to import it via the Anaconda Navigator: https://anaconda.org/anaconda/anaconda-navigator)
    - run test_NETCORE.py
"""

from NETCORE import *
import pandas as pd


# specify the file with the data to be analyzed
filenames = ["Test_datasets/Antibiotics.csv","Test_datasets/Fluorophores.csv","Test_datasets/Vitamins.csv","Test_datasets/Antioxidants.csv","Test_datasets/Pooled.csv"]

# specify the correlation threshold to be used for creating the correlation matrix
t_corr = 0.6

for name in filenames:
    print(f"analyzed dataset: {name}")

    # import data as a pandas data frame
    data = pd.read_csv(name)

    # run the NETCORE algorithm
    run_NETCORE(data, t_corr)
