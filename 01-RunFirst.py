# Run First
#----------
#
# This file has all of the libraries needed for the project.
# Paths to load from or to.
#
###############################################################################


#------------------------------------------------------------------------------


# Libraries
#----------
import pandas as pd
import numpy as np

import time
from datetime import datetime

from collections import deque
from typing import Optional, Tuple, Dict, List

import subprocess
import atexit

import io
import os
import sys
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
import glob
import getpass

from tqdm import tqdm

import random

import re
import json
import pickle

import scipy
from scipy import stats
from scipy.stats import wilcoxon, ttest_rel, shapiro, median_abs_deviation, mannwhitneyu

import matplotlib.pyplot as plt
import seaborn as sns

import openai
from llama_cpp import Llama

import matplotlib.patches as mpatches
from matplotlib.patches import Patch 

from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfgen import canvas


#------------------------------------------------------------------------------


# LLM paths
#----------
models_path = "/Users/ramyalsaffar/.lmstudio/models/"
llama_base_path = Path(models_path + "sgerhart/Meta-Llama-3.1-8B-Q4_K_M-GGUF/meta-llama-3.1-8b-q4_k_m.gguf")
llama_instruct_path = Path(models_path + "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")


# Project path
#-------------
project_path = "/Users/ramyalsaffar/Ramy/C.V..V/1-Resume/06- LLM Model Behavior Projects/01- Alignment Tax - base vs instruct"


# Results path
#-------------
base_results_path = project_path + "/03- Code/03- Results/"


# Specific subdirectories
#------------------------
data_path = base_results_path + "Data/"
reports_path = base_results_path + "Reports/"
graphs_path = base_results_path + "Graphs/"


#------------------------------------------------------------------------------


# Python disply settings
#-----------------------
pd.set_option('display.max_rows', 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_colwidth", 250)
pd.set_option('display.width', 1000)
pd.set_option('display.precision', 5)  # this will help me see big numbers without python converting it to exponential
pd.options.display.float_format = '{:.4f}'.format


#------------------------------------------------------------------------------


# Execute code files
#-------------------
CodeFilePath = project_path + "/03- Code/02- Python/"
code_files_ls = os.listdir(CodeFilePath)
code_files_ls.sort()
code_files_ls = [x for x in code_files_ls if "py" in x]
code_files_ls.pop(0) # pop RunFirst file
code_files_ls.pop(-1) # pop Analyze file


# Loop over cde files
#--------------------
for i in range(0,len(code_files_ls)):
    
    file = code_files_ls[i]
    
    print(file)
    
    exec(open(CodeFilePath+file).read())


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 10:24:33 2025

@author: ramyalsaffar
"""