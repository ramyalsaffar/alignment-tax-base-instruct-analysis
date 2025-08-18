# Control Room Configuration
#---------------------------
# This will:
#   - Provide centralized configuration (control room)
###############################################################################


# =============================================================================
# CONTROL ROOM - All Configuration Settings
# =============================================================================


# API Configuration
#------------------
API_CONFIG = {
    'model':'gpt-4o',             # GPT model name
    'rate_limit_calls': 400,      # Max API calls per time window. Use 20 for free tier, tier 1 is 500 RPM, so use 300-400. After $50 spent: 5,000 RPM. After $100 spent: 10,000 RPM.
    'rate_limit_window': 60,      # Time window in seconds, do NOT change!
    'max_retries': 5,             # Retries for failed API calls
    'temperature_generate': 0.8,  # Temperature for prompt generation
    'temperature_evaluate': 0.0,  # Temperature for evaluation
    'max_tokens_generate': 6000,  # Max tokens for generation
    'max_tokens_evaluate': 10     # Max tokens for evaluation, we only need two digits
}


# Model Configuration
#--------------------
MODEL_CONFIG = {
    'n_ctx': 4096,               # Context window size
    'n_threads': 8,              # CPU threads
    'n_gpu_layers': -1,          # GPU layers, Use ALL layers
    'max_tokens': 512,           # Max response tokens
    'min_tokens': 50,            # Ensure minimum response length, prevents single-word or too-brief responses
    'temperature': 0.7,          # Model temperature
    'top_p': 0.9,                # Nucleus sampling
    'repeat_penalty': 1.1,       # Repetition penalty
    'max_retries': 5,            # Retries for model responses
    'n_batch': 256,              # Controls how many tokens the model processes at once during generation, smaller value means smaller bites and less errors but slower
    'use_mmap': True,            # Memory-mapped files (faster loading)
    'use_mlock': False,          # Forces the OS to keep the ENTIRE model in RAM permanently
    'seed': -1,                  # Random seed
    'verbose':False,             # prevents verbosity
    'stop':["</s>", 
            "\n\n\n", 
            "<|eot_id|>"],       # end-of-sequence or two newlines are encountered, helps prevent rambling after complete thoughts
    'echo': False                # Don't echo prompt
}


# Experiment Configuration
#-------------------------
EXPERIMENT_CONFIG = {
    'experiment_name': f'alignment_tax_base_v_instruct_{datetime.now().strftime("%Y%m%d_%H%M")}',
    'save_intermediate': True,      # Save after each axis
    'prompt_buffer_percentage': 5,  # Extra prompts to generate as buffer (percentage)
    'test_sample_size': 3           # Sample size for quick tests (per axis or total for single axis)
}


# Evaluation Axes Configuration
#------------------------------
AXES_CONFIG = {
    'refusal': 180,              # 1/3 each: direct, roleplay, fictional
    'creativity': 120,           # 1/2 each: novelty, constraint-bound
    'helpfulness': 120,          # 1/2 each: simple, complex
    'hedging': 180,              # 1/3 each: predictions, subjective, ambiguous
    'hallucination': 120         # No subcategories
}


# Timing Configuration
#---------------------
TIMING_CONFIG = {
    'api_delay': 0.5,         # Delay between API calls (seconds)
    'model_delay': 0.1,       # Delay between model calls (seconds)
    'show_progress': True,    # Show progress bars
    'estimate_time': True     # Show time estimates
}


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 13:02:22 2025

@author: ramyalsaffar
"""
