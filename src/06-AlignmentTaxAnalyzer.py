# Class AlignmentTaxAnalyzer
#---------------------------
# This class handles:
#   - Core descriptive analysis
#   - Coordination with visualizer and reporter
#   - Basic statistical summaries
#   - Percentage calculations and interpretations
###############################################################################


class AlignmentTaxAnalyzer:
    """Core analyzer for descriptive analysis and coordination with other components"""
    
    def __init__(self, run_id=None):
        self.run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.visualizer = AlignmentTaxVisualizer(default_id=self.run_id)
        self.reporter = AlignmentTaxReporter(default_id=self.run_id)
        
    def set_run_id(self, run_id):
        """Set or update the run identifier"""
        self.run_id = run_id
        self.visualizer.default_id = run_id
        self.reporter.default_id = run_id
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # DESCRIPTIVE ANALYSIS METHODS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def descriptive_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Comprehensive descriptive analysis of alignment tax data
        
        Args:
            df: DataFrame with alignment tax results
            
        Returns:
            Dictionary with descriptive statistics
        """
        print("📊 DESCRIPTIVE ANALYSIS")
        print("=" * 40)
        
        results = {
            'overall_stats': self._calculate_overall_stats(df),
            'axis_breakdown': self._calculate_axis_breakdown(df),
            'score_distributions': self._analyze_score_distributions(df),
            'approach_analysis': self._analyze_by_approach(df)
        }
        
        # Print key findings
        overall = results['overall_stats']
        print(f"\n🎯 KEY DESCRIPTIVE FINDINGS:")
        print(f"   • Total evaluations: {overall['n_total']:,}")
        print(f"   • Mean alignment tax: {overall['mean_tax']:+.3f}")
        print(f"   • Standard deviation: {overall['std_tax']:.3f}")
        print(f"   • Negative tax axes: {overall['negative_tax_count']}/{overall['total_axes']}")
        
        if overall['mean_tax'] < 0:
            print(f"   🚨 NEGATIVE ALIGNMENT TAX DETECTED!")
            print(f"      This challenges conventional alignment tax theory!")
        
        return results
    
    def _calculate_overall_stats(self, df: pd.DataFrame) -> Dict:
        """Calculate overall descriptive statistics"""
        valid_data = df[df['alignment_tax'] != EXTREME_VALUE]
        
        axis_means = df.groupby('axis')['alignment_tax'].mean()
        negative_count = sum(1 for mean in axis_means if mean < 0)
        
        return {
            'n_total': len(valid_data),
            'mean_tax': valid_data['alignment_tax'].mean(),
            'median_tax': valid_data['alignment_tax'].median(),
            'std_tax': valid_data['alignment_tax'].std(),
            'min_tax': valid_data['alignment_tax'].min(),
            'max_tax': valid_data['alignment_tax'].max(),
            'q1_tax': valid_data['alignment_tax'].quantile(0.25),
            'q3_tax': valid_data['alignment_tax'].quantile(0.75),
            'negative_tax_count': negative_count,
            'total_axes': len(df['axis'].unique()),
            'axes': list(df['axis'].unique())
        }
    
    def _calculate_axis_breakdown(self, df: pd.DataFrame) -> Dict:
        """Calculate statistics by axis"""
        axis_stats = {}
        
        for axis in df['axis'].unique():
            axis_data = df[df['axis'] == axis]
            valid_data = axis_data[axis_data['alignment_tax'] != EXTREME_VALUE]
            
            if len(valid_data) > 0:
                # Calculate percentage improvement (1-3 scale = 2 point range)
                mean_tax = valid_data['alignment_tax'].mean()
                pct_change = abs(mean_tax) / 2 * 100
                
                axis_stats[axis] = {
                    'n': len(valid_data),
                    'base_mean': valid_data['base_score'].mean(),
                    'instruct_mean': valid_data['instruct_score'].mean(),
                    'tax_mean': mean_tax,
                    'tax_std': valid_data['alignment_tax'].std(),
                    'tax_median': valid_data['alignment_tax'].median(),
                    'percentage_change': pct_change,
                    'direction': 'improvement' if mean_tax < 0 else 'degradation',
                    'interpretation': self._interpret_axis_result(axis, mean_tax)
                }
            
        return axis_stats
    
    def _interpret_axis_result(self, axis: str, mean_tax: float) -> str:
        """Interpret alignment tax result for specific axis"""
        pct = abs(mean_tax) / 2 * 100
        
        if axis in ['creativity', 'helpfulness']:
            if mean_tax < 0:
                return f"✅ {pct:.1f}% capability improvement"
            else:
                return f"❌ {pct:.1f}% capability reduction"
        elif axis in ['refusal', 'hedging']:
            if mean_tax < 0:
                return f"✅ {pct:.1f}% safety improvement"
            else:
                return f"❌ {pct:.1f}% safety reduction"
        else:  # hallucination
            if mean_tax < 0:
                return f"✅ {pct:.1f}% accuracy improvement"
            else:
                return f"❌ {pct:.1f}% accuracy reduction"
    
    def _analyze_score_distributions(self, df: pd.DataFrame) -> Dict:
        """Analyze score distributions"""
        distributions = {}
        
        for model in ['base', 'instruct']:
            score_col = f'{model}_score'
            valid_scores = df[df[score_col] != EXTREME_VALUE][score_col]
            
            if len(valid_scores) > 0:
                dist = valid_scores.value_counts(normalize=True).sort_index()
                distributions[model] = {
                    'mean': valid_scores.mean(),
                    'std': valid_scores.std(),
                    'distribution': dist.to_dict(),
                    'entropy': -sum(dist * np.log(dist + 1e-10))  # Shannon entropy
                }
        
        return distributions
    
    def _analyze_by_approach(self, df: pd.DataFrame) -> Dict:
        """Analyze results by approach within each axis"""
        approach_stats = {}
        
        if 'approach' not in df.columns:
            return approach_stats
            
        for axis in df['axis'].unique():
            axis_data = df[df['axis'] == axis]
            approach_stats[axis] = {}
            
            for approach in axis_data['approach'].unique():
                approach_data = axis_data[axis_data['approach'] == approach]
                valid_data = approach_data[approach_data['alignment_tax'] != EXTREME_VALUE]
                
                if len(valid_data) > 0:
                    approach_stats[axis][approach] = {
                        'n': len(valid_data),
                        'tax_mean': valid_data['alignment_tax'].mean(),
                        'tax_std': valid_data['alignment_tax'].std()
                    }
        
        return approach_stats
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PERCENTAGE CALCULATION METHODS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def calculate_alignment_tax_percent(self, df):
        """Calculate alignment tax percentage for each axis"""
        df = df.copy()
        df['alignment_tax_percent'] = 0.0
        df['alignment_interpretation'] = ''
    
        for idx, row in df.iterrows():
            base_score = row['base_score']
            instruct_score = row['instruct_score']
            axis = row['axis']
        
            # Handle division by zero and sentinel values
            if base_score == 0 or pd.isna(base_score) or base_score == EXTREME_VALUE:
                alignment_tax_percent = 0
            else:
                # Correct formula - matches alignment tax direction
                alignment_tax_percent = (base_score - instruct_score) / base_score * 100
        
            df.at[idx, 'alignment_tax_percent'] = alignment_tax_percent
            df.at[idx, 'alignment_interpretation'] = self._interpret_alignment_tax(alignment_tax_percent, axis)
    
        return df

    def _interpret_alignment_tax(self, percent, axis):
        """Enhanced interpretation of alignment tax percentage"""
        if abs(percent) < 5:
            magnitude = "Negligible"
        elif abs(percent) < 15:
            magnitude = "Moderate"
        else:
            magnitude = "Significant"
    
        positive_axes = ['creativity', 'helpfulness']
        safety_axes = ['refusal', 'hedging', 'hallucination']
    
        if axis in positive_axes:
            if percent > 0:
                direction = f"capability loss ({percent:.1f}%)"
            else:
                direction = f"capability gain ({abs(percent):.1f}%)"
        elif axis in safety_axes:
            if percent > 0:
                direction = f"safety reduction ({percent:.1f}%)"
            else:
                direction = f"safety improvement ({abs(percent):.1f}%)"
    
        return f"{magnitude} {direction}"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # DELEGATION METHODS TO OTHER COMPONENTS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def create_visualizations(self, df, identifier=None):
        """Delegate to visualizer's create_visualizations"""
        return self.visualizer.create_visualizations(df, identifier)
    
    def generate_pdf_report(self, df, output_dir=None, **kwargs):
        """Delegate to reporter's generate_pdf_report"""
        if output_dir is None:
            output_dir = results_path
        return self.reporter.generate_pdf_report(df, output_dir, **kwargs)
    
    def create_pareto_frontier(self, df, use_robust_stats=True, pre_cleaned=False, 
                              cleaning_method='remove', identifier=None):
        """Delegate to visualizer's create_pareto_frontier"""
        return self.visualizer.create_pareto_frontier(
            df, use_robust_stats, pre_cleaned, cleaning_method, identifier
        )
    
    def generate_text_report(self, df, output_dir=None, **kwargs):
        """Delegate to reporter's generate_text_report"""
        if output_dir is None:
            output_dir = results_path
        if 'identifier' not in kwargs:
            kwargs['identifier'] = self.run_id
        return self.reporter.generate_text_report(df, output_dir, **kwargs)
    
    def generate_simple_pdf_report(self, df, output_dir=None, identifier=None):
        """Delegate to reporter's generate_simple_pdf_report"""
        if output_dir is None:
            output_dir = results_path
        id_to_use = identifier or self.run_id
        return self.reporter.generate_simple_pdf_report(df, output_dir, id_to_use)
    
    def generate_professional_executive_summary(self, df, output_dir=None, identifier=None):
        """Delegate to reporter's generate_professional_executive_summary"""
        if output_dir is None:
            output_dir = results_path
        id_to_use = identifier or self.run_id
        return self.reporter.generate_professional_executive_summary(df, output_dir, id_to_use)


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:15:56 2025

@author: ramyalsaffar
"""
