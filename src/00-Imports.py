# Imports
#--------
#
# This file has all of the libraries needed for the project.
# It also imports configuration and constants.
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

import boto3
from botocore.exceptions import ClientError

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


# Environment Detection (Smart Defaults)
#----------------------------------------
# Detects if running locally or in AWS/Docker
# Defaults to 'local' if ENVIRONMENT variable not set
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

print(f"🌍 Running in: {ENVIRONMENT.upper()} mode")


# Environment-Aware Paths
#------------------------
# Sets appropriate paths based on where code is running
if ENVIRONMENT == 'aws':
    # AWS/Docker paths
    models_path = "/app/models/"
    project_path = "/app"
    base_results_path = "/app/results/"
    CodeFilePath = "/app/src/"
else:
    # Local paths (default)
    models_path = "/Users/ramyalsaffar/.lmstudio/models/"
    project_path = "/Users/ramyalsaffar/Ramy/C.V..V/1-Resume/06- LLM Model Behavior Projects/01- Alignment Tax - base vs instruct"
    base_results_path = project_path + "/03- Code/03- Results/"
    CodeFilePath = project_path + "/03- Code/02- Python/"


# LLM Model Paths
#----------------
llama_base_path = Path(models_path + "sgerhart/Meta-Llama-3.1-8B-Q4_K_M-GGUF/meta-llama-3.1-8b-q4_k_m.gguf")
llama_instruct_path = Path(models_path + "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf")


# Specific Subdirectories
#------------------------
data_path = base_results_path + "Data/"
reports_path = base_results_path + "Reports/"
graphs_path = base_results_path + "Graphs/"


# Create directories if they don't exist (AWS mode)
#---------------------------------------------------
if ENVIRONMENT == 'aws':
    for path in [base_results_path, data_path, reports_path, graphs_path]:
        os.makedirs(path, exist_ok=True)


#------------------------------------------------------------------------------


# Python Display Settings
#------------------------
pd.set_option('display.max_rows', 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_colwidth", 250)
pd.set_option('display.width', 1000)
pd.set_option('display.precision', 5)  # this will help me see big numbers without python converting it to exponential
pd.options.display.float_format = '{:.4f}'.format


#------------------------------------------------------------------------------


# Execute Code Files
#-------------------

# Import Configuration and Constants FIRST (before other modules)
#-----------------------------------------------------------------
# Note: Config file uses datetime, so it must be imported after datetime is available
# Import order: Config first (contains experiment settings), then Constants
exec(open(CodeFilePath+"01-Config.py").read())
exec(open(CodeFilePath+"02-Constants.py").read())

# Load remaining code files (03-21, excluding 22)
#---------------------------------------------------
# Files are now numbered 00-22:
#   00-Imports.py (this file)
#   01-Config.py (loaded above)
#   02-Constants.py (loaded above)
#   03-06: AWS Infrastructure (AWSConfig, SecretsHandler, S3Handler, EC2Setup)
#   07-11: Core API & Generation (ModelManager, GPT_API, PromptGenerator, ResponseCollector, ResponseEvaluator)
#   12-18: Pipeline & Analysis (Pipeline, OutlierHandler, Analyzers, Visualizer, Reporter)
#   19-20: Experiment Execution (ExperimentRunner, Execute)
#   21-AnalysisPipeline.py (load - contains AnalysisPipeline class)
#   22-Analyze.py (don't load - analysis execution script)
code_files_ls = os.listdir(CodeFilePath)
code_files_ls.sort()
code_files_ls = [x for x in code_files_ls if "py" in x]
code_files_ls.pop(0) # pop Imports file (00-Imports.py)
code_files_ls.pop(0) # pop Config file (01-Config.py) - already loaded
code_files_ls.pop(0) # pop Constants file (02-Constants.py) - already loaded
# Remove 22-Analyze.py (execution script, not a class/function library)
code_files_ls = [x for x in code_files_ls if x != "22-Analyze.py"]


# Loop over code files
#---------------------
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
