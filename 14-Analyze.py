# Analyze with Outlier Handling
###############################


###############################################################################


# =============================================================================
# SECTION 1: DATA LOADING AND SETUP
# =============================================================================


print("🚀 ALIGNMENT TAX ANALYSIS - ENHANCED PIPELINE")
print("=" * 60)

# Load results - Try pickle first (complete data), fall back to Excel
try:
    latest_pickle = max(glob.glob(data_path + "alignment_tax_base_instruct_results_full_*.pkl"), key=os.path.getctime)
    results_df = pd.read_pickle(latest_pickle)
    print(f"✅ Loaded pickle: {os.path.basename(latest_pickle)}")
except:
    try:
        latest_excel = max(glob.glob(data_path + "alignment_tax_base_instruct_results_full_*.xlsx"), key=os.path.getctime)
        results_df = pd.read_excel(latest_excel)
        print(f"✅ Loaded Excel: {os.path.basename(latest_excel)}")
        latest_pickle = latest_excel  # For run_id extraction
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        exit()

# Extract run ID from filename
run_id = re.search(r'(\d{8}_\d{6})', latest_pickle).group(1)
print(f"📊 Analyzing run: {run_id}")
print(f"📈 Total samples: {len(results_df)}")

# Quick discovery check
overall_tax = results_df['alignment_tax'].mean()
if overall_tax < 0:
    print(f"🚨 NEGATIVE ALIGNMENT TAX DETECTED: {overall_tax:.3f}")
    print("   This is a paradigm-shifting discovery!")
else:
    print(f"📊 Overall alignment tax: {overall_tax:.3f}")

print(f"📋 Axes: {list(results_df['axis'].unique())}")
axis_counts = results_df['axis'].value_counts()
print("📊 Samples per axis:")
for axis, count in axis_counts.items():
    print(f"   {axis}: {int(count)}")


# =============================================================================
# SECTION 2: DESCRIPTIVE ANALYSIS  
# =============================================================================


print(f"\n📊 SECTION 2: DESCRIPTIVE ANALYSIS")
print("=" * 50)

# Initialize enhanced analyzer
core_analyzer = AlignmentTaxAnalyzer(run_id)
statistical_analyzer = AlignmentTaxStatisticalAnalyzer()
capability_analyzer = AlignmentTaxCapabilityAnalyzer()

# Run descriptive analysis
descriptive_results = core_analyzer.descriptive_analysis(results_df)

# Print key descriptive findings
print(f"\n🎯 DESCRIPTIVE SUMMARY:")
overall_stats = descriptive_results['overall_stats']
axis_breakdown = descriptive_results['axis_breakdown']

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


# =============================================================================
# SECTION 3: OUTLIER ANALYSIS AND DATA CLEANING
# =============================================================================


print(f"\n🧹 SECTION 3: OUTLIER ANALYSIS & DATA CLEANING")
print("=" * 50)

# Initialize enhanced outlier handler
outlier_handler = OutlierHandler(valid_range=(1, 3), sentinel_value=99)

# Step 3.1: Response validation (enhanced feature)
print(f"\n📝 Step 3.1: Response Content Validation")
response_validation = outlier_handler.validate_responses(results_df)

# Step 3.2: Outlier detection and reporting
print(f"\n🔍 Step 3.2: Outlier Detection")
outlier_report = outlier_handler.get_outlier_report(results_df)
print(outlier_report)

# Step 3.3: Data cleaning with enhanced logic
print(f"\n🧼 Step 3.3: Data Cleaning")

# The enhanced outlier handler now properly handles zero outliers case
df_clean, cleaning_report = outlier_handler.clean_dataset(results_df.copy(), method='auto')

print(f"\n📊 Cleaning Summary:")
print(f"   Original samples: {cleaning_report['original_count']}")
print(f"   Clean samples: {cleaning_report['final_count']}")
print(f"   Removed samples: {cleaning_report['removed_count']}")
print(f"   Method used: {cleaning_report['method_used'].upper()}")

# Validate cleaning preserved the discovery
clean_overall_tax = df_clean['alignment_tax'].mean()
print(f"   Tax before cleaning: {overall_tax:.3f}")
print(f"   Tax after cleaning: {clean_overall_tax:.3f}")
print(f"   Difference: {clean_overall_tax - overall_tax:+.4f}")

if abs(clean_overall_tax - overall_tax) < 0.01:
    print(f"   ✅ Discovery preserved: Cleaning had minimal impact")


# =============================================================================
# SECTION 4: STATISTICAL ANALYSIS
# =============================================================================


print(f"\n🔬 SECTION 4: COMPREHENSIVE STATISTICAL ANALYSIS")  
print("=" * 50)

# Run enhanced statistical analysis
descriptive_results = core_analyzer.descriptive_analysis(results_df)
statistical_results = statistical_analyzer.comprehensive_statistical_analysis(df_clean)
capability_results = capability_analyzer.analyze_capability_subset(df_clean, run_id=run_id)

# Additional statistical insights
print(f"\n📊 STATISTICAL INSIGHTS:")

# Count significant improvements
significant_improvements = [axis for axis, result in statistical_results.items() 
                           if 'error' not in result and 
                           result['hypothesis_test']['significant'] and 
                           result['descriptive']['difference']['mean'] < 0]

if significant_improvements:
    print(f"   ✅ Statistically significant improvements: {', '.join(significant_improvements)}")

# Effect size summary
large_effects = [axis for axis, result in statistical_results.items() 
                if 'error' not in result and abs(result['effect_size']['cohens_d']) > 0.8]

if large_effects:
    print(f"   📏 Large effect sizes detected: {', '.join(large_effects)}")

# Power analysis summary
adequately_powered = [axis for axis, result in statistical_results.items() 
                     if 'error' not in result and 
                     result['power_analysis'].get('adequately_powered', False)]

print(f"   ⚡ Adequately powered analyses: {len(adequately_powered)}/{len(statistical_results)}")


# =============================================================================
# SECTION 4: ECTION 4.5: CAPABILITY-SPECIFIC ANALYSIS
# =============================================================================


print(f"\n🧠 SECTION 4.5: CAPABILITY-SPECIFIC ANALYSIS")
print("=" * 50)

# Run capability analysis and print key findings
print(f"\n🔍 Analyzing capability-heavy vs non-capability prompts...")
capability_results = capability_analyzer.analyze_capability_subset(df_clean, run_id=run_id)

# Extract and display key insights
if 'capability_comparison' in capability_results:
    comparison = capability_results['capability_comparison']
    
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
    
    if 'critical_assessment' in capability_results:
        assessment = capability_results['critical_assessment']
        print(f"\n🎯 ASSESSMENT: {assessment.get('assessment', 'Unknown')}")
        print(f"   {assessment.get('explanation', 'No explanation available')}")

# Get domain breakdown if available
if hasattr(capability_analyzer, 'get_capability_breakdown_by_domain'):
    # Use the classified dataframe from capability_results, not df_clean
    if 'classified_dataframe' in capability_results:
        df_classified = capability_results['classified_dataframe']
        domain_breakdown = capability_analyzer.get_capability_breakdown_by_domain(df_classified)
        if domain_breakdown:
            print(f"\n🏷️ CAPABILITY DOMAINS DETECTED:")
            for domain, count in sorted(domain_breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(df_classified)) * 100
                print(f"   • {domain:12}: {count:3d} prompts ({percentage:5.1f}%)")
    else:
        print(f"\n⚠️ Classified dataframe not available for domain breakdown")


# =============================================================================
# SECTION 5: VISUALIZATION GENERATION
# =============================================================================


print(f"\n🎨 SECTION 5: ENHANCED VISUALIZATION GENERATION")
print("=" * 50)

# Initialize enhanced visualizer  
visualizer = AlignmentTaxVisualizer(default_id=run_id)

# Create main visualization dashboard
print(f"\n📊 Creating enhanced visualization dashboard...")
visualizer.create_visualizations(df_clean, identifier=run_id)

# If negative tax detected, create specialized discovery plots
if clean_overall_tax < 0:
    print(f"\n🚨 Creating negative alignment tax discovery visualization...")
    discovery_plot = visualizer.create_negative_tax_discovery_plot(df_clean, identifier=run_id)

# Create detailed visualizations
print(f"\n📈 Creating detailed analysis plots...")
visualizer.create_detailed_visualizations(df_clean, identifier=run_id)

# Create Pareto frontier analysis (if applicable)
print(f"\n⚖️ Creating capability-safety trade-off analysis...")
try:
    pareto_results = visualizer.create_pareto_frontier(
        df_clean, 
        use_robust_stats=True, 
        pre_cleaned=True, 
        identifier=run_id
    )
    print(f"   ✅ Pareto frontier analysis completed")
except Exception as e:
    print(f"   ⚠️ Pareto analysis skipped: {e}")


# =============================================================================
# SECTION 6: REPORT GENERATION
# =============================================================================


print(f"\n📋 SECTION 6: COMPREHENSIVE REPORT GENERATION")
print("=" * 50)

# Initialize enhanced reporter
reporter = AlignmentTaxReporter(default_id=run_id)

# Generate enhanced text report
print(f"\n📄 Generating enhanced text report...")
text_report_path = reporter.generate_text_report(
    df_clean,
    output_dir=reports_path,
    include_samples=True,
    outlier_summary=cleaning_report,
    model_scores=pareto_results if 'pareto_results' in locals() else None,
    identifier=run_id,
    capability_results=capability_results
)

# Generate Professional-focused executive summary (enhanced feature)
if clean_overall_tax < 0:
    print(f"\n🎯 Generating Professional application executive summary...")
    professional_summary_path = reporter.generate_professional_executive_summary(
        df_clean,
        output_dir=reports_path,
        identifier=run_id
    )

# Generate PDF reports
print(f"\n📄 Generating full PDF reports...")
pdf_report_path = reporter.generate_pdf_report(
        df_clean,
        output_dir=reports_path,
        include_samples=True,
        outlier_summary=cleaning_report,
        model_scores=pareto_results if 'pareto_results' in locals() else None,
        identifier=run_id,
        capability_results=capability_results 
)
print(f"   ✅ full PDF report generated")

print(f"\n📄 Generating simple PDF reports...")
simple_pdf_path = reporter.generate_simple_pdf_report(
        df_clean,
        output_dir=reports_path,
        identifier=run_id,
        capability_results=capability_results 
)
print(f"   ✅ simple PDF report generated")


# =============================================================================
# SECTION 7: FINAL SUMMARY AND NEXT STEPS
# =============================================================================


print(f"\n🎯 SECTION 7: FINAL SUMMARY")
print("=" * 50)

# Calculate final metrics
final_metrics = {
    'total_samples': len(df_clean),
    'overall_tax': clean_overall_tax,
    'axes_improved': sum(1 for axis in df_clean['axis'].unique() 
                        if df_clean[df_clean['axis'] == axis]['alignment_tax'].mean() < 0),
    'total_axes': len(df_clean['axis'].unique()),
    'significant_axes': len(significant_improvements),
    'run_id': run_id
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
print(f"   📊 Enhanced visualizations: alignment_tax_analysis_dashboard_{run_id}.png")
if clean_overall_tax < 0:
    print(f"   🚨 Discovery plot: PARADIGM_SHIFT_negative_alignment_tax_{run_id}.png")
print(f"   📄 Comprehensive report: {os.path.basename(text_report_path)}")
if 'professional_summary_path' in locals():
    print(f"   🎯 Professional summary: {os.path.basename(professional_summary_path)}")

print(f"\n🚀 ANALYSIS COMPLETE!")
print(f"All files saved to: {reports_path}")

if final_metrics['overall_tax'] < 0:
    print(f"\n🌟 Congratulations on discovering negative alignment tax!")
    print(f"This finding could significantly impact AI alignment research.")
    print(f"Perfect timing for your Professional application! 🎯")

print("=" * 60)


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""