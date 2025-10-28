# Class AlignmentTaxStatisticalAnalyzer
#-------------------------------------
# This class handles:
#   - Comprehensive statistical testing
#   - Hypothesis testing (t-tests, Wilcoxon)
#   - Effect size calculations
#   - Confidence intervals
#   - Power analysis
#   - Normality testing
###############################################################################


class AlignmentTaxStatisticalAnalyzer:
    """Enhanced statistical analyzer with rigorous validation for negative alignment tax findings"""
    
    def __init__(self):
        self.statistical_results = {}
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # ENHANCED STATISTICAL ANALYSIS METHODS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def comprehensive_statistical_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Enhanced statistical analysis with rigorous validation
        
        Args:
            df: DataFrame with alignment tax results
            
        Returns:
            Dictionary with comprehensive statistical results
        """
        print("\n🔬 COMPREHENSIVE STATISTICAL ANALYSIS")
        print("=" * 50)
        
        statistical_results = {}
        
        for axis in df['axis'].unique():
            print(f"\n📊 Analyzing {axis.upper()}...")
            result = self._analyze_single_axis(df, axis)
            statistical_results[axis] = result
            
            if 'error' in result:
                print(f"   ❌ {result['error']}")
                continue
            
            # Print key findings
            self._print_axis_statistical_summary(axis, result)
        
        # Store results
        self.statistical_results = statistical_results
        
        # Generate overall summary
        self._print_overall_statistical_summary(statistical_results)
        
        return statistical_results
    
    def _analyze_single_axis(self, df: pd.DataFrame, axis: str) -> Dict:
        """Comprehensive statistical analysis for a single axis"""
        axis_data = df[df['axis'] == axis].copy()
        
        # Remove failed evaluations
        valid_data = axis_data[
            (axis_data['base_score'] != EXTREME_VALUE) &
            (axis_data['instruct_score'] != EXTREME_VALUE) &
            (axis_data['base_score'].between(1, 3)) &
            (axis_data['instruct_score'].between(1, 3))
        ]
        
        if len(valid_data) < 5:
            return {'error': f'Insufficient data for {axis} (n={len(valid_data)})'}
        
        base_scores = valid_data['base_score'].values
        instruct_scores = valid_data['instruct_score'].values
        differences = valid_data['alignment_tax'].values
        
        return {
            'axis': axis,
            'n': len(valid_data),
            'descriptive': self._descriptive_stats(base_scores, instruct_scores, differences),
            'normality': self._test_normality(differences),
            'hypothesis_test': self._paired_hypothesis_test(base_scores, instruct_scores),
            'effect_size': self._calculate_effect_sizes(base_scores, instruct_scores, differences),
            'confidence_intervals': self._confidence_intervals(differences),
            'power_analysis': self._post_hoc_power_analysis(differences),
            'practical_significance': self._assess_practical_significance(differences, axis)
        }
    
    def _descriptive_stats(self, base_scores: np.ndarray, instruct_scores: np.ndarray, 
                          differences: np.ndarray) -> Dict:
        """Calculate comprehensive descriptive statistics"""
        return {
            'base': {
                'mean': np.mean(base_scores),
                'std': np.std(base_scores, ddof=1),
                'median': np.median(base_scores),
                'iqr': np.percentile(base_scores, 75) - np.percentile(base_scores, 25)
            },
            'instruct': {
                'mean': np.mean(instruct_scores),
                'std': np.std(instruct_scores, ddof=1),
                'median': np.median(instruct_scores),
                'iqr': np.percentile(instruct_scores, 75) - np.percentile(instruct_scores, 25)
            },
            'difference': {
                'mean': np.mean(differences),
                'std': np.std(differences, ddof=1),
                'median': np.median(differences),
                'iqr': np.percentile(differences, 75) - np.percentile(differences, 25),
                'skewness': scipy.stats.skew(differences),
                'kurtosis': scipy.stats.kurtosis(differences)
            }
        }
    
    def _test_normality(self, differences: np.ndarray) -> Dict:
        """Test normality assumptions"""
        shapiro_stat, shapiro_p = scipy.stats.shapiro(differences)
        
        return {
            'shapiro_wilk': {
                'statistic': shapiro_stat,
                'p_value': shapiro_p,
                'is_normal': shapiro_p > 0.05
            },
            'sample_size_adequate': len(differences) >= 30
        }
    
    def _paired_hypothesis_test(self, base_scores: np.ndarray, 
                               instruct_scores: np.ndarray) -> Dict:
        """Perform appropriate paired hypothesis test"""
        differences = base_scores - instruct_scores
        
        # Test normality to choose test
        _, normal_p = scipy.stats.shapiro(differences)
        is_normal = normal_p > 0.05
        
        if is_normal or len(differences) >= 30:
            # Paired t-test
            t_stat, t_p = scipy.stats.ttest_rel(base_scores, instruct_scores)
            test_name = "Paired t-test"
            statistic = t_stat
            p_value = t_p
        else:
            # Wilcoxon signed-rank test
            w_stat, w_p = scipy.stats.wilcoxon(base_scores, instruct_scores)
            test_name = "Wilcoxon signed-rank"
            statistic = w_stat
            p_value = w_p
        
        return {
            'test_name': test_name,
            'statistic': statistic,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'direction': 'instruct_better' if np.mean(differences) > 0 else 'base_better',
            'assumptions_met': is_normal or len(differences) >= 30
        }
    
    def _calculate_effect_sizes(self, base_scores: np.ndarray, instruct_scores: np.ndarray,
                               differences: np.ndarray) -> Dict:
        """Calculate multiple effect size measures"""
        
        # Cohen's d (standardized mean difference)
        pooled_std = np.sqrt((np.var(base_scores, ddof=1) + np.var(instruct_scores, ddof=1)) / 2)
        cohens_d = np.mean(differences) / pooled_std if pooled_std > 0 else 0
        
        # Hedges' g (bias-corrected Cohen's d)
        n = len(differences)
        hedges_g = cohens_d * (1 - (3 / (4 * n - 9))) if n > 9 else cohens_d
        
        # Glass's delta (using base model as control group)
        glass_delta = np.mean(differences) / np.std(base_scores, ddof=1) if np.std(base_scores, ddof=1) > 0 else 0
        
        return {
            'cohens_d': cohens_d,
            'hedges_g': hedges_g,
            'glass_delta': glass_delta,
            'interpretation': self._interpret_effect_size(abs(cohens_d))
        }
    
    def _interpret_effect_size(self, effect_size: float) -> str:
        """Interpret effect size magnitude"""
        if effect_size < 0.2:
            return "negligible"
        elif effect_size < 0.5:
            return "small"
        elif effect_size < 0.8:
            return "medium"
        else:
            return "large"
    
    def _confidence_intervals(self, differences: np.ndarray) -> Dict:
        """Calculate confidence intervals"""
        n = len(differences)
        mean_diff = np.mean(differences)
        std_diff = np.std(differences, ddof=1)
        se = std_diff / np.sqrt(n)
        
        # 95% CI using t-distribution
        t_critical = scipy.stats.t.ppf(0.975, df=n-1)
        margin_error = t_critical * se
        
        ci_95 = {
            'lower': mean_diff - margin_error,
            'upper': mean_diff + margin_error,
            'margin_error': margin_error
        }
        
        # 99% CI
        t_critical_99 = scipy.stats.t.ppf(0.995, df=n-1)
        margin_error_99 = t_critical_99 * se
        
        ci_99 = {
            'lower': mean_diff - margin_error_99,
            'upper': mean_diff + margin_error_99,
            'margin_error': margin_error_99
        }
        
        return {
            '95_percent': ci_95,
            '99_percent': ci_99,
            'interpretation': self._interpret_ci(ci_95, mean_diff)
        }
    
    def _interpret_ci(self, ci: Dict, mean_diff: float) -> str:
        """Interpret confidence interval"""
        if ci['lower'] > 0:
            return "Significantly favors base model"
        elif ci['upper'] < 0:
            return "Significantly favors instruct model"
        else:
            return "No significant difference (CI includes 0)"
    
    def _post_hoc_power_analysis(self, differences: np.ndarray) -> Dict:
        """Post-hoc statistical power analysis"""
        try:
            from statsmodels.stats.power import TTestPower
            
            n = len(differences)
            effect_size = abs(np.mean(differences) / np.std(differences, ddof=1))
            
            # Calculate achieved power
            power_analysis = TTestPower()
            achieved_power = power_analysis.solve_power(
                effect_size=effect_size,
                nobs=n,
                alpha=0.05,
                power=None
            )
            
            # Calculate required sample size for 80% power
            required_n = power_analysis.solve_power(
                effect_size=effect_size,
                nobs=None,
                alpha=0.05,
                power=0.8
            )
            
            return {
                'achieved_power': achieved_power,
                'required_n_for_80_power': required_n,
                'current_n': n,
                'adequately_powered': achieved_power >= 0.8
            }
        except ImportError:
            # Fallback if statsmodels not available
            return {
                'achieved_power': None,
                'required_n_for_80_power': None,
                'current_n': len(differences),
                'adequately_powered': None,
                'note': 'Power analysis requires statsmodels package'
            }
    
    def _assess_practical_significance(self, differences: np.ndarray, axis: str) -> Dict:
        """Assess practical significance of the findings"""
        mean_diff = np.mean(differences)
        
        # Convert to percentage of scale (1-3 range = 2 points total)
        percentage_change = abs(mean_diff) / 2 * 100
        
        # Determine practical significance thresholds
        if percentage_change < 5:
            magnitude = "minimal"
        elif percentage_change < 15:
            magnitude = "moderate"
        elif percentage_change < 25:
            magnitude = "substantial"
        else:
            magnitude = "large"
        
        return {
            'percentage_change': percentage_change,
            'magnitude': magnitude,
            'practically_significant': percentage_change >= 10,  # 10% threshold
            'direction': 'improvement' if mean_diff < 0 else 'degradation'
        }
    
    def _print_axis_statistical_summary(self, axis: str, result: Dict):
        """Print statistical summary for a single axis"""
        desc = result['descriptive']['difference']
        hyp = result['hypothesis_test']
        effect = result['effect_size']
        ci = result['confidence_intervals']['95_percent']
        practical = result['practical_significance']
        
        significance = "***" if hyp['p_value'] < 0.001 else "**" if hyp['p_value'] < 0.01 else "*" if hyp['p_value'] < 0.05 else "ns"
        
        print(f"   📈 Mean difference: {desc['mean']:+.3f} ± {desc['std']:.3f}")
        print(f"   🔍 {hyp['test_name']}: p = {hyp['p_value']:.4f} {significance}")
        print(f"   📏 Effect size (Cohen's d): {effect['cohens_d']:.3f} ({effect['interpretation']})")
        print(f"   🎯 95% CI: [{ci['lower']:+.3f}, {ci['upper']:+.3f}]")
        print(f"   💡 {practical['percentage_change']:.1f}% {practical['direction']} ({practical['magnitude']})")
    
    def _print_overall_statistical_summary(self, statistical_results: Dict):
        """Print overall statistical summary"""
        print(f"\n📋 OVERALL STATISTICAL SUMMARY")
        print("-" * 40)
        
        # Count significant results
        significant_axes = [axis for axis, result in statistical_results.items() 
                           if 'error' not in result and result['hypothesis_test']['significant']]
        
        improvement_axes = [axis for axis, result in statistical_results.items() 
                           if 'error' not in result and result['descriptive']['difference']['mean'] < 0]
        
        total_axes = len([axis for axis, result in statistical_results.items() if 'error' not in result])
        
        print(f"📊 Statistically significant: {len(significant_axes)}/{total_axes} axes")
        print(f"✅ Showing improvement: {len(improvement_axes)}/{total_axes} axes")
        
        if len(improvement_axes) == total_axes:
            print(f"🚨 UNIVERSAL IMPROVEMENT: All axes show negative alignment tax!")
        elif len(improvement_axes) >= total_axes * 0.8:
            print(f"🎯 WIDESPREAD IMPROVEMENT: Most axes show negative alignment tax")
        
        if significant_axes:
            print(f"🔬 Significant improvements: {', '.join(significant_axes)}")


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 15:04:58 2025

@author: ramyalsaffar
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 15:31:59 2025

@author: ramyalsaffar
"""
