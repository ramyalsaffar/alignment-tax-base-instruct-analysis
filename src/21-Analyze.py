# Analyze with Outlier Handling
###############################
#
# This script runs the complete alignment tax analysis pipeline.
# It orchestrates:
#   - Data loading and validation
#   - Descriptive analysis
#   - Outlier detection and cleaning
#   - Statistical analysis (including capability-specific)
#   - Visualization generation
#   - Report generation
#   - Summary and insights
#
# The heavy lifting is done by the AnalysisPipeline class (22-AnalysisPipeline.py)
#
###############################################################################


# =============================================================================
# RUN ANALYSIS PIPELINE
# =============================================================================

# Initialize and run the complete analysis pipeline
pipeline = AnalysisPipeline()
pipeline.run_full_analysis()


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
