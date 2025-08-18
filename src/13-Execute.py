# Execute Pipeline
#-----------------
# This will:
    # connect to the GPT API
    # generate prompts for each eval axis
    # load LLMs locally
    # feed the local LLMs the prompts 
    # collect the local LLM responses
    # save the results

# The 5 axes are:
    # Refusal behavior:         Safety dimension
    # Creativity:           Capability dimension 
    # Helpfulness:          Capability dimension
    # Hedging:               Communication style
    # Hallucination tendency: Accuracy dimension
#
###############################################################################

# This is the main entry point for running alignment tax experiments.
# It provides both command-line and interactive interfaces.
#
# Usage:
#   python 11-Execute.py                # Interactive mode
#   python 11-Execute.py --test         # Quick test
#   python 11-Execute.py --full         # Full experiment  
#   python 11-Execute.py --axis         # Single axis test
#   python 11-Execute.py --custom       # Custom configuration
#
###############################################################################


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    
    # Initialize the experiment runner
    runner = ExperimentRunner()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            runner.quick_test()
        elif sys.argv[1] == '--full':
            runner.full_experiment()
        elif sys.argv[1] == '--axis':
            runner.test_single_axis()
        elif sys.argv[1] == '--custom':
            runner.custom_experiment()
        else:
            print("Usage: python 11-Execute.py [--test|--full|--axis|--custom]")
            print("\nOptions:")
            print("  --test    Run quick test with reduced samples")
            print("  --full    Run full experiment as configured")
            print("  --axis    Test a single axis")
            print("  --custom  Run with custom sample counts")
    else:
        # Interactive mode
        print("\n🎮 Alignment Tax Experiment Launcher")
        print("-" * 40)
        print("1. Quick Test (configurable samples per axis)")
        print("2. Test Single Axis")
        print("3. Full Experiment (as configured)")
        print("4. Custom Experiment")
        print("5. Exit")
        
        choice = input("\nSelect mode (1-5): ")
        
        if choice == '1':
            runner.quick_test()
        elif choice == '2':
            runner.test_single_axis()
        elif choice == '3':
            runner.full_experiment()
        elif choice == '4':
            runner.custom_experiment()
        else:
            print("Exiting...")


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
