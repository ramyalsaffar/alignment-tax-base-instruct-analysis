# Class OutlierHandler
#---------------------
# This class handles:
#   - Detection of outliers and invalid scores
#   - Cleaning of data before analysis
#   - Tracking of excluded data points
#   - Robust statistical calculations
###############################################################################


class OutlierHandler:
    """Enhanced outlier handler with response validation and zero outliers case"""
    
    def __init__(self, valid_range=(1, 3), sentinel_value=EXTREME_VALUE):
        """
        Initialize outlier handler
        
        Args:
            valid_range: Tuple of (min, max) valid scores
            sentinel_value: Value used to mark failed evaluations
        """
        self.valid_min, self.valid_max = valid_range
        self.sentinel_value = sentinel_value
        self.outlier_log = []
        self.statistics = {}
        self.response_validation_results = {}
    
    def validate_responses(self, df: pd.DataFrame) -> Dict:
        """
        Validate response content and cross-check with sentinel scores
        """
        print("\n🔍 RESPONSE VALIDATION ANALYSIS")
        print("=" * 50)
        
        validation_results = {
            'empty_responses': {'base': [], 'instruct': []},
            'error_responses': {'base': [], 'instruct': []},
            'sentinel_mismatches': [],
            'summary': {}
        }
        
        # Check for response columns
        response_columns = {'base': None, 'instruct': None}
        
        # Find response columns (flexible naming)
        for col in df.columns:
            if 'base' in col.lower() and 'response' in col.lower():
                response_columns['base'] = col
            elif 'instruct' in col.lower() and 'response' in col.lower():
                response_columns['instruct'] = col
        
        if not response_columns['base'] or not response_columns['instruct']:
            print("⚠️ Response columns not found.")
            validation_results['summary']['status'] = 'no_response_columns'
            return validation_results
        
        print(f"📁 Found response columns: {response_columns['base']}, {response_columns['instruct']}")
        
        # Quick validation for each model
        total_empty = 0
        total_errors = 0
        total_mismatches = 0
        
        for model_type in ['base', 'instruct']:
            response_col = response_columns[model_type]
            score_col = f'{model_type}_score'
            
            if response_col not in df.columns or score_col not in df.columns:
                continue
            
            # Count empty responses
            empty_count = df[response_col].isna().sum() + (df[response_col] == '').sum()
            total_empty += empty_count
            
            # Count error responses
            error_patterns = [
                            r"\[ERROR: Failed to generate response\]",  # Exact system error message
                            r"^ERROR:",  # Lines starting with ERROR:
                            r"Failed to generate response",  # Exact failure message
                            r"Generation failed"  # Another specific failure message
                        ]
            error_count = 0
            for pattern in error_patterns:
                error_count += df[response_col].str.contains(pattern, case=False, na=False, regex=True).sum()
            total_errors += error_count
            
            # Count mismatches (simplified)
            sentinel_with_valid_response = ((df[score_col] == self.sentinel_value) & 
                                          df[response_col].notna() & 
                                          (df[response_col] != '')).sum()
            total_mismatches += sentinel_with_valid_response
            
            print(f"   {model_type.title()}: {empty_count} empty, {error_count} errors")
        
        # Generate summary
        validation_results['summary'] = {
            'status': 'completed',
            'total_empty_responses': total_empty,
            'total_error_responses': total_errors,
            'total_mismatches': total_mismatches,
            'data_quality': 'excellent' if total_mismatches == 0 else 'good' if total_mismatches < 5 else 'concerning'
        }
        
        print(f"\n📊 VALIDATION SUMMARY:")
        print(f"   Empty responses: {total_empty}")
        print(f"   Error responses: {total_errors}")
        print(f"   Score/response mismatches: {total_mismatches}")
        print(f"   Data quality: {validation_results['summary']['data_quality'].upper()}")
        
        if total_mismatches > 0:
            print(f"\n⚠️ Found {total_mismatches} mismatches (details suppressed for brevity)")
        
        self.response_validation_results = validation_results
        return validation_results
        
        def _remove_outliers(self, df: pd.DataFrame, report: Dict) -> pd.DataFrame:
            """Remove rows with outliers"""
            # Create mask for rows to keep
            keep_mask = pd.Series(True, index=df.index)
            
            for score_col in ['base_score', 'instruct_score']:
                if score_col in df.columns:
                    # Remove sentinel values
                    keep_mask &= df[score_col] != self.sentinel_value
                    # Remove out-of-range values
                    keep_mask &= (df[score_col] >= self.valid_min) & (df[score_col] <= self.valid_max)
            
            df_clean = df[keep_mask].copy()
            report['removal_details'] = {
                'removed_indices': df[~keep_mask].index.tolist(),
                'removed_count': (~keep_mask).sum()
            }
            
            return df_clean
        
        def _cap_outliers(self, df: pd.DataFrame, report: Dict) -> pd.DataFrame:
            """Cap outliers to valid range"""
            df_clean = df.copy()
            modified_count = 0
            
            for score_col in ['base_score', 'instruct_score']:
                if score_col in df.columns:
                    # Handle sentinel values - replace with median
                    sentinel_mask = df_clean[score_col] == self.sentinel_value
                    if sentinel_mask.sum() > 0:
                        valid_scores = df_clean[(df_clean[score_col] != self.sentinel_value) & 
                                               (df_clean[score_col] >= self.valid_min) & 
                                               (df_clean[score_col] <= self.valid_max)][score_col]
                        
                        if len(valid_scores) > 0:
                            median_score = valid_scores.median()
                            df_clean.loc[sentinel_mask, score_col] = median_score
                            modified_count += sentinel_mask.sum()
                    
                    # Cap out-of-range values
                    df_clean.loc[df_clean[score_col] < self.valid_min, score_col] = self.valid_min
                    df_clean.loc[df_clean[score_col] > self.valid_max, score_col] = self.valid_max
            
            report['modified_count'] = modified_count
            return df_clean
    
    def _impute_outliers(self, df: pd.DataFrame, report: Dict) -> pd.DataFrame:
        """Impute outliers using axis-specific medians"""
        df_clean = df.copy()
        modified_count = 0
        
        for axis in df_clean['axis'].unique():
            axis_mask = df_clean['axis'] == axis
            
            for score_col in ['base_score', 'instruct_score']:
                if score_col in df_clean.columns:
                    # Find problematic values in this axis
                    problem_mask = axis_mask & (
                        (df_clean[score_col] == self.sentinel_value) |
                        (df_clean[score_col] < self.valid_min) |
                        (df_clean[score_col] > self.valid_max)
                    )
                    
                    if problem_mask.sum() > 0:
                        # Calculate axis-specific median from valid scores
                        valid_mask = axis_mask & \
                                    (df_clean[score_col] != self.sentinel_value) & \
                                    (df_clean[score_col] >= self.valid_min) & \
                                    (df_clean[score_col] <= self.valid_max)
                        
                        if valid_mask.sum() > 0:
                            axis_median = df_clean[valid_mask][score_col].median()
                            df_clean.loc[problem_mask, score_col] = axis_median
                            modified_count += problem_mask.sum()
                        else:
                            # If no valid scores in axis, use global median
                            global_median = 2  # Middle of 1-3 range
                            df_clean.loc[problem_mask, score_col] = global_median
                            modified_count += problem_mask.sum()
        
        report['modified_count'] = modified_count
        return df_clean
    
    def calculate_robust_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate robust statistics that are less sensitive to outliers
        
        Returns:
            Dictionary of robust statistics
        """
        stats = {}
        
        for col in ['base_score', 'instruct_score', 'alignment_tax']:
            if col in df.columns:
                valid_data = df[
                    (df[col] != self.sentinel_value) & 
                    (df[col].notna())
                ][col]
                
                if len(valid_data) > 0:
                    stats[col] = {
                        'mean': valid_data.mean(),
                        'median': valid_data.median(),
                        'trimmed_mean': scipy.stats.trim_mean(valid_data, 0.1) if len(valid_data) >= 10 else valid_data.mean(),
                        'std': valid_data.std(),
                        'mad': scipy.stats.median_abs_deviation(valid_data),
                        'q1': valid_data.quantile(0.25),
                        'q3': valid_data.quantile(0.75),
                        'valid_count': len(valid_data),
                        'invalid_count': len(df) - len(valid_data)
                    }
        
        return stats
    
    def get_outlier_report(self, df: pd.DataFrame) -> str:
        """
        Generate a formatted report of outliers in the dataset
        
        Returns:
            Formatted string report
        """
        report_lines = []
        report_lines.append("\n" + "="*60)
        report_lines.append("OUTLIER ANALYSIS REPORT")
        report_lines.append("="*60)
        
        # Check for sentinel values
        total_sentinel_issues = 0
        for score_col in ['base_score', 'instruct_score']:
            if score_col in df.columns:
                sentinel_count = (df[score_col] == self.sentinel_value).sum()
                total_sentinel_issues += sentinel_count
                if sentinel_count > 0:
                    percentage = (sentinel_count / len(df)) * 100
                    report_lines.append(f"\n⚠️ {score_col}:")
                    report_lines.append(f"  - Failed evaluations (score={EXTREME_VALUE}): {sentinel_count} ({percentage:.1f}%)")
                    
                    # Show by axis
                    if 'axis' in df.columns:
                        axis_breakdown = df[df[score_col] == self.sentinel_value]['axis'].value_counts()
                        if len(axis_breakdown) > 0:
                            report_lines.append("  - By axis:")
                            for axis, count in axis_breakdown.items():
                                report_lines.append(f"    • {axis}: {count}")
        
        # Check for out-of-range values
        total_oor_issues = 0
        for score_col in ['base_score', 'instruct_score']:
            if score_col in df.columns:
                oor = df[(df[score_col] != self.sentinel_value) & 
                        ((df[score_col] < self.valid_min) | (df[score_col] > self.valid_max))]
                total_oor_issues += len(oor)
                if len(oor) > 0:
                    report_lines.append(f"\n❌ {score_col} out of range:")
                    report_lines.append(f"  - Count: {len(oor)}")
                    report_lines.append(f"  - Values found: {sorted(oor[score_col].unique())}")
        
        # Summary statistics
        report_lines.append("\n" + "-"*40)
        report_lines.append("SUMMARY")
        report_lines.append("-"*40)
        
        # Count affected ROWS
        affected_rows_mask = (
            (df['base_score'] == self.sentinel_value) | 
            (df['instruct_score'] == self.sentinel_value) | 
            (df['base_score'] < self.valid_min) | 
            (df['base_score'] > self.valid_max) | 
            (df['instruct_score'] < self.valid_min) | 
            (df['instruct_score'] > self.valid_max)
        )
        
        affected_rows_count = affected_rows_mask.sum()
        clean_rows_count = len(df) - affected_rows_count
        total_issues = total_sentinel_issues + total_oor_issues
        
        report_lines.append(f"Total problematic scores: {total_issues}")
        report_lines.append(f"Affected rows: {affected_rows_count}")
        report_lines.append(f"Clean rows: {clean_rows_count}")
        report_lines.append(f"Total rows: {len(df)}")
        
        # Enhanced recommendation logic
        if total_issues == 0:
            report_lines.append("\n✅ PERFECT DATA QUALITY:")
            report_lines.append("   No outliers detected. No cleaning required.")
            report_lines.append("   Proceed directly to analysis.")
        elif affected_rows_count < len(df) * 0.025:  # Less than 2.5%
            report_lines.append("\n✅ EXCELLENT DATA QUALITY:")
            report_lines.append("   Minimal outliers (<2.5%). Safe to remove.")
        elif affected_rows_count < len(df) * 0.05:  # Less than 5%
            report_lines.append("\n✅ GOOD DATA QUALITY:")
            report_lines.append("   Minor outliers (<5%). Recommend removal.")
        elif affected_rows_count < len(df) * 0.15:  # Less than 15%
            report_lines.append("\n⚠️ MODERATE DATA QUALITY:")
            report_lines.append("   Moderate outliers (5-15%). Consider imputation.")
        else:
            report_lines.append("\n🚨 CONCERNING DATA QUALITY:")
            report_lines.append("   Significant outliers (>15%). Review evaluation process.")
        
        report_lines.append("="*60 + "\n")
        
        return '\n'.join(report_lines)
    
    
    def clean_dataset(self, df: pd.DataFrame, method='remove') -> Tuple[pd.DataFrame, Dict]:
        """
        Enhanced clean dataset method with zero outliers case
        
        Args:
            df: Original dataframe
            method: 'remove', 'cap', 'impute', or 'none'
        
        Returns:
            (cleaned_df, cleaning_report)
        """
        df_clean = df.copy()
        report = {
            'original_count': len(df),
            'sentinel_values': {},
            'out_of_range': {},
            'statistical_outliers': {},
            'final_count': 0,
            'removed_count': 0,
            'modified_count': 0,
            'method_used': method
        }
        
        # Step 1: Handle sentinel values (EXTREME_VALUE)
        total_sentinel_issues = 0
        for score_col in ['base_score', 'instruct_score']:
            if score_col in df_clean.columns:
                sentinel_mask = df_clean[score_col] == self.sentinel_value
                sentinel_count = sentinel_mask.sum()
                total_sentinel_issues += sentinel_count
                
                if sentinel_count > 0:
                    report['sentinel_values'][score_col] = {
                        'count': sentinel_count,
                        'percentage': (sentinel_count / len(df)) * 100,
                        'indices': df_clean[sentinel_mask].index.tolist()
                    }
                    
                    # Log details about sentinel values
                    for idx in df_clean[sentinel_mask].index:
                        self.outlier_log.append({
                            'index': idx,
                            'type': 'sentinel',
                            'column': score_col,
                            'value': self.sentinel_value,
                            'prompt': df_clean.loc[idx, 'prompt'][:50] if 'prompt' in df_clean.columns else 'N/A'
                        })
        
        # Step 2: Handle out-of-range values (not in 1-3)
        total_oor_issues = 0
        for score_col in ['base_score', 'instruct_score']:
            if score_col in df_clean.columns:
                # Exclude sentinel values from range check
                non_sentinel = df_clean[score_col] != self.sentinel_value
                out_of_range = non_sentinel & ((df_clean[score_col] < self.valid_min) | 
                                              (df_clean[score_col] > self.valid_max))
                oor_count = out_of_range.sum()
                total_oor_issues += oor_count
                
                if oor_count > 0:
                    report['out_of_range'][score_col] = {
                           'count': oor_count,
                           'values': df_clean[out_of_range][score_col].unique().tolist(),
                           'indices': df_clean[out_of_range].index.tolist()
                    }
        
        # Calculate total issues percentage
        total_issues = total_sentinel_issues + total_oor_issues
        issues_percentage = (total_issues / (len(df) * 2)) * 100  # 2 scores per row
        
        # Enhanced method selection logic including zero outliers case
        if total_issues == 0:
            recommended_method = 'none'
            print(f"✅ No outliers detected (0% issues). No cleaning needed.")
        elif issues_percentage < 2.5:  # Very low threshold
            recommended_method = 'remove'
            print(f"✅ Minimal outliers ({issues_percentage:.1f}% issues). Recommended: REMOVE")
        elif issues_percentage < 7.5:  # Low threshold  
            recommended_method = 'remove'
            print(f"⚠️ Low outliers ({issues_percentage:.1f}% issues). Recommended: REMOVE")
        elif issues_percentage < 15:  # Medium threshold
            recommended_method = 'impute'
            print(f"⚠️ Moderate outliers ({issues_percentage:.1f}% issues). Recommended: IMPUTE")
        else:  # High threshold
            recommended_method = 'cap'
            print(f"🚨 High outliers ({issues_percentage:.1f}% issues). Recommended: CAP")
        
        # Override with user's choice or use recommendation
        if method == 'auto':
            method = recommended_method
        
        report['method_used'] = method
        report['recommended_method'] = recommended_method
        
        # Step 3: Apply cleaning method
        if method == 'none' or total_issues == 0:
            # No cleaning needed
            pass
        elif method == 'remove':
            df_clean = self._remove_outliers(df_clean, report)
        elif method == 'cap':
            df_clean = self._cap_outliers(df_clean, report)
        elif method == 'impute':
            df_clean = self._impute_outliers(df_clean, report)
        
        # Step 4: Recalculate alignment tax for modified rows
        if 'base_score' in df_clean.columns and 'instruct_score' in df_clean.columns:
            df_clean['alignment_tax'] = df_clean['base_score'] - df_clean['instruct_score']
        
        # Final statistics
        report['final_count'] = len(df_clean)
        report['removed_count'] = report['original_count'] - report['final_count']
        
        return df_clean, report
    
    
#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 13:03:31 2025

@author: ramyalsaffar
"""
