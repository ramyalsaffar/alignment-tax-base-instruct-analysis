# Class ResponseCollector
#------------------------
# This class handles:
#   - Collecting responses from base and instruct models
#   - Progress tracking
#   - Error handling
###############################################################################


class ResponseCollector:
    """Collect model responses with progress tracking"""

    def __init__(self, model_manager, config):
        """
        Initialize response collector

        Args:
            model_manager: ModelManager instance with loaded models
            config: Configuration dictionary
        """
        self.model_manager = model_manager
        self.config = config
        self.collection_stats = {
            'total_collected': 0,
            'errors': 0
        }


    def collect_responses(self, prompts, show_progress=True):
        """
        Collect responses from both base and instruct models

        Args:
            prompts: List of prompt dictionaries
            show_progress: Whether to show progress bar

        Returns:
            List of prompt dictionaries with responses added
        """
        print("Collecting model responses...")

        if show_progress:
            iterator = tqdm(prompts, desc="Collecting responses")
        else:
            iterator = prompts

        for prompt_data in iterator:
            prompt = prompt_data['prompt']

            # Get responses from both models
            base_response = self.model_manager.get_response('base', prompt)
            instruct_response = self.model_manager.get_response('instruct', prompt)

            # Store responses
            prompt_data['base_response'] = base_response
            prompt_data['instruct_response'] = instruct_response

            # Track success
            if base_response and instruct_response:
                self.collection_stats['total_collected'] += 1
            else:
                self.collection_stats['errors'] += 1

            # Small delay between calls
            model_delay = self.config.get('timing_config', {}).get('model_delay', 0.1)
            time.sleep(model_delay)

        return prompts


    def collect_single_response(self, model_name, prompt):
        """
        Collect a single response from specified model

        Args:
            model_name: 'base' or 'instruct'
            prompt: Prompt string

        Returns:
            Response string
        """
        return self.model_manager.get_response(model_name, prompt)


    def get_stats(self):
        """Get collection statistics"""
        return self.collection_stats.copy()


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 2025

@author: ramyalsaffar
"""
