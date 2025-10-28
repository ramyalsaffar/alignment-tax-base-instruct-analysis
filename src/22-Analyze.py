# Analyze with Outlier Handling
###############################
#
# This script runs the alignment tax analysis pipeline.
# It provides both command-line and interactive interfaces for flexibility.
#
# The heavy lifting is done by the AnalysisPipeline class (21-AnalysisPipeline.py)
#
# Usage:
#   python 22-Analyze.py                # Interactive mode
#   python 22-Analyze.py --full         # Full analysis pipeline
#   python 22-Analyze.py --quick        # Load + descriptive only
#   python 22-Analyze.py --stats        # Up to statistical analysis
#   python 22-Analyze.py --viz          # Generate visualizations only
#   python 22-Analyze.py --reports      # Generate reports only
#
###############################################################################


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    # Initialize the analysis pipeline
    pipeline = AnalysisPipeline()

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--full':
            # Run complete analysis pipeline
            pipeline.run_full_analysis()

        elif sys.argv[1] == '--quick':
            # Quick look: Load data + descriptive analysis only
            pipeline.load_data()
            pipeline.run_descriptive_analysis()

        elif sys.argv[1] == '--stats':
            # Up to statistical analysis (no viz/reports)
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()
            pipeline.run_statistical_analysis()

        elif sys.argv[1] == '--viz':
            # Generate visualizations only (assumes data already loaded)
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()
            pipeline.generate_visualizations()

        elif sys.argv[1] == '--reports':
            # Generate reports only (assumes data already processed)
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()
            pipeline.run_statistical_analysis()
            pipeline.generate_reports()
            pipeline.print_summary()

        else:
            print("Usage: python 22-Analyze.py [--full|--quick|--stats|--viz|--reports]")
            print("\nOptions:")
            print("  --full     Run complete analysis pipeline")
            print("  --quick    Load data + descriptive analysis only")
            print("  --stats    Run up to statistical analysis (no viz/reports)")
            print("  --viz      Generate visualizations only")
            print("  --reports  Generate reports only")

    else:
        # Interactive mode
        print("\n📊 Alignment Tax Analysis Launcher")
        print("-" * 50)
        print("1. Full Analysis (complete pipeline)")
        print("2. Quick Look (load + descriptive only)")
        print("3. Data Loading Only")
        print("4. Descriptive Analysis")
        print("5. Outlier Cleaning")
        print("6. Statistical Analysis")
        print("7. Generate Visualizations")
        print("8. Generate Reports")
        print("9. Custom Sections (choose multiple)")
        print("0. Exit")

        choice = input("\nSelect mode (0-9): ").strip()

        if choice == '1':
            # Full pipeline
            pipeline.run_full_analysis()

        elif choice == '2':
            # Quick look
            pipeline.load_data()
            pipeline.run_descriptive_analysis()

        elif choice == '3':
            # Just load data
            pipeline.load_data()

        elif choice == '4':
            # Just descriptive
            pipeline.load_data()
            pipeline.run_descriptive_analysis()

        elif choice == '5':
            # Just outlier cleaning
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()

        elif choice == '6':
            # Just statistical
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()
            pipeline.run_statistical_analysis()

        elif choice == '7':
            # Just visualizations
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()
            pipeline.generate_visualizations()

        elif choice == '8':
            # Just reports
            pipeline.load_data()
            pipeline.run_descriptive_analysis()
            pipeline.clean_outliers()
            pipeline.run_statistical_analysis()
            pipeline.generate_reports()

        elif choice == '9':
            # Custom sections
            print("\n📋 Select sections to run (comma-separated):")
            print("  1=Load, 2=Descriptive, 3=Clean, 4=Stats, 5=Viz, 6=Reports, 7=Summary")
            sections_input = input("Enter sections (e.g., 1,2,4,6): ").strip()
            sections = [s.strip() for s in sections_input.split(',')]

            if '1' in sections:
                pipeline.load_data()
            if '2' in sections:
                if pipeline.results_df is None:
                    pipeline.load_data()
                pipeline.run_descriptive_analysis()
            if '3' in sections:
                if pipeline.results_df is None:
                    pipeline.load_data()
                if pipeline.core_analyzer is None:
                    pipeline.run_descriptive_analysis()
                pipeline.clean_outliers()
            if '4' in sections:
                if pipeline.results_df is None:
                    pipeline.load_data()
                if pipeline.core_analyzer is None:
                    pipeline.run_descriptive_analysis()
                if pipeline.df_clean is None:
                    pipeline.clean_outliers()
                pipeline.run_statistical_analysis()
            if '5' in sections:
                if pipeline.results_df is None:
                    pipeline.load_data()
                if pipeline.core_analyzer is None:
                    pipeline.run_descriptive_analysis()
                if pipeline.df_clean is None:
                    pipeline.clean_outliers()
                pipeline.generate_visualizations()
            if '6' in sections:
                if pipeline.results_df is None:
                    pipeline.load_data()
                if pipeline.core_analyzer is None:
                    pipeline.run_descriptive_analysis()
                if pipeline.df_clean is None:
                    pipeline.clean_outliers()
                if pipeline.statistical_results is None:
                    pipeline.run_statistical_analysis()
                pipeline.generate_reports()
            if '7' in sections:
                if pipeline.results_df is None:
                    pipeline.load_data()
                if pipeline.core_analyzer is None:
                    pipeline.run_descriptive_analysis()
                if pipeline.df_clean is None:
                    pipeline.clean_outliers()
                pipeline.print_summary()

        elif choice == '0':
            print("Exiting...")
        else:
            print("Invalid choice. Exiting...")


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
