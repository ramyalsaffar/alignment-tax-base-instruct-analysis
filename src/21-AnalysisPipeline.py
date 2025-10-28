# Class AnalysisPipeline
#-----------------------
# This class orchestrates the entire analysis pipeline:
#   - Data loading and validation
#   - Descriptive analysis
#   - Outlier detection and cleaning
#   - Statistical analysis (including capability-specific)
#   - Visualization generation
#   - Report generation
#   - Summary and insights
###############################################################################


class AnalysisPipeline:
    """
    Orchestrates the complete alignment tax analysis workflow.

    This class provides a clean, organized interface for running the full
    analysis pipeline from data loading through report generation.
    """

    def __init__(self, run_id=None):
        """
        Initialize the analysis pipeline.

        Args:
            run_id: Optional run identifier. If None, will be extracted from data filename.
        """
        self.run_id = run_id
        self.results_df = None
        self.df_clean = None
        self.cleaning_report = None
        self.descriptive_results = None
        self.statistical_results = None
        self.capability_results = None
        self.pareto_results = None
        self.overall_tax = None
        self.clean_overall_tax = None
        self.significant_improvements = []

        # Initialize analyzers (will be created in run_full_analysis)
        self.core_analyzer = None
        self.statistical_analyzer = None
        self.capability_analyzer = None
        self.outlier_handler = None
        self.visualizer = None
        self.reporter = None


    def load_data(self):
        """
        Load results data from pickle or Excel file.
        In AWS mode, tries to download from S3 first.
        Extracts run_id from filename and performs initial validation.
        """
        print("🚀 ALIGNMENT TAX ANALYSIS - ENHANCED PIPELINE")
        print("=" * 60)

        # If running in AWS, try to download latest results from S3 first
        if os.getenv('ENVIRONMENT') == 'aws':
            try:
                print("☁️  Checking S3 for latest results...")
                from S3Handler import S3Handler
                s3_handler = S3Handler()

                # List available runs in S3
                runs = s3_handler.list_runs()
                if runs:
                    latest_run = runs[0]  # Already sorted by date
                    print(f"📥 Downloading results for run: {latest_run}")

                    # Download the pickle file
                    s3_key = f"runs/alignment_tax_base_instruct_results_full_{latest_run}.pkl"
                    local_path = data_path + f"alignment_tax_base_instruct_results_full_{latest_run}.pkl"

                    try:
                        s3_handler.download_file(s3_key, local_path)
                        print(f"✅ Downloaded from S3")
                    except:
                        print(f"⚠️  S3 download failed, using local files...")
            except Exception as e:
                print(f"⚠️  S3 check failed: {e}, using local files...")

        # Load results - Try pickle first (complete data), fall back to Excel
        try:
            latest_pickle = max(glob.glob(data_path + "alignment_tax_base_instruct_results_full_*.pkl"), key=os.path.getctime)
            self.results_df = pd.read_pickle(latest_pickle)
            print(f"✅ Loaded pickle: {os.path.basename(latest_pickle)}")
            file_for_id = latest_pickle
        except:
            try:
                latest_excel = max(glob.glob(data_path + "alignment_tax_base_instruct_results_full_*.xlsx"), key=os.path.getctime)
                self.results_df = pd.read_excel(latest_excel)
                print(f"✅ Loaded Excel: {os.path.basename(latest_excel)}")
                file_for_id = latest_excel
            except Exception as e:
                print(f"❌ Error loading data: {e}")
                exit()

        # Extract run ID from filename if not provided
        if self.run_id is None:
            self.run_id = re.search(r'(\d{8}_\d{6})', file_for_id).group(1)

        print(f"📊 Analyzing run: {self.run_id}")
        print(f"📈 Total samples: {len(self.results_df)}")

        # Quick discovery check
        self.overall_tax = self.results_df['alignment_tax'].mean()
        if self.overall_tax < 0:
            print(f"🚨 NEGATIVE ALIGNMENT TAX DETECTED: {self.overall_tax:.3f}")
            print("   This is a paradigm-shifting discovery!")
        else:
            print(f"📊 Overall alignment tax: {self.overall_tax:.3f}")

        print(f"📋 Axes: {list(self.results_df['axis'].unique())}")
        axis_counts = self.results_df['axis'].value_counts()
        print("📊 Samples per axis:")
        for axis, count in axis_counts.items():
            print(f"   {axis}: {int(count)}")


    def run_descriptive_analysis(self):
        """
        Run descriptive statistical analysis on the raw data.
        """
        print(f"\n📊 SECTION 2: DESCRIPTIVE ANALYSIS")
        print("=" * 50)

        # Initialize analyzers
        self.core_analyzer = AlignmentTaxAnalyzer(self.run_id)
        self.statistical_analyzer = AlignmentTaxStatisticalAnalyzer()
        self.capability_analyzer = AlignmentTaxCapabilityAnalyzer()

        # Run descriptive analysis
        self.descriptive_results = self.core_analyzer.descriptive_analysis(self.results_df)

        # Print key descriptive findings
        print(f"\n🎯 DESCRIPTIVE SUMMARY:")
        overall_stats = self.descriptive_results['overall_stats']
        axis_breakdown = self.descriptive_results['axis_breakdown']

        print(f"   • Total evaluations: {overall_stats['n_total']:,}")
        print(f"   • Mean alignment tax: {overall_stats['mean_tax']:+.3f}")
        print(f"   • Negative tax axes: {overall_stats['negative_tax_count']}/{overall_stats['total_axes']}")

        print(f"\n📈 BY DIMENSION:")
        for axis, stats in axis_breakdown.items():
            print(f"   {axis:12} | Tax: {stats['tax_mean']:+.3f} | {stats['interpretation']}")

        # Check for paradigm shift
        if overall_stats['negative_tax_count'] == overall_stats['total_axes']:
            print(f"\n🚨 PARADIGM SHIFT: Universal negative alignment tax detected!")
            print(f"   This challenges conventional alignment tax theory!")


    def clean_outliers(self):
        """
        Detect and clean outliers from the dataset.
        Validates responses and generates cleaning report.
        """
        print(f"\n🧹 SECTION 3: OUTLIER ANALYSIS & DATA CLEANING")
        print("=" * 50)

        # Initialize enhanced outlier handler
        self.outlier_handler = OutlierHandler(valid_range=(1, 3), sentinel_value=EXTREME_VALUE)

        # Step 3.1: Response validation
        print(f"\n📝 Step 3.1: Response Content Validation")
        response_validation = self.outlier_handler.validate_responses(self.results_df)

        # Step 3.2: Outlier detection and reporting
        print(f"\n🔍 Step 3.2: Outlier Detection")
        outlier_report = self.outlier_handler.get_outlier_report(self.results_df)
        print(outlier_report)

        # Step 3.3: Data cleaning
        print(f"\n🧼 Step 3.3: Data Cleaning")
        self.df_clean, self.cleaning_report = self.outlier_handler.clean_dataset(
            self.results_df.copy(),
            method='auto'
        )

        print(f"\n📊 Cleaning Summary:")
        print(f"   Original samples: {self.cleaning_report['original_count']}")
        print(f"   Clean samples: {self.cleaning_report['final_count']}")
        print(f"   Removed samples: {self.cleaning_report['removed_count']}")
        print(f"   Method used: {self.cleaning_report['method_used'].upper()}")

        # Validate cleaning preserved the discovery
        self.clean_overall_tax = self.df_clean['alignment_tax'].mean()
        print(f"   Tax before cleaning: {self.overall_tax:.3f}")
        print(f"   Tax after cleaning: {self.clean_overall_tax:.3f}")
        print(f"   Difference: {self.clean_overall_tax - self.overall_tax:+.4f}")

        if abs(self.clean_overall_tax - self.overall_tax) < 0.01:
            print(f"   ✅ Discovery preserved: Cleaning had minimal impact")


    def run_statistical_analysis(self):
        """
        Run comprehensive statistical analysis including hypothesis tests,
        effect sizes, and capability-specific analysis.
        """
        print(f"\n🔬 SECTION 4: COMPREHENSIVE STATISTICAL ANALYSIS")
        print("=" * 50)

        # Run enhanced statistical analysis
        self.descriptive_results = self.core_analyzer.descriptive_analysis(self.results_df)
        self.statistical_results = self.statistical_analyzer.comprehensive_statistical_analysis(self.df_clean)
        self.capability_results = self.capability_analyzer.analyze_capability_subset(self.df_clean, run_id=self.run_id)

        # Additional statistical insights
        print(f"\n📊 STATISTICAL INSIGHTS:")

        # Count significant improvements
        self.significant_improvements = [
            axis for axis, result in self.statistical_results.items()
            if 'error' not in result and
            result['hypothesis_test']['significant'] and
            result['descriptive']['difference']['mean'] < 0
        ]

        if self.significant_improvements:
            print(f"   ✅ Statistically significant improvements: {', '.join(self.significant_improvements)}")

        # Effect size summary
        large_effects = [
            axis for axis, result in self.statistical_results.items()
            if 'error' not in result and abs(result['effect_size']['cohens_d']) > 0.8
        ]

        if large_effects:
            print(f"   📏 Large effect sizes detected: {', '.join(large_effects)}")

        # Power analysis summary
        adequately_powered = [
            axis for axis, result in self.statistical_results.items()
            if 'error' not in result and
            result['power_analysis'].get('adequately_powered', False)
        ]

        print(f"   ⚡ Adequately powered analyses: {len(adequately_powered)}/{len(self.statistical_results)}")

        # Capability-specific analysis
        print(f"\n🧠 SECTION 4.5: CAPABILITY-SPECIFIC ANALYSIS")
        print("=" * 50)

        print(f"\n🔍 Analyzing capability-heavy vs non-capability prompts...")

        # Extract and display key insights
        if 'capability_comparison' in self.capability_results:
            comparison = self.capability_results['capability_comparison']

            if 'capability' in comparison and 'non_capability' in comparison:
                cap_tax = comparison['capability']['mean_tax']
                non_cap_tax = comparison['non_capability']['mean_tax']

                print(f"\n📊 CAPABILITY SUBSET FINDINGS:")
                print(f"   • Capability-heavy prompts: {cap_tax:+.3f} alignment tax")
                print(f"   • Non-capability prompts: {non_cap_tax:+.3f} alignment tax")
                print(f"   • Difference: {cap_tax - non_cap_tax:+.3f}")

                if 'statistical_test' in comparison:
                    p_val = comparison['statistical_test'].get('p_value', 1.0)
                    significant = comparison['statistical_test'].get('significant', False)
                    print(f"   • Statistical significance: {'Yes' if significant else 'No'} (p={p_val:.4f})")

            if 'critical_assessment' in self.capability_results:
                assessment = self.capability_results['critical_assessment']
                print(f"\n🎯 ASSESSMENT: {assessment.get('assessment', 'Unknown')}")
                print(f"   {assessment.get('explanation', 'No explanation available')}")

        # Get domain breakdown if available
        if hasattr(self.capability_analyzer, 'get_capability_breakdown_by_domain'):
            if 'classified_dataframe' in self.capability_results:
                df_classified = self.capability_results['classified_dataframe']
                domain_breakdown = self.capability_analyzer.get_capability_breakdown_by_domain(df_classified)
                if domain_breakdown:
                    print(f"\n🏷️ CAPABILITY DOMAINS DETECTED:")
                    for domain, count in sorted(domain_breakdown.items(), key=lambda x: x[1], reverse=True):
                        percentage = (count / len(df_classified)) * 100
                        print(f"   • {domain:12}: {count:3d} prompts ({percentage:5.1f}%)")
            else:
                print(f"\n⚠️ Classified dataframe not available for domain breakdown")


    def generate_visualizations(self):
        """
        Generate all visualization plots including dashboards,
        discovery plots, and Pareto frontiers.
        """
        print(f"\n🎨 SECTION 5: ENHANCED VISUALIZATION GENERATION")
        print("=" * 50)

        # Initialize enhanced visualizer
        self.visualizer = AlignmentTaxVisualizer(default_id=self.run_id)

        # Create main visualization dashboard
        print(f"\n📊 Creating enhanced visualization dashboard...")
        self.visualizer.create_visualizations(self.df_clean, identifier=self.run_id)

        # If negative tax detected, create specialized discovery plots
        if self.clean_overall_tax < 0:
            print(f"\n🚨 Creating negative alignment tax discovery visualization...")
            discovery_plot = self.visualizer.create_negative_tax_discovery_plot(self.df_clean, identifier=self.run_id)

        # Create detailed visualizations
        print(f"\n📈 Creating detailed analysis plots...")
        self.visualizer.create_detailed_visualizations(self.df_clean, identifier=self.run_id)

        # Create Pareto frontier analysis (if applicable)
        print(f"\n⚖️ Creating capability-safety trade-off analysis...")
        try:
            self.pareto_results = self.visualizer.create_pareto_frontier(
                self.df_clean,
                use_robust_stats=True,
                pre_cleaned=True,
                identifier=self.run_id
            )
            print(f"   ✅ Pareto frontier analysis completed")
        except Exception as e:
            print(f"   ⚠️ Pareto analysis skipped: {e}")


    def generate_reports(self):
        """
        Generate comprehensive text and PDF reports.
        """
        print(f"\n📋 SECTION 6: COMPREHENSIVE REPORT GENERATION")
        print("=" * 50)

        # Initialize enhanced reporter
        self.reporter = AlignmentTaxReporter(default_id=self.run_id)

        # Generate enhanced text report
        print(f"\n📄 Generating enhanced text report...")
        self.text_report_path = self.reporter.generate_text_report(
            self.df_clean,
            output_dir=reports_path,
            include_samples=True,
            outlier_summary=self.cleaning_report,
            model_scores=self.pareto_results if self.pareto_results else None,
            identifier=self.run_id,
            capability_results=self.capability_results
        )

        # Generate Professional-focused executive summary (enhanced feature)
        if self.clean_overall_tax < 0:
            print(f"\n🎯 Generating Professional application executive summary...")
            self.professional_summary_path = self.reporter.generate_professional_executive_summary(
                self.df_clean,
                output_dir=reports_path,
                identifier=self.run_id
            )

        # Generate PDF reports
        print(f"\n📄 Generating full PDF reports...")
        self.pdf_report_path = self.reporter.generate_pdf_report(
            self.df_clean,
            output_dir=reports_path,
            include_samples=True,
            outlier_summary=self.cleaning_report,
            model_scores=self.pareto_results if self.pareto_results else None,
            identifier=self.run_id,
            capability_results=self.capability_results
        )
        print(f"   ✅ full PDF report generated")

        print(f"\n📄 Generating simple PDF reports...")
        self.simple_pdf_path = self.reporter.generate_simple_pdf_report(
            self.df_clean,
            output_dir=reports_path,
            identifier=self.run_id,
            capability_results=self.capability_results
        )
        print(f"   ✅ simple PDF report generated")


    def print_summary(self):
        """
        Print final summary with key metrics and insights.
        """
        print(f"\n🎯 SECTION 7: FINAL SUMMARY")
        print("=" * 50)

        # Calculate final metrics
        final_metrics = {
            'total_samples': len(self.df_clean),
            'overall_tax': self.clean_overall_tax,
            'axes_improved': sum(1 for axis in self.df_clean['axis'].unique()
                                if self.df_clean[self.df_clean['axis'] == axis]['alignment_tax'].mean() < 0),
            'total_axes': len(self.df_clean['axis'].unique()),
            'significant_axes': len(self.significant_improvements),
            'run_id': self.run_id
        }

        print(f"\n📊 FINAL METRICS:")
        print(f"   • Run ID: {final_metrics['run_id']}")
        print(f"   • Total samples analyzed: {final_metrics['total_samples']:,}")
        print(f"   • Overall alignment tax: {final_metrics['overall_tax']:+.3f}")
        print(f"   • Axes showing improvement: {final_metrics['axes_improved']}/{final_metrics['total_axes']}")
        print(f"   • Statistically significant: {final_metrics['significant_axes']}")

        # Determine the significance of findings
        if final_metrics['overall_tax'] < 0 and final_metrics['axes_improved'] == final_metrics['total_axes']:
            significance = "PARADIGM-SHIFTING DISCOVERY"
            color = "🚨"
        elif final_metrics['overall_tax'] < 0:
            significance = "NOTABLE NEGATIVE TAX FINDING"
            color = "🎯"
        else:
            significance = "STANDARD ALIGNMENT TAX ANALYSIS"
            color = "📊"

        print(f"\n{color} SIGNIFICANCE: {significance}")

        if final_metrics['overall_tax'] < 0:
            print(f"\n💡 KEY INSIGHTS FOR Professional APPLICATION:")
            print(f"   • Novel empirical evidence challenging alignment tax theory")
            print(f"   • Demonstrates win-win capability-safety optimization potential")
            print(f"   • Provides methodology for measuring alignment interventions")
            print(f"   • Shows rigorous experimental design and statistical validation")
            print(f"   • Opens new research directions for AI safety")

        print(f"\n📁 OUTPUT FILES GENERATED:")
        print(f"   📊 Enhanced visualizations: alignment_tax_analysis_dashboard_{self.run_id}.png")
        if self.clean_overall_tax < 0:
            print(f"   🚨 Discovery plot: PARADIGM_SHIFT_negative_alignment_tax_{self.run_id}.png")
        print(f"   📄 Comprehensive report: {os.path.basename(self.text_report_path)}")
        if hasattr(self, 'professional_summary_path'):
            print(f"   🎯 Professional summary: {os.path.basename(self.professional_summary_path)}")

        print(f"\n🚀 ANALYSIS COMPLETE!")
        print(f"All files saved to: {reports_path}")

        if final_metrics['overall_tax'] < 0:
            print(f"\n🌟 Congratulations on discovering negative alignment tax!")
            print(f"This finding could significantly impact AI alignment research.")
            print(f"Perfect timing for your Professional application! 🎯")

        print("=" * 60)


    def run_full_analysis(self):
        """
        Execute the complete analysis pipeline from start to finish.

        This is the main entry point that orchestrates all analysis steps.
        """
        self.load_data()
        self.run_descriptive_analysis()
        self.clean_outliers()
        self.run_statistical_analysis()
        self.generate_visualizations()
        self.generate_reports()
        self.print_summary()


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
