# Class AlignmentTaxPipeline
#---------------------------
# This class orchestrates the alignment tax evaluation pipeline:
#   - Coordinates prompt generation, response collection, and evaluation
#   - Delegates work to specialized classes
#   - Tracks results and saves data
###############################################################################


class AlignmentTaxPipeline:
    """
    Orchestrates the alignment tax evaluation pipeline

    This refactored pipeline delegates work to specialized classes:
    - PromptGenerator: Generates prompts for evaluation axes
    - ResponseCollector: Collects model responses
    - ResponseEvaluator: Evaluates responses using GPT
    """


    def __init__(self, config):
        """
        Initialize the pipeline and all components

        Args:
            config: Configuration dictionary with all settings
        """
        self.config = config
        self.results = []

        # Initialize model manager
        self.model_manager = ModelManager(model_config=config.get('model_config', {}))

        # Initialize GPT API
        self.chatgpt = GPTAPI(
            config['openai_api_key'],
            api_config=config.get('api_config', {})
        )

        # Initialize specialized components
        self.prompt_generator = PromptGenerator(self.chatgpt, config)
        self.response_collector = ResponseCollector(self.model_manager, config)
        self.response_evaluator = ResponseEvaluator(self.chatgpt, config)

        # Load models
        print("\n🔧 Loading models...")
        self.model_manager.load_model(config['base_model_path'], 'base')
        self.model_manager.load_model(config['instruct_model_path'], 'instruct')
        print("✅ Models loaded successfully\n")


    def run_axis_evaluation(self, axis, prompt_count=50):
        """
        Run complete evaluation for a single axis

        Args:
            axis: Evaluation axis name
            prompt_count: Number of prompts to generate

        Returns:
            List of evaluated prompt dictionaries
        """
        print(f"\n{'='*60}")
        print(f"EVALUATING {axis.upper()}")
        print(f"{'='*60}\n")

        # Step 1: Generate prompts with retry logic
        print(f"📝 Step 1: Generating prompts...")
        prompts = self.prompt_generator.validate_and_generate_prompts(axis, prompt_count)

        if not prompts:
            print(f"❌ Failed to generate prompts for {axis}")
            return []

        print(f"✅ Generated {len(prompts)} prompts\n")

        # Step 2: Collect responses from models
        print(f"🤖 Step 2: Collecting model responses...")
        prompts = self.response_collector.collect_responses(prompts)
        print(f"✅ Collected {len(prompts)} responses\n")

        # Step 3: Evaluate responses using GPT
        print(f"⚖️ Step 3: Evaluating responses with GPT...")
        prompts = self.response_evaluator.evaluate_responses(prompts)

        # Print evaluation summary
        self._print_axis_summary(prompts, axis)

        # Store results
        self.results.extend(prompts)

        return prompts


    def generate_all_prompts_first(self, axes_config):
        """
        NEW FLOW: Generate all prompts for all axes upfront

        Args:
            axes_config: Dictionary mapping axis names to prompt counts

        Returns:
            Dictionary mapping axis names to lists of prompts
        """
        print(f"\n{'='*60}")
        print(f"PHASE 1: PROMPT GENERATION FOR ALL AXES")
        print(f"{'='*60}\n")

        all_prompts = self.prompt_generator.generate_all_axes_prompts(axes_config)

        print(f"✅ All prompts generated successfully\n")
        return all_prompts


    def run_axis_evaluation_with_prompts(self, axis, prompts):
        """
        Run evaluation for an axis using pre-generated prompts

        Args:
            axis: Evaluation axis name
            prompts: List of pre-generated prompt dictionaries

        Returns:
            List of evaluated prompt dictionaries
        """
        print(f"\n{'='*60}")
        print(f"EVALUATING {axis.upper()} ({len(prompts)} prompts)")
        print(f"{'='*60}\n")

        # Step 1: Collect responses from models
        print(f"🤖 Step 1: Collecting model responses...")
        prompts = self.response_collector.collect_responses(prompts)
        print(f"✅ Collected {len(prompts)} responses\n")

        # Step 2: Evaluate responses using GPT
        print(f"⚖️ Step 2: Evaluating responses with GPT...")
        prompts = self.response_evaluator.evaluate_responses(prompts)

        # Print evaluation summary
        self._print_axis_summary(prompts, axis)

        # Store results
        self.results.extend(prompts)

        return prompts


    def _print_axis_summary(self, prompts, axis):
        """
        Print summary statistics for axis evaluation

        Args:
            prompts: List of evaluated prompt dictionaries
            axis: Axis name
        """
        successful_evals = 0
        failed_evals = 0
        partial_failures = 0

        for prompt_data in prompts:
            base_score = prompt_data['base_score']
            instruct_score = prompt_data['instruct_score']

            if base_score == EXTREME_VALUE and instruct_score == EXTREME_VALUE:
                failed_evals += 1
            elif base_score == EXTREME_VALUE or instruct_score == EXTREME_VALUE:
                partial_failures += 1
            elif 1 <= base_score <= 3 and 1 <= instruct_score <= 3:
                successful_evals += 1
            else:
                failed_evals += 1

        # Print summary
        print(f"\n📊 Evaluation Summary for {axis.upper()}:")
        print(f"  ✅ Successful: {successful_evals}/{len(prompts)} ({successful_evals/len(prompts)*100:.1f}%)")
        print(f"  ⚠️  Partial failures: {partial_failures}/{len(prompts)} ({partial_failures/len(prompts)*100:.1f}%)")
        print(f"  ❌ Complete failures: {failed_evals}/{len(prompts)} ({failed_evals/len(prompts)*100:.1f}%)")


    def save_results(self, test_mode=False):
        """
        Save results to pickle file

        Args:
            test_mode: Whether this is a test run

        Returns:
            DataFrame with results
        """
        df = pd.DataFrame(self.results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mode_suffix = "_test" if test_mode else "_full"

        # Save full data as pickle for complete preservation
        pickle_filename = f"alignment_tax_base_instruct_results{mode_suffix}_{timestamp}.pkl"
        df.to_pickle(data_path + pickle_filename)
        print(f"\n✅ Full results saved to {pickle_filename}")
        print(f"📝 Excel conversion will happen during analysis phase")

        return df


    def get_stats(self):
        """Get statistics from all components"""
        return {
            'prompt_generation': self.prompt_generator.generation_stats,
            'response_collection': self.response_collector.get_stats(),
            'response_evaluation': self.response_evaluator.get_stats(),
            'total_results': len(self.results)
        }


    def print_pipeline_stats(self):
        """Print comprehensive pipeline statistics"""
        stats = self.get_stats()

        print(f"\n{'='*60}")
        print(f"PIPELINE STATISTICS")
        print(f"{'='*60}\n")

        print(f"📊 Total Results: {stats['total_results']}\n")

        print(f"📝 Response Collection:")
        collection_stats = stats['response_collection']
        print(f"  - Total collected: {collection_stats['total_collected']}")
        print(f"  - Errors: {collection_stats['errors']}\n")

        print(f"⚖️  Response Evaluation:")
        eval_stats = stats['response_evaluation']
        total_eval = eval_stats['total_evaluated']
        if total_eval > 0:
            print(f"  - Total evaluated: {total_eval}")
            print(f"  - Successful: {eval_stats['successful']} ({eval_stats['successful']/total_eval*100:.1f}%)")
            print(f"  - Partial failures: {eval_stats['partial_failures']} ({eval_stats['partial_failures']/total_eval*100:.1f}%)")
            print(f"  - Complete failures: {eval_stats['failed']} ({eval_stats['failed']/total_eval*100:.1f}%)")

        print(f"\n{'='*60}\n")


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 2025

@author: ramyalsaffar
"""
