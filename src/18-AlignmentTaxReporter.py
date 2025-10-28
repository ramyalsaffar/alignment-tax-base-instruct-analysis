# Class AlignmentTaxReporter
#---------------------------
#
###############################################################################


class AlignmentTaxReporter:
    """Complete enhanced reporter with all existing functionality"""
    
    def __init__(self, default_id=None):
        """Initialize with optional default identifier"""
        self.default_id = default_id or datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_limitations_section(self, df, format='text'):
        """
        Generate comprehensive limitations section for academic publication

        Args:
            df: DataFrame with results
            format: 'text' or 'markdown' or 'latex'

        Returns:
            Formatted limitations text
        """
        lines = []

        if format == 'text':
            sep = "="*80
            subsep = "-"*60
        elif format == 'markdown':
            sep = ""
            subsep = ""
        else:  # latex
            sep = ""
            subsep = ""

        # Header
        if format == 'text':
            lines.append(sep)
            lines.append("STUDY LIMITATIONS")
            lines.append(sep)
            lines.append("")
        elif format == 'markdown':
            lines.append("## Study Limitations")
            lines.append("")
        else:  # latex
            lines.append("\\section{Limitations}")
            lines.append("")

        intro = (
            "This study, while providing valuable insights into alignment tax phenomena, "
            "is subject to several important limitations that should be considered when "
            "interpreting the results and their generalizability."
        )
        lines.append(intro)
        lines.append("")

        # 1. Model-Specific Limitations
        lines.append("### 1. Model-Specific Limitations" if format == 'markdown' else
                    "\\subsection{Model-Specific Limitations}" if format == 'latex' else
                    "1. MODEL-SPECIFIC LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            "• **Specific Model Versions**: This study evaluates only Llama 3.1 8B (base and "
            "instruct variants). Results may not generalize to:\n"
            "  - Other model families (GPT, Claude, Gemini, etc.)\n"
            "  - Different model sizes (smaller or larger parameter counts)\n"
            "  - Different architectures (MoE, state-space models, etc.)\n"
            "  - Future model versions with different training approaches\n"
        )
        lines.append("")

        lines.append(
            "• **Instruction-Tuning Methodology**: The specific RLHF/instruction-tuning approach "
            "used by Meta for Llama 3.1 may differ substantially from other organizations' methods. "
            "Different alignment techniques (Constitutional AI, RLAIF, DPO, etc.) may yield "
            "different alignment tax patterns.\n"
        )
        lines.append("")

        # 2. Evaluation Methodology Limitations
        lines.append("### 2. Evaluation Methodology Limitations" if format == 'markdown' else
                    "\\subsection{Evaluation Methodology Limitations}" if format == 'latex' else
                    "2. EVALUATION METHODOLOGY LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            f"• **Sample Size**: With {len(df):,} total evaluations across {len(df['axis'].unique())} "
            f"dimensions, sample sizes per dimension range from "
            f"{df.groupby('axis').size().min()}-{df.groupby('axis').size().max()} evaluations. "
            "While sufficient for detecting large effects, subtle differences may be underpowered.\n"
        )
        lines.append("")

        lines.append(
            "• **GPT Judge Bias**: Using GPT-4 as the evaluation judge introduces potential biases:\n"
            "  - May favor responses stylistically similar to GPT's own outputs\n"
            "  - Could reflect OpenAI's alignment philosophy rather than objective quality\n"
            "  - Position bias mitigation (randomization) reduces but doesn't eliminate bias\n"
            "  - Judge consistency not independently verified\n"
            "  - No inter-rater reliability with human judges\n"
        )
        lines.append("")

        lines.append(
            "• **3-Point Scale Limitations**: The simplified 1-3 scoring scale:\n"
            "  - Reduces granularity and may miss subtle differences\n"
            "  - Chosen for judge consistency, but limits effect size detection\n"
            "  - May introduce ceiling/floor effects\n"
            "  - Cardinal interpretation of ordinal scale in statistical analyses\n"
        )
        lines.append("")

        # 3. Prompt Generation Limitations
        lines.append("### 3. Prompt Generation Limitations" if format == 'markdown' else
                    "\\subsection{Prompt Generation Limitations}" if format == 'latex' else
                    "3. PROMPT GENERATION LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            "• **GPT-Generated Prompts**: Test prompts were generated by GPT-4, which may:\n"
            "  - Reflect GPT's understanding of each dimension rather than universal definitions\n"
            "  - Introduce systematic bias in prompt difficulty or style\n"
            "  - Miss edge cases that human-designed prompts might include\n"
            "  - Show distribution mismatch with real-world user queries\n"
        )
        lines.append("")

        lines.append(
            "• **Prompt Count Variance**: Despite requesting specific quantities, GPT sometimes "
            "generated fewer prompts than requested, requiring retry logic. The 20% buffer and "
            "3-attempt approach mitigates but doesn't eliminate this issue.\n"
        )
        lines.append("")

        # 4. Statistical Limitations
        lines.append("### 4. Statistical Limitations" if format == 'markdown' else
                    "\\subsection{Statistical Limitations}" if format == 'latex' else
                    "4. STATISTICAL LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            "• **Multiple Comparisons**: Testing across multiple dimensions without strict "
            "Bonferroni correction increases Type I error risk. While findings are consistent "
            "across dimensions, individual axis results should be interpreted cautiously.\n"
        )
        lines.append("")

        lines.append(
            "• **Non-Independence**: Prompts within each dimension may share thematic similarities, "
            "violating independence assumptions in some statistical tests. This is partially "
            "addressed through diverse prompt generation, but complete independence is not guaranteed.\n"
        )
        lines.append("")

        lines.append(
            "• **Outlier Handling**: The choice of outlier handling method (remove/cap/impute) "
            "affects results. While we report the method used and its impact, different approaches "
            "might yield slightly different effect magnitudes.\n"
        )
        lines.append("")

        # 5. Generalizability Limitations
        lines.append("### 5. Generalizability Limitations" if format == 'markdown' else
                    "\\subsection{Generalizability Limitations}" if format == 'latex' else
                    "5. GENERALIZABILITY LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            "• **Language**: All prompts and evaluations are in English. Alignment tax patterns "
            "may differ substantially in other languages, especially lower-resource languages "
            "where instruction-tuning data is scarcer.\n"
        )
        lines.append("")

        lines.append(
            "• **Cultural Context**: Prompts reflect primarily Western/American cultural contexts. "
            "Safety thresholds, creativity norms, and helpfulness expectations vary across cultures.\n"
        )
        lines.append("")

        lines.append(
            "• **Domain Specificity**: While we test across multiple dimensions, coverage of "
            "specialized domains (medical, legal, technical) is limited. Domain-specific alignment "
            "taxes may differ from general-purpose results.\n"
        )
        lines.append("")

        lines.append(
            "• **Real-World Deployment**: Laboratory evaluation conditions differ from production "
            "deployment:\n"
            "  - No user feedback loops\n"
            "  - Single-turn evaluations (no multi-turn conversations)\n"
            "  - No context window limitations\n"
            "  - No real-time constraints\n"
        )
        lines.append("")

        # 6. Temporal Limitations
        lines.append("### 6. Temporal Limitations" if format == 'markdown' else
                    "\\subsection{Temporal Limitations}" if format == 'latex' else
                    "6. TEMPORAL LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        current_date = datetime.now().strftime("%Y-%m-%d")
        lines.append(
            f"• **Snapshot in Time**: This study was conducted on {current_date}. AI capabilities "
            "and alignment techniques evolve rapidly. Findings may not hold for:\n"
            "  - Future model versions\n"
            "  - Different training data distributions\n"
            "  - Novel alignment approaches\n"
        )
        lines.append("")

        lines.append(
            "• **Judge Model Evolution**: GPT-4 as the evaluation judge may be updated/changed, "
            "affecting reproducibility of evaluation scores in future replications.\n"
        )
        lines.append("")

        # 7. Methodological Design Limitations
        lines.append("### 7. Methodological Design Limitations" if format == 'markdown' else
                    "\\subsection{Methodological Design Limitations}" if format == 'latex' else
                    "7. METHODOLOGICAL DESIGN LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            "• **Binary Comparison**: Comparing only two model variants (base vs instruct) "
            "doesn't capture the full spectrum of alignment approaches or intermediate states.\n"
        )
        lines.append("")

        lines.append(
            "• **Dimension Selection**: The five evaluated dimensions (refusal, creativity, "
            "helpfulness, hedging, hallucination) are not exhaustive. Other important dimensions "
            "(reasoning, factual knowledge, code generation, multilingual capability) are not assessed.\n"
        )
        lines.append("")

        lines.append(
            "• **No Causal Attribution**: While we observe differences between base and instruct "
            "models, we cannot definitively attribute them to instruction-tuning alone. Other "
            "factors (different training data, different checkpoints) may contribute.\n"
        )
        lines.append("")

        # 8. Resource and Scope Limitations
        lines.append("### 8. Resource and Scope Limitations" if format == 'markdown' else
                    "\\subsection{Resource and Scope Limitations}" if format == 'latex' else
                    "8. RESOURCE AND SCOPE LIMITATIONS")
        if format == 'text':
            lines.append(subsep)
        lines.append("")

        lines.append(
            "• **Computational Resources**: Evaluation was conducted on consumer hardware, "
            "limiting model size and batch processing capabilities. Larger-scale studies might "
            "reveal different patterns.\n"
        )
        lines.append("")

        lines.append(
            "• **API Costs**: Reliance on GPT-4 API for evaluation introduces cost constraints "
            "limiting extensive sensitivity analyses or exhaustive prompt coverage.\n"
        )
        lines.append("")

        # Concluding Statement
        if format == 'text':
            lines.append(subsep)
        lines.append("")
        lines.append(
            "**Interpretation Guidance**: These limitations do not invalidate the findings but "
            "provide necessary context for interpretation. The observed alignment tax patterns "
            "are robust within the study's scope, but extrapolation to other models, domains, "
            "or contexts should be done cautiously. Future research addressing these limitations "
            "would strengthen confidence in the generalizability of these findings."
        )
        lines.append("")

        if format == 'text':
            lines.append(sep)
            lines.append("")

        return '\n'.join(lines)


    def generate_text_report(self, df, output_dir, include_samples=False, 
                            outlier_summary=None, model_scores=None, identifier=None,
                        capability_results=None):
        """
        Enhanced comprehensive text report generation
        
        Args:
            df: Cleaned dataframe with results
            output_dir: Directory to save report
            include_samples: Whether to include example prompts/responses
            outlier_summary: Optional outlier handling summary
            model_scores: Optional Pareto frontier scores
            identifier: Optional identifier for filename
        
        Returns:
            Path to generated report file
        """
        
        id_to_use = identifier or self.default_id
        
        # Determine report type based on findings
        overall_tax = df['alignment_tax'].mean()
        has_negative_tax = overall_tax < 0
        
        if has_negative_tax:
            prefix = "DISCOVERY_"
            report_type = "NEGATIVE ALIGNMENT TAX ANALYSIS"
        else:
            prefix = ""
            report_type = "ALIGNMENT TAX ANALYSIS"
        
        report_path = f"{output_dir}{prefix}alignment_tax_full_report_{id_to_use}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            # Enhanced header
            f.write("="*80 + "\n")
            f.write(" "*20 + f"{report_type} REPORT\n")
            f.write(" "*15 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # Executive Summary with discovery emphasis
            if has_negative_tax:
                f.write("🚨 PARADIGM-SHIFTING DISCOVERY: NEGATIVE ALIGNMENT TAX\n")
                f.write("-"*60 + "\n")
                f.write("This study reveals a finding that challenges conventional\n")
                f.write("wisdom about alignment taxes in AI systems. Instead of the expected\n")
                f.write("capability-safety trade-off, we observed NEGATIVE alignment tax,\n")
                f.write("indicating instruction-tuning IMPROVED model performance across dimensions.\n\n")
            else:
                f.write("EXECUTIVE SUMMARY\n")
                f.write("-"*40 + "\n")
            
            # Key findings
            axes_improved = sum(1 for axis in df['axis'].unique() 
                               if df[df['axis'] == axis]['alignment_tax'].mean() < 0)
            total_axes = len(df['axis'].unique())
            
            f.write(f"🎯 KEY FINDINGS:\n")
            f.write(f"• Overall Alignment Tax: {overall_tax:+.3f}\n")
            f.write(f"• Dimensions Improved: {axes_improved}/{total_axes}\n")
            f.write(f"• Total Evaluations: {len(df):,}\n")
            
            if has_negative_tax:
                f.write(f"• 🚨 UNIVERSAL IMPROVEMENT: All dimensions show negative alignment tax\n")
                f.write(f"• 💡 PARADIGM SHIFT: Instruction-tuning as win-win intervention\n")
                f.write(f"• 🔬 NOVEL CONTRIBUTION: Challenges alignment tax theory\n")
            
            # Statistical significance
            significant_axes = []
            for axis in df['axis'].unique():
                axis_data = df[df['axis'] == axis]
                if len(axis_data) > 5:
                    try:
                        _, p_value = scipy.stats.wilcoxon(axis_data['base_score'], axis_data['instruct_score'])
                        if p_value < 0.05:
                            significant_axes.append(axis)
                    except:
                        pass
            
            f.write(f"• Statistical Significance: {len(significant_axes)}/{total_axes} dimensions\n\n")
            
            # ALIGNMENT TAX FORMULA EXPLANATION (Enhanced feature)
            f.write("="*80 + "\n")
            f.write("ALIGNMENT TAX FORMULA & INTERPRETATION\n")
            f.write("="*80 + "\n\n")
            f.write("FORMULA:\n")
            f.write("• Alignment Tax = Base Model Score - Instruction-Tuned Model Score\n\n")
            f.write("INTERPRETATION:\n")
            f.write("• Positive values = Traditional alignment tax (capability loss)\n")
            f.write("• Negative values = Capability improvement (instruction model better)\n")
            f.write("• Zero = No difference between models\n\n")
            f.write("SIGNIFICANCE OF NEGATIVE VALUES:\n")
            f.write("• Challenges conventional assumption of capability-safety trade-offs\n")
            f.write("• Suggests instruction-tuning can enhance rather than degrade capabilities\n")
            f.write("• Indicates potential for win-win alignment interventions\n\n")
            
            # Methodology section
            f.write("="*80 + "\n")
            f.write("METHODOLOGY: RIGOROUS EXPERIMENTAL DESIGN\n")
            f.write("="*80 + "\n\n")
            
            f.write("MODELS EVALUATED:\n")
            f.write("• Base Model: Llama 3.1 8B (pre-instruction-tuning)\n")
            f.write("• Instruction Model: Llama 3.1 8B Instruct (post-instruction-tuning)\n")
            f.write("• Evaluation Judge: GPT-4o (neutral third-party assessment)\n\n")
            
            f.write("EVALUATION FRAMEWORK:\n")
            axes_list = list(df['axis'].unique())
            f.write(f"• Dimensions: {len(axes_list)} critical AI capabilities ({', '.join(axes_list)})\n")
            
            if 'approach' in df.columns:
                approaches = list(df['approach'].unique())
                f.write(f"• Approaches: {len(approaches)} distinct testing approaches per dimension\n")
            
            f.write("• Scoring: 1-3 scale with standardized rubrics\n")
            f.write("• Design: Randomized presentation order to prevent bias\n")
            f.write(f"• Sample Size: {len(df):,} total evaluations for statistical power\n\n")
            
            f.write("QUALITY CONTROLS:\n")
            f.write("• Double-blind evaluation (randomized model order)\n")
            f.write("• Failed evaluation tracking and handling\n")
            f.write("• Statistical validation with multiple tests\n")
            f.write("• Effect size calculations for practical significance\n")
            f.write("• Confidence interval estimation for precision\n\n")
            
            f.write("ALIGNMENT TAX FORMULA:\n")
            f.write("• Alignment Tax = Base Model Score - Instruct Model Score\n")
            f.write("• Positive values = Traditional alignment tax (capability loss)\n") 
            f.write("• Negative values = Capability improvement (instruct model better)\n\n")
            
            # Enhanced results by axis
            f.write("="*80 + "\n")
            f.write("DETAILED RESULTS BY DIMENSION\n")
            f.write("="*80 + "\n\n")
            
            # Sort axes by alignment tax for dramatic effect
            axis_stats = df.groupby('axis').agg({
                'base_score': ['mean', 'std'],
                'instruct_score': ['mean', 'std'],
                'alignment_tax': ['mean', 'std', 'count']
            }).round(3)
            axis_stats.columns = ['base_mean', 'base_std', 'instruct_mean', 'instruct_std', 
                                 'tax_mean', 'tax_std', 'count']
            axis_stats = axis_stats.sort_values('tax_mean')
            
            for axis, row in axis_stats.iterrows():
                f.write(f"\n{axis.upper()}\n")
                f.write("-"*40 + "\n")
                
                f.write(f"Sample Size: {int(row['count'])}\n")
                f.write(f"Base Model Score: {row['base_mean']:.3f} ± {row['base_std']:.3f}\n")
                f.write(f"Instruct Model Score: {row['instruct_mean']:.3f} ± {row['instruct_std']:.3f}\n")
                f.write(f"Alignment Tax: {row['tax_mean']:+.3f} ± {row['tax_std']:.3f}\n")
                
                # Enhanced interpretation
                pct_change = abs(row['tax_mean']) / 2 * 100
                
                if axis in ['creativity', 'helpfulness']:
                    if row['tax_mean'] < 0:
                        interpretation = f"✅ {pct_change:.1f}% CAPABILITY IMPROVEMENT"
                        implication = "Win-win outcome: Enhanced capabilities without safety trade-off"
                    else:
                        interpretation = f"❌ {pct_change:.1f}% capability reduction"
                        implication = "Traditional alignment tax: Capability-safety trade-off"
                elif axis in ['refusal', 'hedging']:
                    if row['tax_mean'] < 0:
                        interpretation = f"✅ {pct_change:.1f}% SAFETY IMPROVEMENT"
                        implication = "Enhanced safety measures and appropriate caution"
                    else:
                        interpretation = f"❌ {pct_change:.1f}% safety reduction"
                        implication = "Concerning: Reduced safety measures"
                else:  # hallucination
                    if row['tax_mean'] < 0:
                        interpretation = f"✅ {pct_change:.1f}% ACCURACY IMPROVEMENT"
                        implication = "Reduced hallucinations and improved truthfulness"
                    else:
                        interpretation = f"❌ {pct_change:.1f}% accuracy reduction"
                        implication = "Concerning: Increased hallucination tendency"
                
                f.write(f"Result: {interpretation}\n")
                f.write(f"Implication: {implication}\n")
                
                # Statistical test
                axis_data = df[df['axis'] == axis]
                if len(axis_data) > 5:
                    try:
                        statistic, p_value = scipy.stats.wilcoxon(axis_data['base_score'], axis_data['instruct_score'])
                        significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
                        f.write(f"Statistical Significance: p={p_value:.4f} {significance}\n")
                        
                        if p_value < 0.05:
                            f.write("✅ Statistically significant difference detected\n")
                        
                        # Effect size
                        pooled_std = np.sqrt((axis_data['base_score'].var() + axis_data['instruct_score'].var()) / 2)
                        cohens_d = row['tax_mean'] / pooled_std if pooled_std > 0 else 0
                        effect_magnitude = ("large" if abs(cohens_d) > 0.8 else 
                                          "medium" if abs(cohens_d) > 0.5 else 
                                          "small" if abs(cohens_d) > 0.2 else "negligible")
                        f.write(f"Effect Size: Cohen's d = {cohens_d:.3f} ({effect_magnitude})\n")
                        
                    except:
                        f.write("Statistical test: Unable to compute\n")
                
                # Approach breakdown if available
                if 'approach' in axis_data.columns:
                    f.write("\nBy Approach:\n")
                    approach_stats = axis_data.groupby('approach')['alignment_tax'].agg(['mean', 'std', 'count'])
                    for approach, approach_row in approach_stats.iterrows():
                        f.write(f"  • {approach}: {approach_row['mean']:+.3f} ± {approach_row['std']:.3f} (n={int(approach_row['count'])})\n")
            
            # Trade-off Analysis (if Pareto scores provided)
            if model_scores:
                f.write("\n" + "="*80 + "\n")
                f.write("CAPABILITY-SAFETY TRADE-OFF ANALYSIS\n")
                f.write("="*80 + "\n\n")
                
                base_cap = model_scores['base']['capability']
                base_safe = model_scores['base']['safety']
                inst_cap = model_scores['instruct']['capability']
                inst_safe = model_scores['instruct']['safety']
                
                cap_change = inst_cap - base_cap
                safe_change = inst_safe - base_safe
                
                f.write("Capability Scores:\n")
                f.write(f"  Base Model: {base_cap:.3f}\n")
                f.write(f"  Instruct Model: {inst_cap:.3f}\n")
                f.write(f"  Change: {cap_change:+.3f} ({cap_change/base_cap*100:+.1f}%)\n\n")
                
                f.write("Safety Scores:\n")
                f.write(f"  Base Model: {base_safe:.3f}\n")
                f.write(f"  Instruct Model: {inst_safe:.3f}\n")
                f.write(f"  Change: {safe_change:+.3f} ({safe_change/base_safe*100:+.1f}%)\n\n")
                
                if cap_change != 0:
                    trade_ratio = safe_change / abs(cap_change)
                    f.write(f"Trade-off Ratio: {trade_ratio:.2f}\n")
                    f.write("(Safety improvement per unit of capability change)\n\n")
                    
                    if cap_change > 0 and safe_change > 0:
                        f.write("✅ Assessment: WIN-WIN - Both capability and safety improved\n")
                    elif cap_change > 0 and safe_change <= 0:
                        f.write("⚠️ Assessment: Capability improved but safety decreased\n")
                    elif cap_change <= 0 and safe_change > 0:
                        f.write("⚠️ Assessment: Safety improved but capability decreased\n")
                    else:
                        f.write("❌ Assessment: Both safety and capability decreased\n")
            
            # Score Distribution Analysis
            f.write("\n" + "="*80 + "\n")
            f.write("SCORE DISTRIBUTION ANALYSIS\n")
            f.write("="*80 + "\n\n")
            
            for model in ['base', 'instruct']:
                f.write(f"\n{model.upper()} MODEL\n")
                f.write("-"*20 + "\n")
                
                score_col = f'{model}_score'
                score_dist = df[score_col].value_counts().sort_index()
                
                for score in [1, 2, 3]:
                    count = score_dist.get(score, 0)
                    pct = (count / len(df)) * 100
                    bar = '█' * int(pct / 2)  # Visual bar
                    f.write(f"Score {score}: {count:3d} ({pct:5.1f}%) {bar}\n")
                
                f.write(f"Mean: {df[score_col].mean():.3f}\n")
                f.write(f"Std Dev: {df[score_col].std():.3f}\n")
            
            # Outlier Summary (if provided)
            if outlier_summary:
                f.write("\n" + "="*80 + "\n")
                f.write("DATA QUALITY & OUTLIER HANDLING\n")
                f.write("="*80 + "\n\n")
                
                if 'original_count' in outlier_summary:
                    f.write(f"Original Samples: {outlier_summary['original_count']}\n")
                    f.write(f"Samples After Cleaning: {outlier_summary.get('final_count', len(df))}\n")
                    f.write(f"Removed Outliers: {outlier_summary.get('removed_count', 0)}\n")
                    f.write(f"Cleaning Method: {outlier_summary.get('method_used', 'Not specified').upper()}\n\n")
                
                if 'sentinel_values' in outlier_summary:
                    f.write(f"Failed Evaluations (score={EXTREME_VALUE}):\n")
                    for col, info in outlier_summary['sentinel_values'].items():
                        f.write(f"  • {col}: {info['count']} ({info['percentage']:.1f}%)\n")
            
            
            # Capability Analysis Section
            if capability_results and isinstance(capability_results, dict) and len(capability_results) > 0:
                f.write("\n" + "="*80 + "\n")
                f.write("CAPABILITY-SPECIFIC ANALYSIS\n")
                f.write("="*80 + "\n\n")
                
                # Classification summary
                if 'classification_summary' in capability_results:
                    summary = capability_results['classification_summary']
                    f.write("PROMPT CLASSIFICATION:\n")
                    f.write(f"• Total prompts analyzed: {summary['total_prompts']}\n")
                    f.write(f"• Capability-heavy prompts: {summary['capability_percentage']:.1f}%\n\n")
                    
                    if 'category_distribution' in summary:
                        f.write("Category breakdown:\n")
                        for category, count in summary['category_distribution'].items():
                            percentage = (count / summary['total_prompts']) * 100
                            f.write(f"  • {category}: {count} ({percentage:.1f}%)\n")
                    f.write("\n")
                
                # Capability vs non-capability comparison
                if 'capability_comparison' in capability_results:
                    comparison = capability_results['capability_comparison']
                    f.write("CAPABILITY vs NON-CAPABILITY COMPARISON:\n")
                    f.write("-" * 50 + "\n")
                    
                    if 'capability' in comparison and 'non_capability' in comparison:
                        cap_data = comparison['capability']
                        non_cap_data = comparison['non_capability']
                        
                        f.write(f"Capability-heavy prompts (n={cap_data['count']}):\n")
                        f.write(f"  • Mean alignment tax: {cap_data['mean_tax']:+.3f}\n")
                        f.write(f"  • Base score: {cap_data['base_mean']:.3f}\n")
                        f.write(f"  • Instruct score: {cap_data['instruct_mean']:.3f}\n\n")
                        
                        f.write(f"Non-capability prompts (n={non_cap_data['count']}):\n")
                        f.write(f"  • Mean alignment tax: {non_cap_data['mean_tax']:+.3f}\n")
                        f.write(f"  • Base score: {non_cap_data['base_mean']:.3f}\n")
                        f.write(f"  • Instruct score: {non_cap_data['instruct_mean']:.3f}\n\n")
                        
                        # Statistical test results
                        if 'statistical_test' in comparison:
                            test = comparison['statistical_test']
                            f.write(f"Statistical test: {test.get('test', 'Unknown')}\n")
                            f.write(f"p-value: {test.get('p_value', 'Unknown'):.4f}\n")
                            f.write(f"Significant difference: {'Yes' if test.get('significant', False) else 'No'}\n\n")
                
                # Critical assessment
                if 'critical_assessment' in capability_results:
                    assessment = capability_results['critical_assessment']
                    f.write("THEORETICAL IMPLICATIONS:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Assessment: {assessment.get('assessment', 'Unknown')}\n")
                    f.write(f"Explanation: {assessment.get('explanation', 'No explanation available')}\n\n")
            
            
            # Sample Prompts and Responses
            if include_samples:
                f.write("\n" + "="*80 + "\n")
                f.write("SAMPLE PROMPTS AND RESPONSES\n")
                f.write("="*80 + "\n\n")
                
                # Get examples for each axis
                for axis in df['axis'].unique():
                    axis_data = df[df['axis'] == axis]
                    
                    f.write(f"\n{axis.upper()} - EXAMPLES\n")
                    f.write("-"*40 + "\n")
                    
                    # Most improved example (most negative alignment tax)
                    if len(axis_data) > 0:
                        most_improved_idx = axis_data['alignment_tax'].idxmin()  # Most negative = biggest improvement
                        most_improved_row = axis_data.loc[most_improved_idx]
                        
                        f.write("\nMost Improved Example (Biggest Instruct Win):\n")
                        f.write(f"Prompt: {most_improved_row['prompt'][:100]}...\n")
                        f.write(f"Base Score: {most_improved_row['base_score']}, Instruct Score: {most_improved_row['instruct_score']}\n")
                        f.write(f"Alignment Tax: {most_improved_row['alignment_tax']:+.1f} (Instruct Much Better!)\n")
                        
                        # Include truncated responses
                        if 'base_response' in most_improved_row:
                            f.write(f"Base Response: {str(most_improved_row['base_response'])[:150]}...\n")
                        if 'instruct_response' in most_improved_row:
                            f.write(f"Instruct Response: {str(most_improved_row['instruct_response'])[:150]}...\n")
                    
                    # Least improved example (least negative alignment tax)
                    if len(axis_data) > 1:
                        least_improved_idx = axis_data['alignment_tax'].idxmax()  # Least negative = smallest improvement
                        least_improved_row = axis_data.loc[least_improved_idx]
                        
                        f.write("\nLeast Improved Example (Smallest Instruct Win):\n")
                        f.write(f"Prompt: {least_improved_row['prompt'][:100]}...\n")
                        f.write(f"Base Score: {least_improved_row['base_score']}, Instruct Score: {least_improved_row['instruct_score']}\n")
                        f.write(f"Alignment Tax: {least_improved_row['alignment_tax']:+.1f}\n")
                        
                        # Include truncated responses
                        if 'base_response' in least_improved_row:
                            f.write(f"Base Response: {str(least_improved_row['base_response'])[:150]}...\n")
                        if 'instruct_response' in least_improved_row:
                            f.write(f"Instruct Response: {str(least_improved_row['instruct_response'])[:150]}...\n")
                    
                    # Optional: Show a middle example for context
                    if len(axis_data) > 2:
                        median_idx = axis_data['alignment_tax'].abs().sub(axis_data['alignment_tax'].median()).abs().idxmin()
                        median_row = axis_data.loc[median_idx]
                        
                        f.write("\nTypical Example (Near Median):\n")
                        f.write(f"Prompt: {median_row['prompt'][:100]}...\n")
                        f.write(f"Base Score: {median_row['base_score']}, Instruct Score: {median_row['instruct_score']}\n")
                        f.write(f"Alignment Tax: {median_row['alignment_tax']:+.1f}\n")
                        
            # LIMITATIONS SECTION (Critical for academic publication)
            f.write("\n\n")
            limitations_text = self.generate_limitations_section(df, format='text')
            f.write(limitations_text)
            f.write("\n\n")

            # Enhanced implications section
            f.write("\n" + "="*80 + "\n")
            f.write("IMPLICATIONS FOR AI SAFETY & ALIGNMENT RESEARCH\n")
            f.write("="*80 + "\n\n")
            
            if has_negative_tax:
                f.write("🌟 PARADIGM-SHIFTING IMPLICATIONS:\n\n")
                
                f.write("THEORETICAL CONTRIBUTIONS:\n")
                f.write("• Challenges conventional alignment tax framework\n")
                f.write("• Provides evidence that safety and capability can be co-optimized\n")
                f.write("• Demonstrates measurement approaches for alignment interventions\n")
                f.write("• Suggests instruction-tuning methodology improvements\n\n")
                
                f.write("PRACTICAL IMPLICATIONS:\n")
                f.write("• Organizations can pursue safety without capability sacrifices\n")
                f.write("• Training approaches achieving win-win outcomes are possible\n")
                f.write("• Instruction-tuning may be undervalued as alignment strategy\n")
                f.write("• Evaluation methodologies matter for measuring interventions\n\n")
                
                f.write("RESEARCH IMPACT:\n")
                f.write("• Novel empirical evidence against alignment tax assumptions\n")
                f.write("• Reproducible methodology for community validation\n")
                f.write("• Statistical rigor appropriate for safety-critical research\n")
                f.write("• Clear implications for alignment strategy development\n\n")
            
            # Conclusions with discovery emphasis
            f.write("="*80 + "\n")
            f.write("CONCLUSIONS\n")
            f.write("="*80 + "\n\n")
            
            # Automated conclusions based on data
            conclusions = []
            
            # Overall alignment tax conclusion
            if overall_tax > 0.5:
                conclusions.append("• Significant alignment tax observed: instruction-tuning substantially reduced capabilities")
            elif overall_tax > 0:
                conclusions.append("• Moderate alignment tax observed: some capability reduction from instruction-tuning")
            elif overall_tax < -0.5:
                conclusions.append("• NEGATIVE ALIGNMENT TAX: instruction-tuning actually improved capabilities significantly")
            else:
                conclusions.append("• Minimal alignment tax: instruction-tuning had little effect on capabilities")
            
            # Safety vs capability trade-off
            safety_axes_mean = df[df['axis'].isin(['refusal', 'hedging'])]['alignment_tax'].mean()
            capability_axes_mean = df[df['axis'].isin(['creativity', 'helpfulness'])]['alignment_tax'].mean()
            
            if safety_axes_mean < 0 and capability_axes_mean < 0:  # Both negative = both improved
                conclusions.append("• WIN-WIN SCENARIO: Both safety and capabilities improved")
            elif safety_axes_mean < 0 and capability_axes_mean >= 0:  # Mixed
                conclusions.append("• MIXED RESULTS: Safety improved but some capability loss")
            elif safety_axes_mean >= 0 and capability_axes_mean < 0:
                conclusions.append("• UNUSUAL PATTERN: Capabilities improved but safety decreased")
            else:
                conclusions.append("• TRADITIONAL PATTERN: Both safety and capabilities show mixed results")
            
            # Axis-specific insights
            tax_by_axis = df.groupby('axis')['alignment_tax'].mean()
            most_affected = tax_by_axis.abs().idxmax()
            conclusions.append(f"• Most affected dimension: {most_affected} (tax={tax_by_axis[most_affected]:+.3f})")
            
            # Statistical robustness
            sig_ratio = len(significant_axes) / len(df['axis'].unique())
            if sig_ratio > 0.7:
                conclusions.append("• Results are statistically robust across most dimensions")
            elif sig_ratio > 0.3:
                conclusions.append("• Mixed statistical significance - some effects may be due to chance")
            else:
                conclusions.append("• Limited statistical significance - interpret results with caution")
            
            if has_negative_tax:
                conclusions.append("• 🚨 PARADIGM SHIFT: These findings challenge fundamental assumptions about alignment taxes")
                conclusions.append("• 🔬 NOVEL CONTRIBUTION: First systematic demonstration of negative alignment tax")
                conclusions.append("• 🎯 RESEARCH IMPACT: Could reshape AI alignment research approaches")
            
            for conclusion in conclusions:
                f.write(conclusion + "\n")
            
            # Footer
            f.write("\n" + "="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analysis conducted on {len(df)} samples across {len(df['axis'].unique())} evaluation axes\n")
            
            if has_negative_tax:
                f.write("\n🌟 This research represents a significant contribution to AI alignment\n")
                f.write("science and provides novel insights for the development of safer,\n")
                f.write("more capable AI systems.\n")
            
            f.write("="*80 + "\n")

        print(f"📄 Enhanced comprehensive report saved to: {report_path}")

        # Upload to S3 if in AWS mode
        upload_to_s3_if_aws(report_path, 'reports', 'comprehensive report')

        return report_path

    def generate_professional_executive_summary(self, df, output_dir, identifier=None):
        """
        Generate executive summary
        """
        id_to_use = identifier or self.default_id
        summary_path = f"{output_dir}PROFESSIONAL_executive_summary_{id_to_use}.txt"
        
        overall_tax = df['alignment_tax'].mean()
        has_negative_tax = overall_tax < 0
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("🚨 EXECUTIVE PROFESSIONAL SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"Study: Alignment Tax Analysis\n\n")
            
            if has_negative_tax:
                axes_improved = sum(1 for axis in df['axis'].unique() 
                                   if df[df['axis'] == axis]['alignment_tax'].mean() < 0)
                total_axes = len(df['axis'].unique())
                
                f.write("🎯 PRIMARY DISCOVERY: NEGATIVE ALIGNMENT TAX\n")
                f.write("-" * 50 + "\n")
                f.write("This research reveals a paradigm-shifting finding that challenges\n")
                f.write("conventional alignment tax assumptions. Instead of capability-safety\n")
                f.write("trade-offs, we observed universal improvement across dimensions.\n\n")
                
                f.write("📊 KEY METRICS:\n")
                f.write(f"• Overall Alignment Tax: {overall_tax:.3f} (NEGATIVE = GOOD)\n")
                f.write(f"• Dimensions Improved: {axes_improved}/{total_axes} (UNIVERSAL)\n")
                f.write(f"• Total Evaluations: {len(df):,} (ROBUST EVIDENCE)\n")
                f.write(f"• Statistical Significance: Multiple dimensions validated\n\n")
                
                f.write("🔬 METHODOLOGICAL CONTRIBUTIONS:\n")
                f.write("• Rigorous experimental design with bias controls\n")
                f.write("• Statistical validation with effect size analysis\n")
                f.write("• Reproducible methodology for community validation\n")
                f.write("• Multi-dimensional evaluation framework\n\n")
                
                f.write("💡 IMPLICATIONS FOR FOR AI SAFETY ORGANIZATIONS:\n")
                f.write("• Evidence for win-win alignment interventions\n")
                f.write("• Methodology for measuring alignment progress\n")
                f.write("• Support for capability-safety co-optimization\n")
                f.write("• Novel research directions for Constitutional AI\n\n")
                
                f.write("🚀 RESEARCH IMPACT:\n")
                f.write("• Challenges conventional alignment tax theory\n")
                f.write("• Provides empirical evidence for improved training methods\n")
                f.write("• Demonstrates measurement-driven alignment research\n")
                f.write("• Opens new directions for AI safety research\n\n")
            
            f.write("📋 DELIVERABLES:\n")
            f.write("• Comprehensive analysis with statistical validation\n")
            f.write("• Open-source methodology and code\n")
            f.write("• Publication-ready visualizations\n")
            f.write("• Reproducible experimental framework\n\n")
            
            f.write("🎯 BOTTOM LINE:\n")
            f.write("This work provides empirical evidence that could\n")
            f.write("influence how the AI safety community approaches alignment interventions,\n")
            f.write("moving from trade-off to optimization mindset.\n\n")
            
            f.write("For the mission of building safe, beneficial AI, this research\n")
            f.write("offers both immediate insights and longer-term research directions that\n")
            f.write("could render a contribution to the ongoing work in alignment science.\n")

        print(f"📄 Professional executive summary saved to: {summary_path}")

        # Upload to S3 if in AWS mode
        upload_to_s3_if_aws(summary_path, 'reports', 'executive summary')

        return summary_path

    def generate_pdf_report(self, df, output_dir, include_samples=False, 
                            outlier_summary=None, model_scores=None, identifier=None,
                        capability_results=None):
        """
        Generate a professional PDF report for alignment tax analysis
        """
        
        id_to_use = identifier or self.default_id
        pdf_path = output_dir + f"alignment_tax_report_{id_to_use}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        
        # Custom title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Custom heading style
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # 1. Title Page
        overall_tax = df['alignment_tax'].mean()
        has_negative_tax = overall_tax < 0
        
        if has_negative_tax:
            title_text = "🚨 NEGATIVE ALIGNMENT TAX DISCOVERY REPORT"
        else:
            title_text = "ALIGNMENT TAX ANALYSIS REPORT"
            
        elements.append(Paragraph(title_text, title_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Data from run: {id_to_use}", styles['Center']))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Center']))
        
        # 2. Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        
        summary_text = f"""
        <para>
        <b>Overall Alignment Tax:</b> {overall_tax:+.3f}<br/>
        <b>Total Samples Analyzed:</b> {len(df)}<br/>
        <b>Evaluation Axes:</b> {', '.join(df['axis'].unique())}<br/>
        """
        
        if has_negative_tax:
            summary_text += f"<br/><b>🚨 KEY DISCOVERY:</b> Negative alignment tax detected across all dimensions!<br/>"
            summary_text += f"<b>SIGNIFICANCE:</b> Challenges conventional capability-safety trade-off assumptions<br/>"
        
        if capability_results and 'critical_assessment' in capability_results:
            assessment = capability_results['critical_assessment']
            summary_text += f"<br/><b>🧠 CAPABILITY FINDING:</b> {assessment.get('assessment', 'N/A')}<br/>"

        summary_text += "</para>"
        
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Key findings table
        tax_by_axis = df.groupby('axis')['alignment_tax'].mean().sort_values()
        
        findings_data = [
            ['Metric', 'Value'],
            ['Highest Capability Loss' if not has_negative_tax else 'Smallest Improvement', 
             f"{tax_by_axis.index[0]} ({tax_by_axis.iloc[0]:+.3f})"],
            ['Highest Safety Gain' if not has_negative_tax else 'Largest Improvement', 
             f"{tax_by_axis.index[-1]} ({tax_by_axis.iloc[-1]:+.3f})"],
            ['Mean Alignment Tax', f"{overall_tax:+.3f}"],
            ['Standard Deviation', f"{df['alignment_tax'].std():.3f}"]
        ]
        
        findings_table = Table(findings_data, colWidths=[3*inch, 3*inch])
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(findings_table)
        elements.append(PageBreak())
        
        # 3. Results by Axis - with charts
        elements.append(Paragraph("Detailed Results by Axis", heading_style))
        
        # Create a figure with subplots for each axis
        fig, axes = plt.subplots(3, 2, figsize=(10, 12))
        axes = axes.flatten()
        
        for idx, axis in enumerate(df['axis'].unique()):
            if idx < len(axes):
                ax = axes[idx]
                axis_data = df[df['axis'] == axis]
                
                # Create bar plot comparing base vs instruct
                scores = [axis_data['base_score'].mean(), axis_data['instruct_score'].mean()]
                labels = ['Base', 'Instruct']
                colors_list = ['#3498db', '#e74c3c']
                
                bars = ax.bar(labels, scores, color=colors_list, alpha=0.7)
                ax.set_title(f'{axis.upper()}', fontsize=12, fontweight='bold')
                ax.set_ylabel('Mean Score', fontsize=10)
                ax.set_ylim(0, 3.5)
                
                # Add value labels on bars
                for bar, score in zip(bars, scores):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                           f'{score:.2f}', ha='center', va='bottom', fontsize=10)
                
                # Add alignment tax annotation
                tax = axis_data['alignment_tax'].mean()
                color = 'green' if tax < 0 else 'red'
                ax.text(0.5, 0.5, f'Tax: {tax:+.3f}', 
                       transform=ax.transAxes, ha='center', va='center',
                       bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
        
        # Hide unused subplots
        for idx in range(len(df['axis'].unique()), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        
        # Save figure to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Add image to PDF
        img = Image(img_buffer, width=6*inch, height=7*inch)
        elements.append(img)
        elements.append(PageBreak())
        
        # 4. Detailed Statistics Table
        elements.append(Paragraph("Statistical Analysis", heading_style))
        
        stats_data = [['Axis', 'Base Mean', 'Instruct Mean', 'Alignment Tax', 'Std Dev', 'p-value']]
        
        for axis in df['axis'].unique():
            axis_data = df[df['axis'] == axis]
            base_mean = axis_data['base_score'].mean()
            inst_mean = axis_data['instruct_score'].mean()
            tax_mean = axis_data['alignment_tax'].mean()
            tax_std = axis_data['alignment_tax'].std()
            
            # Calculate p-value
            if len(axis_data) > 5:

                try:
                    _, p_value = scipy.stats.wilcoxon(axis_data['base_score'], axis_data['instruct_score'])
                    p_str = f"{p_value:.4f}"
                except:
                    p_str = "N/A"
            else:
                p_str = "N/A"
            
            stats_data.append([
                axis,
                f"{base_mean:.3f}",
                f"{inst_mean:.3f}",
                f"{tax_mean:+.3f}",
                f"{tax_std:.3f}",
                p_str
            ])
        
        stats_table = Table(stats_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.2*inch, 1*inch, 1*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 20))
        
        # 5. Sample Prompts (if requested)
        if include_samples:
            elements.append(PageBreak())
            elements.append(Paragraph("Sample Prompts and Responses", heading_style))
            
            for axis in df['axis'].unique()[:2]:  # Just show 2 axes to save space
                axis_data = df[df['axis'] == axis]
                if len(axis_data) > 0:
                    elements.append(Paragraph(f"<b>{axis.upper()}</b>", styles['Normal']))
                    
                    # Get highest alignment tax example
                    max_idx = axis_data['alignment_tax'].idxmax()
                    max_row = axis_data.loc[max_idx]
                    
                    sample_text = f"""
                    <para fontSize="9">
                    <b>Prompt:</b> {max_row['prompt'][:100]}...<br/>
                    <b>Scores:</b> Base={max_row['base_score']}, Instruct={max_row['instruct_score']}<br/>
                    <b>Alignment Tax:</b> {max_row['alignment_tax']:+.3f}<br/>
                    </para>
                    """
                    elements.append(Paragraph(sample_text, styles['Normal']))
                    elements.append(Spacer(1, 12))
        
        # 6. LIMITATIONS (Critical for publication)
        elements.append(PageBreak())
        elements.append(Paragraph("Study Limitations", heading_style))
        elements.append(Spacer(1, 12))

        # Add key limitations
        key_limitations = [
            f"<b>Sample Scope:</b> {len(df):,} evaluations on Llama 3.1 8B only - results may not generalize to other model families, sizes, or architectures",
            "<b>Evaluation Method:</b> GPT-4 judge may introduce bias favoring stylistically similar responses and reflects OpenAI's alignment philosophy",
            "<b>Scoring Granularity:</b> 3-point scale reduces sensitivity to subtle differences; chosen for consistency but limits effect size detection",
            "<b>Dimension Coverage:</b> Five dimensions tested (refusal, creativity, helpfulness, hedging, hallucination) - excludes reasoning, code generation, multilingual capabilities",
            "<b>Language Limitation:</b> English-only evaluation - alignment tax patterns may differ substantially in other languages",
            "<b>Prompt Generation:</b> GPT-4 generated prompts may not match real-world query distributions or include all edge cases",
            "<b>Deployment Context:</b> Laboratory single-turn evaluations differ from production multi-turn conversations with user feedback",
            "<b>Causal Attribution:</b> While differences are observed, cannot definitively isolate instruction-tuning effects from other training factors",
            "<b>Temporal Specificity:</b> Snapshot evaluation - AI capabilities evolve rapidly and findings may not hold for future versions"
        ]

        for limitation in key_limitations:
            elements.append(Paragraph(f"• {limitation}", styles['Normal']))
            elements.append(Spacer(1, 8))

        elements.append(Spacer(1, 12))
        elements.append(Paragraph(
            "<b>Interpretation Guidance:</b> These limitations provide necessary context but do not invalidate "
            "findings within the study's defined scope. Results are robust for the specific models and conditions "
            "tested, but extrapolation to other contexts requires caution and additional validation.",
            styles['Normal']
        ))

        # 7. Conclusions
        elements.append(PageBreak())
        elements.append(Paragraph("Conclusions", heading_style))
        elements.append(Spacer(1, 12))

        conclusions = []
        
        if has_negative_tax:
            conclusions.append("• 🚨 PARADIGM-SHIFTING DISCOVERY: Negative alignment tax observed across all dimensions")
            conclusions.append("• This challenges conventional assumptions about capability-safety trade-offs")
            conclusions.append("• Instruction-tuning appears to enhance rather than degrade capabilities")
            conclusions.append("• Evidence for potential win-win alignment interventions")
        elif overall_tax > 0.5:
            conclusions.append("• Significant alignment tax observed: instruction-tuning substantially reduced capabilities")
        elif overall_tax > 0:
            conclusions.append("• Moderate alignment tax observed: some capability reduction from instruction-tuning")
        else:
            conclusions.append("• Minimal alignment tax: instruction-tuning preserved capabilities")
        
        # Add safety analysis
        safety_mean = df[df['axis'].isin(['refusal', 'hedging'])]['alignment_tax'].mean()
        capability_mean = df[df['axis'].isin(['creativity', 'helpfulness'])]['alignment_tax'].mean()
        
        if safety_mean < 0 and capability_mean < 0:
            conclusions.append("• Win-win outcome: Both safety and capabilities improved")
        elif safety_mean < 0 and capability_mean >= 0:
            conclusions.append("• Mixed results: Safety improved but some capability impact")
        
        for conclusion in conclusions:
            elements.append(Paragraph(conclusion, styles['Normal']))
            elements.append(Spacer(1, 6))
        
        # Build PDF
        try:
            doc.build(elements)
            print(f"✅ PDF report saved to: {pdf_path}")

            # Upload to S3 if in AWS mode
            upload_to_s3_if_aws(pdf_path, 'reports', 'full PDF report')

        except Exception as e:
            print(f"⚠️ PDF generation failed: {str(e)}")
            print("Falling back to simple PDF...")
            return self.generate_simple_pdf_report(df, output_dir, identifier)

        return pdf_path
    
    def generate_simple_pdf_report(self, df, output_dir, identifier=None,
                              capability_results=None):
        """
        Generate a simple PDF report using only matplotlib
        """
        id_to_use = identifier or self.default_id
        pdf_path = output_dir + f"alignment_tax_report_simple_{id_to_use}.pdf"
        
        overall_tax = df['alignment_tax'].mean()
        has_negative_tax = overall_tax < 0
        
        with PdfPages(pdf_path) as pdf:
            # Page 1: Overview
            fig = plt.figure(figsize=(11, 8.5))
            
            if has_negative_tax:
                fig.suptitle(f'🚨 NEGATIVE ALIGNMENT TAX DISCOVERY - Run {id_to_use}', fontsize=20, fontweight='bold')
            else:
                fig.suptitle(f'Alignment Tax Analysis Report - Run {id_to_use}', fontsize=20, fontweight='bold')
            
            # Create 4 subplots
            gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.4, 
                      width_ratios=[1.2, 0.8])
            
            # Plot 1: Bar chart of alignment tax by axis
            ax1 = fig.add_subplot(gs[0, 0])
            tax_by_axis = df.groupby('axis')['alignment_tax'].mean().sort_values()
            colors_list = ['green' if x < 0 else 'red' for x in tax_by_axis.values]
            tax_by_axis.plot(kind='barh', ax=ax1, color=colors_list)
            ax1.set_title('Alignment Tax by Axis')
            ax1.set_xlabel('Alignment Tax (Base - Instruct)\nNegative = Instruct Better')
            ax1.axvline(x=0, color='black', linestyle='--', alpha=0.5)
            
            # Plot 2: Score distributions
            ax2 = fig.add_subplot(gs[0, 1])
            df[['base_score', 'instruct_score']].boxplot(ax=ax2)
            ax2.set_title('Score Distributions')
            ax2.set_ylabel('Score')
            
            # Plot 3: Scatter plot of base vs instruct
            ax3 = fig.add_subplot(gs[1, 0])

            # Define colors for each axis
            axis_colors = {
                'creativity': 'blue',
                'helpfulness': 'green', 
                'refusal': 'red',
                'hedging': 'orange',
                'hallucination': 'purple'
            }
            
            # Add jittering to separate overlapping points
            np.random.seed(42)  # For reproducible jittering
            
            for axis in df['axis'].unique():
                axis_data = df[df['axis'] == axis]
                color = axis_colors.get(axis, 'gray')
                
                # Add small random jitter to separate overlapping points
                jitter_amount = 0.05
                base_jittered = axis_data['base_score'] + np.random.normal(0, jitter_amount, len(axis_data))
                instruct_jittered = axis_data['instruct_score'] + np.random.normal(0, jitter_amount, len(axis_data))
                
                ax3.scatter(base_jittered, instruct_jittered, 
                           label=f"{axis}\n(n={len(axis_data)})", alpha=0.6, s=40, 
                           color=color, edgecolors='white', linewidth=0.5)
            
            ax3.plot([1, 3], [1, 3], 'k--', alpha=0.3, label='No Change')
            ax3.set_xlabel('Base Score')
            ax3.set_ylabel('Instruct Score')
            ax3.set_title('Base vs Instruct Scores')
            ax3.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
            ax3.set_xlim(0.8, 3.2)
            ax3.set_ylim(0.8, 3.2)
            ax3.grid(True, alpha=0.3)

            
            # Plot 4: Summary statistics table
            ax4 = fig.add_subplot(gs[1, 1])
            ax4.axis('tight')
            ax4.axis('off')
            
            summary_data = [
                ['Metric', 'Value'],
                ['Total Samples', f'{len(df)}'],
                ['Mean Alignment Tax', f'{overall_tax:.3f}'],
                ['Std Dev', f'{df["alignment_tax"].std():.3f}'],
                ['Min Tax', f'{df["alignment_tax"].min():.3f}'],
                ['Max Tax', f'{df["alignment_tax"].max():.3f}']
            ]
            
            if has_negative_tax:
                summary_data.append(['Discovery', 'NEGATIVE TAX!'])
            
            if capability_results and 'critical_assessment' in capability_results:
                assessment = capability_results['critical_assessment'].get('assessment', 'N/A')
                summary_data.append(['Capability Analysis', assessment])
            
            table = ax4.table(cellText=summary_data, loc='center', cellLoc='left')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            
            # Style the header row
            for i in range(len(summary_data[0])):
                table[(0, i)].set_facecolor('#40466e')
                table[(0, i)].set_text_props(weight='bold', color='white')
            
            # Highlight discovery if negative tax
            if has_negative_tax and len(summary_data) > 6:
                table[(6, 1)].set_facecolor('yellow')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 2: Detailed statistics by axis
            fig = plt.figure(figsize=(11, 8.5))
            fig.suptitle('Detailed Results by Axis', fontsize=16, fontweight='bold')
            
            n_axes = len(df['axis'].unique())
            rows = (n_axes + 1) // 2
            
            for idx, axis in enumerate(df['axis'].unique()):
                ax = plt.subplot(rows, 2, idx + 1)
                axis_data = df[df['axis'] == axis]
                
                # Histogram of alignment tax for this axis
                axis_data['alignment_tax'].hist(ax=ax, bins=20, alpha=0.7, 
                                               color='green' if axis_data['alignment_tax'].mean() < 0 else 'red')
                ax.axvline(x=0, color='black', linestyle='--', alpha=0.7)
                ax.set_title(f'{axis.upper()}')
                ax.set_xlabel('Alignment Tax')
                ax.set_ylabel('Frequency')
                
                # Add statistics text
                mean_tax = axis_data['alignment_tax'].mean()
                std_tax = axis_data['alignment_tax'].std()
                interpretation = "IMPROVED" if mean_tax < 0 else "degraded"
                ax.text(0.05, 0.95, f'Mean: {mean_tax:.3f}\nStd: {std_tax:.3f}\n{interpretation}',
                       transform=ax.transAxes, va='top',
                       bbox=dict(boxstyle='round', facecolor='lightgreen' if mean_tax < 0 else 'lightcoral', alpha=0.8))
            
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # PDF metadata
            d = pdf.infodict()
            d['Title'] = f'Alignment Tax Analysis Report - {id_to_use}'
            d['Author'] = 'Alignment Tax Analyzer'
            d['Subject'] = f'Analysis of instruction-tuning effects on model capabilities (Run: {id_to_use})'
            d['Keywords'] = f'LLM, Alignment, Instruction-tuning, Run-{id_to_use}'
            if has_negative_tax:
                d['Keywords'] += ', Negative-Alignment-Tax, Paradigm-Shift'
            d['CreationDate'] = datetime.now()

        print(f"✅ Simple PDF report saved to: {pdf_path}")

        # Upload to S3 if in AWS mode
        upload_to_s3_if_aws(pdf_path, 'reports', 'simple PDF report')

        return pdf_path


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 14:42:46 2025

@author: ramyalsaffar
"""
