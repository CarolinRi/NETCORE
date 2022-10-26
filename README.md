# NETCORE
The NETCORE algorithm performs feature elimination considering both, multicollinearity of datasets and the reduction efficiency.

This repository contains the following files:
- NETCORE.py:                   the source code for the NETCORE algorithm
- LICENSE.md:                   the license under which the algorithm may be used
- environment_NETCORE.yaml:     the Anaconda environment used during development and testing
- Test_datasets.zip:            5 molecular data sets used for testing: Antibiotics.csv, Fluorophores.csv, Vitamins.csv, Antioxidants.csv, Pooled.csv
- test_NETCORE.py:              A python file to run and test the NETCORE algorithm (instructions how to use it are included in the file)

One easy way how to use the NETCORE algorithm (for an example, please see test_NETCORE.py):
1. Download the NETCORE.py script
2. include the file into your code repository
3. create a new python file
4. in this file, import the NETCORE algorithm via "from NETCORE import *"
5. to run it call the function "run_NETCORE(data, correlation_threshold)" - data should be provided as a pandas dataframe, the correlation threshold should be a number between 0 and 1



MIT License

Copyright (c) [2022] [Carolin Rickert, Manuel Henkel, Oliver Lieleg]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
