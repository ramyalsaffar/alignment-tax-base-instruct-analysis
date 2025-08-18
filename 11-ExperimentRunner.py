# Class ExperimentRunner
#-----------------------
# This class handles all different ways to run the alignment tax experiment:
#   - Quick tests with reduced samples
#   - Single axis testing
#   - Full experiments
#   - Custom configurations
#   - Progress tracking and time estimation
###############################################################################


class ExperimentRunner:
    """
    Manages different experiment execution modes for alignment tax analysis
    """
    
    
    def __init__(self, base_config=None):
        """
        Initialize the experiment runner
        
        Args:
            base_config: Optional base configuration to use
        """
        self.base_config = base_config or {}
        self.pipeline = None
        self.caffeinate_process = None
        
        # Register cleanup on exit
        atexit.register(self._allow_sleep)

    
    def _prevent_sleep(self):
        """Prevent Mac from sleeping during experiment"""
        if sys.platform == 'darwin' and not self.caffeinate_process:
            try:
                self.caffeinate_process = subprocess.Popen(['caffeinate', '-dim'])
                print("☕ Sleep prevention activated")
            except:
                print("⚠️ Could not activate sleep prevention")
    
    
    def _allow_sleep(self):
        """Re-enable sleep by terminating caffeinate process"""
        if self.caffeinate_process:
            try:
                self.caffeinate_process.terminate()
                self.caffeinate_process.wait(timeout=5)
                print("☕ Sleep prevention deactivated")
            except:
                try:
                    self.caffeinate_process.kill()
                except:
                    pass
            finally:
                self.caffeinate_process = None

    
    def _build_config(self, api_key=None, overrides=None):
        """
        Build experiment configuration
        
        Args:
            api_key: OpenAI API key
            overrides: Dictionary of config overrides
        
        Returns:
            Complete configuration dictionary
        """
        # Start with base config
        config = {
            'base_model_path': llama_base_path,
            'instruct_model_path': llama_instruct_path,
            'experiment_config': EXPERIMENT_CONFIG.copy(),
            'api_config': API_CONFIG.copy(),
            'model_config': MODEL_CONFIG.copy()
        }
        
        # Add API key
        if api_key:
            config['openai_api_key'] = api_key
        elif not self.base_config.get('openai_api_key'):
            config['openai_api_key'] = getpass.getpass("\nEnter your OpenAI API key: ")
        else:
            config['openai_api_key'] = self.base_config['openai_api_key']
        
        # Apply any overrides
        if overrides:
            for key, value in overrides.items():
                if key in config:
                    if isinstance(config[key], dict):
                        config[key].update(value)
                    else:
                        config[key] = value
        
        # Merge with base config
        config.update(self.base_config)
        
        return config
    
    def _print_experiment_header(self, mode_name, sample_count=None):
        """Print a formatted experiment header"""
        print("\n" + "="*60)
        print(f"{mode_name.upper()}")
        print("="*60)
        
        if sample_count:
            print(f"📊 Total samples to evaluate: {sample_count}")
            estimated_time = self._get_time_estimate(sample_count)
            print(f"⏱️ Estimated time: {estimated_time}")
    
    def _get_time_estimate(self, sample_count):
        """
        Get time estimate for given sample count
        
        Args:
            sample_count: Number of samples to process
        
        Returns:
            String with time estimate
        """
        # Assume ~15 seconds per sample (conservative estimate)
        min_time = sample_count * 12 / 60
        max_time = sample_count * 20 / 60
        
        if min_time < 60:
            return f"{min_time:.0f}-{max_time:.0f} minutes"
        else:
            return f"{min_time/60:.1f}-{max_time/60:.1f} hours"
    
    def _print_summary(self, results_df, runtime_minutes=None):
        """
        Print experiment summary
        
        Args:
            results_df: DataFrame with results
            runtime_minutes: Optional runtime in minutes
        """
        print("\n" + "="*60)
        print("EXPERIMENT SUMMARY")
        print("="*60)
        
        # Basic stats
        print(f"✅ Total evaluations: {len(results_df)}")
        
        if runtime_minutes:
            print(f"⏱️ Total runtime: {runtime_minutes:.1f} minutes")
            if len(results_df) > 0:
                print(f"📊 Average time per evaluation: {runtime_minutes*60/len(results_df):.1f} seconds")
        
        # Success rates
        if 'base_score' in results_df.columns and 'instruct_score' in results_df.columns:
            successful = ((results_df['base_score'] != 99) & 
                         (results_df['instruct_score'] != 99)).sum()
            print(f"✅ Successful evaluations: {successful}/{len(results_df)} ({successful/len(results_df)*100:.1f}%)")
        
        # Results location
        print(f"📁 Results saved to: {data_path}")
    
    def run_experiment(self, test_mode=False, axes_override=None):
        """
        Main experiment execution with configurable settings
        
        Args:
            test_mode: If True, run with reduced samples for testing
            axes_override: Optional dictionary to override axes configuration
        
        Returns:
            DataFrame with results
        """
        self._print_experiment_header(
            "ALIGNMENT TAX EXPERIMENT" if not test_mode else "TEST MODE EXPERIMENT"
        )
        
        print("\n📋 Configuration Summary:")
        print(f"  - Experiment: {EXPERIMENT_CONFIG['experiment_name']}")
        print(f"  - API Rate Limit: {API_CONFIG['rate_limit_calls']} calls per {API_CONFIG['rate_limit_window']}s")
        print(f"  - Model Context: {MODEL_CONFIG['n_ctx']} tokens")
        
        # Determine axes to test
        if test_mode:
            print("\n⚠️ TEST MODE - Using reduced samples")
            test_size = EXPERIMENT_CONFIG.get('test_sample_size', 6)
            axes_to_test = {k: test_size for k in AXES_CONFIG.keys()}
        elif axes_override:
            axes_to_test = axes_override
        else:
            # AUTO-ADD BUFFER HERE! 
            buffer_pct = EXPERIMENT_CONFIG.get('prompt_buffer_percentage', 10)
            axes_to_test = {
                k: int(v * (1 + buffer_pct / 100)) 
                for k, v in AXES_CONFIG.items()
            }
            print(f"\n📊 Auto-added {buffer_pct}% buffer to all axes")
        
        total_samples = sum(axes_to_test.values())
        print(f"  - Total Samples: {total_samples} (includes buffer)")
        
        # Build configuration
        config = self._build_config()
        
        # Initialize pipeline
        print("\n🚀 Initializing pipeline...")
        self.pipeline = AlignmentTaxPipeline(config)
        
        # Track timing
        start_time = time.time()
        completed_axes = []
        
        try:
            # Run evaluation for each axis
            for idx, (axis, prompt_count) in enumerate(axes_to_test.items(), 1):
                axis_start = time.time()
                
                print(f"\n{'='*50}")
                print(f"{idx}. Evaluating {axis.upper()} ({prompt_count} samples)")
                print(f"{'='*50}")
                
                self.pipeline.run_axis_evaluation(axis, prompt_count)
                completed_axes.append(axis)
                
                # Save intermediate results if configured
                if EXPERIMENT_CONFIG.get('save_intermediate', True):
                    intermediate_df = pd.DataFrame(self.pipeline.results)
                    intermediate_file = f"{data_path}intermediate_{axis}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                    intermediate_df.to_pickle(intermediate_file)  # Use pickle instead of Excel
                    print(f"💾 Intermediate results saved for {axis}")
                
                # Show progress
                axis_time = time.time() - axis_start
                total_elapsed = time.time() - start_time
                
                if idx < len(axes_to_test) and TIMING_CONFIG.get('estimate_time', True):
                    avg_time_per_axis = total_elapsed / idx
                    remaining_axes = len(axes_to_test) - idx
                    eta = avg_time_per_axis * remaining_axes
                    print(f"\n⏱️ Axis completed in {axis_time/60:.1f} min")
                    print(f"📊 Progress: {idx}/{len(axes_to_test)} axes")
                    print(f"⏳ Estimated time remaining: {eta/60:.1f} min")
                
                # Delay between axes
                if axis != list(axes_to_test.keys())[-1]:
                    time.sleep(TIMING_CONFIG.get('api_delay', 0.5) * 2)
                    
        except KeyboardInterrupt:
            print("\n\n⚠️ Experiment interrupted by user!")
            print(f"✓ Completed axes: {', '.join(completed_axes)}")
            if self.pipeline.results:
                print("💾 Saving partial results...")
                partial_df = self.pipeline.save_results(test_mode)
                print(f"✓ Saved {len(partial_df)} evaluations")
            return None
            
        except Exception as e:
            print(f"\n❌ Error occurred: {str(e)}")
            print(f"✓ Completed axes: {', '.join(completed_axes)}")
            if self.pipeline.results:
                print("💾 Saving partial results...")
                partial_df = self.pipeline.save_results(test_mode)
            raise
        
        # Save final results
        print("\n💾 Saving final results...")
        results_df = self.pipeline.save_results(test_mode=test_mode)
        
        # Clean up intermediate files if configured
        if EXPERIMENT_CONFIG.get('save_intermediate', True):
            self._cleanup_intermediate_files()
        
        # Final summary
        total_time = time.time() - start_time
        self._print_evaluation_success_breakdown()
        self._print_summary(results_df, total_time/60)
        
        # Show API usage stats
        if hasattr(self.pipeline, 'chatgpt'):
            api_stats = self.pipeline.chatgpt.get_stats()
            print(f"\n📈 API Usage:")
            print(f"  - Total calls: {api_stats['total_calls']}")
            print(f"  - Errors: {api_stats['errors']}")
            print(f"  - Success rate: {api_stats['success_rate']:.1f}%")
        
        return results_df
    
    def _cleanup_intermediate_files(self):
        """Clean up intermediate files after successful completion"""
        print("\n🧹 Cleaning up intermediate files...")
        intermediate_pattern = f"{data_path}intermediate_*.pkl"
        intermediate_files = glob.glob(intermediate_pattern)
        
        if intermediate_files:
            for file in intermediate_files:
                try:
                    os.remove(file)
                    print(f"  ✓ Removed: {os.path.basename(file)}")
                except Exception as e:
                    print(f"  ⚠️ Could not remove {os.path.basename(file)}: {e}")
            print(f"  Cleaned up {len(intermediate_files)} intermediate files")
        else:
            print("  No intermediate files to clean")
    
    def _print_evaluation_success_breakdown(self):
        """Print breakdown of evaluation success/failure rates"""
        if not self.pipeline or not self.pipeline.results:
            return
        
        print("\n📊 EVALUATION SUCCESS BREAKDOWN:")
        total_results = len(self.pipeline.results)
        successful = sum(1 for r in self.pipeline.results 
                        if r['base_score'] != 99 and r['instruct_score'] != 99)
        partial_fail = sum(1 for r in self.pipeline.results 
                          if (r['base_score'] == 99) != (r['instruct_score'] == 99))
        complete_fail = sum(1 for r in self.pipeline.results 
                           if r['base_score'] == 99 and r['instruct_score'] == 99)
        
        print(f"  ✅ Successful: {successful}/{total_results} ({successful/total_results*100:.1f}%)")
        print(f"  ⚠️ Partial failures: {partial_fail}/{total_results} ({partial_fail/total_results*100:.1f}%)")
        print(f"  ❌ Complete failures: {complete_fail}/{total_results} ({complete_fail/total_results*100:.1f}%)")
    
    
    def quick_test(self):
        """Quick test with reduced samples"""
        print("\n🧪 Running quick test...")
        test_size = EXPERIMENT_CONFIG.get('test_sample_size', 6)
        print(f"   Using {test_size} samples per axis")
        return self.run_experiment(test_mode=True)
    
    
    def full_experiment(self):
        """Full experiment with all configured samples"""
        print("\n🔬 Running full experiment...")
        
        total_samples = sum(AXES_CONFIG.values())
        estimated_time = self._get_time_estimate(total_samples)
        
        print(f"\n⚠️ This will evaluate {total_samples} samples")
        print(f"⏱️ Estimated time: {estimated_time}")
        
        response = input("\nProceed? (y/n): ")
        if response.lower() != 'y':
            print("Experiment cancelled")
            return None
        
        # Prevent sleep for long experiment
        self._prevent_sleep()
        
        try:
            return self.run_experiment(test_mode=False)
        finally:
            self._allow_sleep()
    
    
    def test_single_axis(self):
        """Test a single axis with full or reduced samples"""
        print("\n🎯 Single Axis Test Mode")
        print("-" * 40)
        
        # Show available axes
        print("Available axes:")
        for i, (axis, count) in enumerate(AXES_CONFIG.items(), 1):
            print(f"{i}. {axis} ({count} samples)")
        print(f"{len(AXES_CONFIG)+1}. Cancel")
        
        # Get user choice
        choice = input(f"\nSelect axis to test (1-{len(AXES_CONFIG)+1}): ")
        
        try:
            choice_idx = int(choice) - 1
            if choice_idx == len(AXES_CONFIG):
                print("Test cancelled")
                return None
                
            axis_list = list(AXES_CONFIG.keys())
            if 0 <= choice_idx < len(axis_list):
                selected_axis = axis_list[choice_idx]
                
                # Ask for sample size
                default_count = AXES_CONFIG[selected_axis]
                test_count = EXPERIMENT_CONFIG.get('test_sample_size', 6)
                
                print(f"\nSample size options:")
                print(f"1. Quick test ({test_count} samples)")
                print(f"2. Full test ({default_count} samples)")
                print(f"3. Custom number")
                
                size_choice = input("Select option (1-3): ")
                
                if size_choice == '1':
                    sample_count = test_count
                elif size_choice == '2':
                    sample_count = default_count
                elif size_choice == '3':
                    custom = input(f"Enter number of samples (1-{default_count*2}): ")
                    try:
                        sample_count = min(int(custom), default_count * 2)
                    except ValueError:
                        sample_count = test_count
                else:
                    sample_count = test_count
                
                print(f"\n🚀 Testing {selected_axis} with {sample_count} samples...")
                
                # Run single axis
                axes_override = {selected_axis: sample_count}
                results = self.run_experiment(test_mode=False, axes_override=axes_override)
                
                if results is not None and len(results) > 0:
                    # Quick analysis
                    print(f"\n📈 Quick Analysis for {selected_axis}:")
                    print(f"   - Mean alignment tax: {results['alignment_tax'].mean():.3f}")
                    print(f"   - Std deviation: {results['alignment_tax'].std():.3f}")
                
                return results
            else:
                print("Invalid choice")
                return None
                
        except ValueError:
            print("Invalid input")
            return None
    
    
    def custom_experiment(self):
        """Run experiment with custom parameters"""
        print("\n⚙️ Custom Experiment Mode")
        print("-" * 40)
        
        # Initialize custom axes dictionary
        custom_axes = {}
        
        # Show available axes and get custom counts
        print("\nEnter sample count for each axis (press Enter for 0/skip):")
        for axis, default_count in AXES_CONFIG.items():
            user_input = input(f"{axis} (default {default_count}): ").strip()
            
            if user_input:
                try:
                    count = int(user_input)
                    if count > 0:
                        custom_axes[axis] = min(count, default_count * 2)  # Cap at 2x default
                        if count > default_count * 2:
                            print(f"  Capped at {default_count * 2}")
                except ValueError:
                    print(f"  Invalid input, skipping {axis}")
            else:
                # Skip this axis if no input
                continue
        
        # Check if any axes were selected
        if not custom_axes:
            print("No axes selected. Cancelled.")
            return None
        
        # Show summary
        total = sum(custom_axes.values())
        print(f"\n📊 Custom configuration:")
        for axis, count in custom_axes.items():
            print(f"  {axis}: {count}")
        print(f"  Total: {total} samples")
        
        estimated_time = self._get_time_estimate(total)
        print(f"⏱️ Estimated time: {estimated_time}")
        
        response = input("\nProceed? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            return None
        
        # Prevent sleep if it's a long experiment
        if total > 50:
            self._prevent_sleep()
        
        try:
            return self.run_experiment(test_mode=False, axes_override=custom_axes)
        finally:
            self._allow_sleep()
            

    def clean_text_for_excel(self, text):
        """Clean text to remove characters illegal in Excel"""
        if not isinstance(text, str):
            return text
        
        # Remove illegal characters for Excel
        illegal_chars = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')
        cleaned = illegal_chars.sub('', text)
        
        # Remove problematic Unicode
        cleaned = cleaned.encode('utf-8', errors='ignore').decode('utf-8')
        
        return cleaned
    
    
    def convert_pickle_to_excel(self, df, run_id, output_path):
        """Convert pickle dataframe to Excel with cleaned text"""
        print("\n📊 Converting to Excel with cleaned text...")
        
        # Create Excel-friendly version
        df_excel = df.copy()
        text_columns = ['prompt', 'base_response', 'instruct_response']
        
        for col in text_columns:
            if col in df_excel.columns:
                # Clean illegal characters
                df_excel[col] = df_excel[col].apply(self.clean_text_for_excel)
                # Keep first 500 chars for readability in Excel
                df_excel[f'{col}_preview'] = df_excel[col].apply(
                    lambda x: x[:500] + "..." if isinstance(x, str) and len(x) > 500 else x
                )
                # Drop full text columns from Excel version
                df_excel = df_excel.drop(col, axis=1)
        
        # Save to Excel
        excel_filename = f"alignment_tax_base_instruct_results_full_{run_id}.xlsx"
        try:
            df_excel.to_excel(output_path + excel_filename, index=False)
            print(f"✅ Excel summary saved to {excel_filename}")
            return excel_filename
        except Exception as e:
            print(f"⚠️ Excel save failed: {e}")
            print("📝 Continuing with pickle data for analysis...")
            return None


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 19:24:40 2025

@author: ramyalsaffar
"""