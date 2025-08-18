# Class AlignmentTaxCapabilityAnalyzer
#------------------------------------
# This class handles:
#   - Intelligent prompt classification by capability content
#   - Capability vs non-capability subset analysis
#   - Domain-specific capability analysis (math, coding, reasoning, etc.)
#   - Statistical comparison between capability types
#   - Visualization of capability patterns
###############################################################################


class AlignmentTaxCapabilityAnalyzer:
    """Specialized analyzer for capability-heavy prompts within alignment tax dataset"""
    
    def __init__(self):
        self.capability_results = {}
        
    # ═══════════════════════════════════════════════════════════════════════════════
    # CAPABILITY SUBSET ANALYSIS (INTEGRATED)
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def analyze_capability_subset(self, df: pd.DataFrame, visualize: bool = True, 
                                 save_results: bool = True, run_id: str = None) -> Dict:
        """
        Perfect method for analyzing capability-heavy prompts within existing dataset
        
        Args:
            df: DataFrame with alignment tax results including 'prompt' column
            visualize: Whether to create visualizations
            save_results: Whether to save detailed results
            run_id: Run identifier for file naming
            
        Returns:
            Dictionary with comprehensive capability subset analysis
        """
        
        print("\n🔍 CAPABILITY SUBSET ANALYSIS")
        print("=" * 60)
        print("Scanning ALL prompts for capability-heavy content...")
        
        # ========================================================================
        # PHASE 1: INTELLIGENT PROMPT CLASSIFICATION
        # ========================================================================
        
        # Execute classification
        print("🏷️ Executing intelligent classification...")
        df_classified = self._classify_prompts_by_capability(df)
        
        # Print classification summary
        category_counts = df_classified['capability_category'].value_counts()
        print(f"\n📈 Classification Results:")
        for category, count in category_counts.items():
            percentage = (count / len(df_classified)) * 100
            print(f"   {category:15} | {count:3d} ({percentage:5.1f}%)")
        
        # ========================================================================
        # PHASE 2: CAPABILITY vs NON-CAPABILITY COMPARISON
        # ========================================================================
        
        print(f"\n🔬 CAPABILITY vs NON-CAPABILITY COMPARISON")
        print("-" * 50)
        
        comparison_results = self._compare_capability_vs_non_capability(df_classified)
        
        # ========================================================================
        # PHASE 3: CRITICAL ASSESSMENT
        # ========================================================================
        
        print(f"\n🎯 CRITICAL ASSESSMENT")
        print("=" * 50)
        
        assessment = self._assess_capability_findings(comparison_results)
        
        # ========================================================================
        # PHASE 4: VISUALIZATION
        # ========================================================================
        
        if visualize:
            print(f"\n🎨 Creating capability subset visualizations...")
            
            # Note: This would need to be added to the visualizer class
            print("   📊 Visualization creation would be handled by AlignmentTaxVisualizer")
            print("   🔗 Integration point: visualizer.create_capability_subset_visualization()")
        
        # Store results
        self.capability_results = {
            'classification_summary': {
                'total_prompts': len(df_classified),
                'category_distribution': category_counts.to_dict(),
                'capability_percentage': (category_counts.get('high_capability', 0) + 
                                        category_counts.get('medium_capability', 0)) / len(df_classified) * 100
            },
            'capability_comparison': comparison_results,
            'critical_assessment': assessment,
            'classified_dataframe': df_classified
        }
        
        # Save detailed results if requested
        if save_results and run_id:
            results_filename = f'capability_subset_results_{run_id}.pkl'
            
            with open(results_path + results_filename, 'wb') as f:
                pickle.dump(self.capability_results, f)
            
            print(f"\n💾 Detailed results saved: {results_filename}")
        
        print(f"\n✅ Capability subset analysis complete!")
        
        return self.capability_results
    
    def _classify_prompts_by_capability(self, df: pd.DataFrame) -> pd.DataFrame:
        """Classify each prompt by capability content and intensity"""
        
        # Enhanced keyword dictionaries with comprehensive coverage
        CAPABILITY_PATTERNS = {
            'math': {
                'keywords': ['calculate', 'equation', 'formula', 'mathematics', 'algebra', 'geometry', 
                           'statistics', 'probability', 'solve', 'compute', 'arithmetic', 'calculus',
                           'derivative', 'integral', 'theorem', 'proof', 'trigonometry', 'logarithm'],
                'patterns': [r'\d+\s*[\+\-\*\/]\s*\d+', r'\b\d+%\b', r'\$\d+', r'\b\d+\.\d+\b',
                           r'x\s*=\s*\d+', r'f\(x\)', r'equation', r'formula']
            },
            'coding': {
                'keywords': ['code', 'program', 'algorithm', 'function', 'python', 'javascript', 'java',
                           'debug', 'syntax', 'implementation', 'programming', 'script', 'variable',
                           'loop', 'array', 'class', 'method', 'API', 'database', 'SQL', 'HTML',
                           'CSS', 'framework', 'library', 'repository', 'git', 'compile'],
                'patterns': [r'def\s+\w+\(', r'function\s+\w+', r'import\s+\w+', r'\.py\b', r'\.js\b',
                           r'console\.log', r'print\(', r'return\s+', r'if\s+.*:', r'for\s+.*:']
            },
            'reasoning': {
                'keywords': ['logic', 'deduce', 'infer', 'analyze', 'conclude', 'reasoning', 'logical',
                           'premise', 'assumption', 'hypothesis', 'evidence', 'argument', 'contradiction',
                           'syllogism', 'inference', 'deduction', 'induction', 'cause', 'effect'],
                'patterns': [r'if.*then', r'because.*therefore', r'given.*conclude', r'assuming.*',
                           r'evidence.*suggests', r'logic.*dictates']
            },
            'technical': {
                'keywords': ['technical', 'engineering', 'scientific', 'specification', 'architecture',
                           'design pattern', 'system', 'protocol', 'network', 'hardware', 'software',
                           'mechanism', 'process', 'methodology', 'analysis', 'optimization'],
                'patterns': [r'how\s+does.*work', r'technical.*details', r'system.*design',
                           r'implement.*', r'optimize.*']
            },
            'science': {
                'keywords': ['physics', 'chemistry', 'biology', 'scientific', 'experiment', 'hypothesis',
                           'theory', 'law', 'principle', 'molecule', 'atom', 'cell', 'DNA', 'evolution',
                           'quantum', 'relativity', 'energy', 'force', 'mass', 'acceleration'],
                'patterns': [r'scientific.*method', r'experiment.*', r'hypothesis.*', r'theory.*']
            }
        }
        
        df_classified = df.copy()
        
        # Initialize classification columns
        df_classified['capability_domains'] = ''
        df_classified['capability_score'] = 0
        df_classified['capability_evidence'] = ''
        df_classified['capability_category'] = 'non_capability'
        
        print(f"\n📊 Classifying {len(df)} prompts...")
        
        for idx, row in df_classified.iterrows():
            prompt_text = str(row['prompt']).lower()
            
            # Track domains and evidence
            domains_found = []
            evidence_list = []
            total_score = 0
            
            # Check each capability domain
            for domain, patterns in CAPABILITY_PATTERNS.items():
                domain_score = 0
                domain_evidence = []
                
                # Keyword matching with weight
                for keyword in patterns['keywords']:
                    if keyword in prompt_text:
                        domain_score += 1
                        domain_evidence.append(f"kw:{keyword}")
                
                # Pattern matching with higher weight
                for pattern in patterns['patterns']:
                    if re.search(pattern, prompt_text, re.IGNORECASE):
                        domain_score += 2  # Patterns weighted higher
                        domain_evidence.append(f"pat:{pattern[:10]}...")
                
                # Record domain if found
                if domain_score > 0:
                    domains_found.append(f"{domain}({domain_score})")
                    evidence_list.extend([f"{domain}:{ev}" for ev in domain_evidence[:2]])  # Limit evidence
                    total_score += domain_score
            
            # Additional heuristics for capability detection
            
            # Problem-solving language
            problem_solving_terms = ['solve', 'calculate', 'determine', 'find', 'compute', 'derive',
                                   'prove', 'demonstrate', 'show that', 'work out', 'figure out']
            for term in problem_solving_terms:
                if term in prompt_text:
                    total_score += 1
                    evidence_list.append(f"problem:{term}")
            
            # Question complexity (multiple steps, technical depth)
            complexity_indicators = ['step by step', 'first.*then', 'explain how', 'walk through',
                                   'break down', 'detail', 'comprehensive', 'thorough']
            for indicator in complexity_indicators:
                if re.search(indicator, prompt_text, re.IGNORECASE):
                    total_score += 0.5
                    evidence_list.append(f"complex:{indicator[:8]}...")
            
            # Store results
            df_classified.at[idx, 'capability_domains'] = '; '.join(domains_found)
            df_classified.at[idx, 'capability_score'] = total_score
            df_classified.at[idx, 'capability_evidence'] = '; '.join(evidence_list[:5])  # Limit evidence length
            
            # Categorize by intensity
            if total_score >= 4:
                df_classified.at[idx, 'capability_category'] = 'high_capability'
            elif total_score >= 2:
                df_classified.at[idx, 'capability_category'] = 'medium_capability'
            elif total_score >= 0.5:
                df_classified.at[idx, 'capability_category'] = 'low_capability'
            else:
                df_classified.at[idx, 'capability_category'] = 'non_capability'
        
        return df_classified
    
    def _compare_capability_vs_non_capability(self, df_classified: pd.DataFrame) -> Dict:
        """Compare capability vs non-capability prompt performance"""
        
        comparison_results = {}
        
        # Define capability vs non-capability groups
        capability_mask = df_classified['capability_category'].isin(['high_capability', 'medium_capability'])
        
        capability_data = df_classified[capability_mask]
        non_capability_data = df_classified[~capability_mask]
        
        print(f"Capability prompts: {len(capability_data)}")
        print(f"Non-capability prompts: {len(non_capability_data)}")
        
        if len(capability_data) >= 5 and len(non_capability_data) >= 5:
            # Statistical comparison
            for group_name, group_data in [('Capability', capability_data), ('Non-Capability', non_capability_data)]:
                mean_tax = group_data['alignment_tax'].mean()
                std_tax = group_data['alignment_tax'].std()
                base_mean = group_data['base_score'].mean()
                instruct_mean = group_data['instruct_score'].mean()
                
                print(f"\n{group_name} Prompts:")
                print(f"   Alignment Tax: {mean_tax:+.3f} ± {std_tax:.3f}")
                print(f"   Base Score: {base_mean:.3f}")
                print(f"   Instruct Score: {instruct_mean:.3f}")
                print(f"   Sample Size: {len(group_data)}")
                
                comparison_results[group_name.lower().replace('-', '_')] = {
                    'count': len(group_data),
                    'mean_tax': mean_tax,
                    'std_tax': std_tax,
                    'base_mean': base_mean,
                    'instruct_mean': instruct_mean
                }
            
            # Statistical test
            try:
                stat, p_value = mannwhitneyu(capability_data['alignment_tax'], 
                                           non_capability_data['alignment_tax'],
                                           alternative='two-sided')
                
                print(f"\n📊 Statistical Test (Mann-Whitney U):")
                print(f"   p-value: {p_value:.4f}")
                print(f"   Significant difference: {'Yes' if p_value < 0.05 else 'No'}")
                
                comparison_results['statistical_test'] = {
                    'test': 'Mann-Whitney U',
                    'statistic': stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                }
                
                # Effect size (Cohen's d approximation)
                pooled_std = np.sqrt((capability_data['alignment_tax'].var() + 
                                    non_capability_data['alignment_tax'].var()) / 2)
                if pooled_std > 0:
                    cohens_d = (capability_data['alignment_tax'].mean() - 
                               non_capability_data['alignment_tax'].mean()) / pooled_std
                    print(f"   Effect size (Cohen's d): {cohens_d:.3f}")
                    comparison_results['statistical_test']['cohens_d'] = cohens_d
                
            except Exception as e:
                print(f"   Statistical test failed: {e}")
        
        return comparison_results
    
    def _assess_capability_findings(self, comparison_results: Dict) -> Dict:
        """Assess the implications of capability analysis findings"""
        
        assessment = {}
        
        if comparison_results:
            cap_tax = comparison_results['capability']['mean_tax']
            non_cap_tax = comparison_results['non_capability']['mean_tax']
            
            if cap_tax > 0 > non_cap_tax:
                assessment_result = "SUPPORTS TRADITIONAL THEORY"
                explanation = "Capability prompts show positive tax (worse performance), non-capability show improvement"
            elif cap_tax > non_cap_tax and cap_tax > 0:
                assessment_result = "PARTIALLY SUPPORTS TRADITIONAL THEORY"  
                explanation = "Capability prompts show higher alignment tax than non-capability prompts"
            elif cap_tax < 0 and non_cap_tax < 0:
                assessment_result = "CHALLENGES TRADITIONAL THEORY"
                explanation = "Both capability and non-capability prompts show improvement"
            else:
                assessment_result = "MIXED/UNCLEAR PATTERN"
                explanation = "Results don't clearly support or refute traditional alignment tax theory"
            
            print(f"Assessment: {assessment_result}")
            print(f"Explanation: {explanation}")
            
            assessment = {
                'assessment': assessment_result,
                'explanation': explanation,
                'capability_tax': cap_tax,
                'non_capability_tax': non_cap_tax,
                'supports_traditional_theory': 'SUPPORTS' in assessment_result
            }
        
        return assessment
    
    def get_capability_breakdown_by_domain(self, df_classified: pd.DataFrame) -> Dict:
        """Get detailed breakdown of capability domains found in prompts"""
        
        domain_breakdown = {}
        
        # Extract individual domains from the domain strings
        all_domains = []
        for domains_str in df_classified['capability_domains']:
            if domains_str:
                # Parse domain(score) format
                domains = domains_str.split('; ')
                for domain in domains:
                    if '(' in domain:
                        domain_name = domain.split('(')[0]
                        all_domains.append(domain_name)
        
        # Count domain frequencies
        from collections import Counter
        domain_counts = Counter(all_domains)
        
        print(f"\n📊 CAPABILITY DOMAIN BREAKDOWN:")
        for domain, count in domain_counts.most_common():
            percentage = (count / len(df_classified)) * 100
            print(f"   {domain:12} | {count:3d} prompts ({percentage:5.1f}%)")
        
        return dict(domain_counts)


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 15:04:58 2025

@author: ramyalsaffar
"""
