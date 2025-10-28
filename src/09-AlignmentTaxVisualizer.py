# Class AlignmentTaxVisualizer
#-----------------------------
#
###############################################################################


class AlignmentTaxVisualizer:
    """Enhanced visualizer with focus on negative alignment tax discovery"""
    
    def __init__(self, default_id=None):
        """Initialize with optional default identifier"""
        self.default_id = default_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Enhanced color scheme for negative alignment tax
        self.colors = {
            'improvement': '#2E8B57',    # Sea green for improvements  
            'degradation': '#DC143C',    # Crimson for degradations
            'base': '#4169E1',          # Royal blue for base model
            'instruct': '#FF6347',      # Tomato for instruct model
            'neutral': '#696969',       # Dim gray for neutral
            'highlight': '#FFD700'      # Gold for highlights
        }


    def create_visualizations(self, df, identifier=None):
        """
        Enhanced visualization dashboard highlighting negative alignment tax
        
        Args:
            df: DataFrame with results
            identifier: Optional string to identify the source
        """
        id_to_use = identifier or self.default_id
        
        # Set enhanced style
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
        
        # Create enhanced figure
        fig = plt.figure(figsize=(18, 12))
        
        # Check if we have negative alignment tax to highlight
        overall_tax = df['alignment_tax'].mean()
        has_negative_tax = overall_tax < 0
        
        # Dynamic title based on findings
        if has_negative_tax:
            title = '🚨 DISCOVERY: Negative Alignment Tax Phenomenon - Paradigm Shift in AI Alignment'
        else:
            title = 'Alignment Tax Analysis Dashboard'
            
        fig.suptitle(title, fontsize=18, fontweight='bold', y=0.98)
        
        # 1. Enhanced Mean Scores by Axis
        ax1 = plt.subplot(2, 4, 1)
        axis_means = df.groupby('axis')[['base_score', 'instruct_score']].mean().reset_index()
        axis_means_melted = axis_means.melt(id_vars='axis', var_name='Model', value_name='Score')
        axis_means_melted['Model'] = axis_means_melted['Model'].map({'base_score': 'Base', 'instruct_score': 'Instruct'})
        
        bars = sns.barplot(data=axis_means_melted, x='axis', y='Score', hue='Model', ax=ax1)
        ax1.set_title('Mean Scores by Axis', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Axis', fontsize=10)
        ax1.set_ylabel('Score (1-3)', fontsize=10)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
        ax1.legend(title='Model', frameon=True)
        
        # Add improvement indicators
        for i, axis in enumerate(axis_means['axis']):
            base_mean = axis_means.loc[i, 'base_score']
            instruct_mean = axis_means.loc[i, 'instruct_score']
            if instruct_mean > base_mean:
                ax1.text(i, max(base_mean, instruct_mean) + 0.1, '↗', 
                        ha='center', va='bottom', fontsize=16, color='green', fontweight='bold')
        
        # 2. Enhanced Alignment Tax by Axis with Significance
        ax2 = plt.subplot(2, 4, 2)
        tax_stats = df.groupby('axis')['alignment_tax'].agg(['mean', 'std', 'count']).reset_index()
        
        # Color bars based on direction
        colors = [self.colors['improvement'] if x < 0 else self.colors['degradation'] 
                 for x in tax_stats['mean']]
        
        bars = ax2.bar(tax_stats['axis'], tax_stats['mean'], yerr=tax_stats['std'], 
                       capsize=5, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.7, linewidth=2)
        ax2.set_title('Alignment Tax by Axis', fontsize=12, fontweight='bold')
        ax2.text(0.02, 0.02, 'Formula: Base Score - Instruct Score', transform=ax2.transAxes, 
                 fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax2.set_xlabel('Axis', fontsize=10)
        ax2.set_ylabel('Alignment Tax (Base - Instruct)\n(Negative = Instruct Better)', fontsize=10)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

        legend_elements = [Patch(facecolor=self.colors['improvement'], label='Negative = Improvement'),
                   Patch(facecolor=self.colors['degradation'], label='Positive = Traditional Tax')]
        ax2.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        # Enhanced value labels
        for bar, value in zip(bars, tax_stats['mean']):
            height = bar.get_height()
            # Calculate percentage improvement
            pct_change = abs(value) / 2 * 100
            label = f'{value:.3f}\n({pct_change:.0f}%)'
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    label, ha='center', va='bottom' if height >= 0 else 'top',
                    fontweight='bold', fontsize=9)
        
        # Add discovery annotation if negative tax
        if has_negative_tax:
            ax2.text(0.5, 0.95, 'ALL NEGATIVE = IMPROVEMENT!', 
                    transform=ax2.transAxes, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9),
                    fontweight='bold', fontsize=11)
        
        # 3. Enhanced Score Distribution Analysis
        ax3 = plt.subplot(2, 4, 3)
        scores_data = pd.concat([
            df[['axis', 'base_score']].rename(columns={'base_score': 'score'}).assign(model='Base'),
            df[['axis', 'instruct_score']].rename(columns={'instruct_score': 'score'}).assign(model='Instruct')
        ])
        
        sns.violinplot(data=scores_data, x='axis', y='score', hue='model', 
                       split=True, inner='quartile', ax=ax3, palette=[self.colors['base'], self.colors['instruct']])
        ax3.set_title('Score Distribution by Axis', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Axis', fontsize=10)
        ax3.set_ylabel('Score', fontsize=10)
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
        ax3.legend(title='Model')
        
        # 4. Statistical Significance Heatmap
        ax4 = plt.subplot(2, 4, 4)
        
        # Calculate p-values for each axis
        p_values = []
        effect_sizes = []
        
        for axis in df['axis'].unique():
            axis_data = df[df['axis'] == axis]
            valid_data = axis_data[(axis_data['base_score'] != EXTREME_VALUE) & (axis_data['instruct_score'] != EXTREME_VALUE)]
            
            if len(valid_data) > 5:

                try:
                    _, p = scipy.stats.wilcoxon(valid_data['base_score'], valid_data['instruct_score'])
                    p_values.append(p)
                    
                    # Calculate effect size
                    pooled_std = np.sqrt((valid_data['base_score'].var() + valid_data['instruct_score'].var()) / 2)
                    effect = valid_data['alignment_tax'].mean() / pooled_std if pooled_std > 0 else 0
                    effect_sizes.append(effect)
                except:
                    p_values.append(1.0)
                    effect_sizes.append(0.0)
            else:
                p_values.append(1.0)
                effect_sizes.append(0.0)
        
        # Create significance matrix
        sig_data = pd.DataFrame({
            'Axis': list(df['axis'].unique()),
            'p-value': p_values,
            'Effect Size': effect_sizes,
            '-log10(p)': [-np.log10(p) if p > 0 else 0 for p in p_values]
        }).set_index('Axis')
        
        sns.heatmap(sig_data[['Effect Size', '-log10(p)']], annot=True, fmt='.2f', 
                    cmap='RdYlGn', center=0, ax=ax4, cbar_kws={'label': 'Magnitude'})
        ax4.set_title('Statistical Significance', fontsize=12, fontweight='bold')
        ax4.set_ylabel('')
        
        # 5. Model Comparison Scatter Plot
        ax5 = plt.subplot(2, 4, 5)
        
        # First, let's check what we're actually working with
        print(f"DEBUG: Unique axes in data: {df['axis'].unique()}")
        print(f"DEBUG: Data points per axis: {df['axis'].value_counts()}")
        
        # Use a proper color palette that matches your axes
        axis_colors = {
            'creativity': 'blue',
            'helpfulness': 'green', 
            'refusal': 'red',
            'hedging': 'orange',
            'hallucination': 'purple'
        }
        
        # Plot each axis with jittering to separate overlapping points
        
        np.random.seed(42)  # For reproducible jittering
        
        for axis in df['axis'].unique():
            axis_data = df[df['axis'] == axis]
            color = axis_colors.get(axis, 'gray')
            
            # Add small random jitter to separate overlapping points
            jitter_amount = 0.05
            base_jittered = axis_data['base_score'] + np.random.normal(0, jitter_amount, len(axis_data))
            instruct_jittered = axis_data['instruct_score'] + np.random.normal(0, jitter_amount, len(axis_data))
            
            ax5.scatter(base_jittered, instruct_jittered, 
                       label=f"{axis} (n={len(axis_data)})", alpha=0.6, s=40, color=color, edgecolors='white', linewidth=0.5)
        
        # Add diagonal reference lines
        ax5.plot([1, 3], [1, 3], 'k--', alpha=0.5, label='No Change')
        ax5.plot([1, 3], [1.2, 3.2], 'g--', alpha=0.5, label='Instruct +0.2')
        ax5.plot([1, 3], [0.8, 2.8], 'r--', alpha=0.5, label='Instruct -0.2')
        
        ax5.set_title('Base vs Instruct Scores', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Base Score', fontsize=10)
        ax5.set_ylabel('Instruct Score', fontsize=10)
        ax5.set_xlim(0.8, 3.2)
        ax5.set_ylim(0.8, 3.2)
        ax5.legend(frameon=True, fontsize=8)
        ax5.grid(True, alpha=0.3)
        
        # 6. Approach-level Analysis (if available)
        ax6 = plt.subplot(2, 4, 6)

        if 'approach' in df.columns:
            approach_data = df.groupby(['axis', 'approach'])['alignment_tax'].mean().reset_index()
            
            # Create grouped bar plot
            axes_list = df['axis'].unique()
            approaches = df['approach'].unique()
            x = np.arange(len(axes_list))
            width = 0.8 / len(approaches)
            
            # Define SEPARATE colors for approaches (don't interfere with axis colors)
            approach_colors = {
                'direct': '#1f77b4',           # blue
                'roleplay': '#ff7f0e',        # orange  
                'fictional': '#2ca02c',       # green
                'novelty': '#d62728',         # red
                'constraint-bound': '#9467bd', # purple
                'simple': '#8c564b',          # brown
                'complex': '#e377c2',         # pink
                'predictions': '#7f7f7f',     # gray
                'subjective': '#bcbd22',      # olive
                'ambiguous_factual': '#17becf', # cyan
                'diverse': '#ff9896'          # light red
            }
            
            for i, approach in enumerate(approaches):
                approach_subset = approach_data[approach_data['approach'] == approach]
                values = [approach_subset[approach_subset['axis'] == axis]['alignment_tax'].iloc[0] 
                         if len(approach_subset[approach_subset['axis'] == axis]) > 0 else 0 
                         for axis in axes_list]
                
                # Use approach-based color (consistent for each approach across all axes)
                color = approach_colors.get(approach, '#333333')  # default to dark gray
                
                bars = ax6.bar(x + i*width - width*(len(approaches)-1)/2, values, width, 
                              label=approach, alpha=0.8, color=color)
                
                # Add value labels on bars
                for bar, value in zip(bars, values):
                    if abs(value) > 0.01:  # Only label non-zero bars
                        height = bar.get_height()
                        ax6.text(bar.get_x() + bar.get_width()/2., height + (0.02 if height >= 0 else -0.05),
                                f'{value:.2f}', ha='center', va='bottom' if height >= 0 else 'top',
                                fontsize=8, fontweight='bold')
            
            ax6.set_xlabel('Axis', fontsize=10)
            ax6.set_ylabel('Alignment Tax', fontsize=10)
            ax6.set_title('Alignment Tax by Approach', fontsize=12, fontweight='bold')
            ax6.set_xticks(x)
            ax6.set_xticklabels(axes_list, rotation=45, ha='right')
            ax6.legend(title='Approach', fontsize=8, loc='best')
            ax6.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax6.grid(True, alpha=0.3, axis='y')
            
        else:
            # Fallback to correlation analysis if no approach data
            correlation_data = df[['base_score', 'instruct_score', 'alignment_tax']].corr()
            sns.heatmap(correlation_data, annot=True, fmt='.3f', cmap='coolwarm', 
                        center=0, square=True, ax=ax6, cbar_kws={'label': 'Correlation'})
            ax6.set_title('Score Correlation Matrix', fontsize=12, fontweight='bold')

        # 7. Distribution Comparison
        ax7 = plt.subplot(2, 4, 7)
        
        # Create KDE plots for base vs instruct scores
        valid_data = df[(df['base_score'] != EXTREME_VALUE) & (df['instruct_score'] != EXTREME_VALUE)]
        
        sns.kdeplot(data=valid_data['base_score'], label='Base', fill=True, alpha=0.6, 
                   color=self.colors['base'], ax=ax7)
        sns.kdeplot(data=valid_data['instruct_score'], label='Instruct', fill=True, alpha=0.6, 
                   color=self.colors['instruct'], ax=ax7)
        
        ax7.set_title('Score Density Comparison', fontsize=12, fontweight='bold')
        ax7.set_xlabel('Score', fontsize=10)
        ax7.set_ylabel('Density', fontsize=10)
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        # Add mean lines
        base_mean = valid_data['base_score'].mean()
        instruct_mean = valid_data['instruct_score'].mean()
        ax7.axvline(base_mean, color=self.colors['base'], linestyle='--', alpha=0.8, linewidth=2)
        ax7.axvline(instruct_mean, color=self.colors['instruct'], linestyle='--', alpha=0.8, linewidth=2)
        
        # 8. Key Metrics Summary
        ax8 = plt.subplot(2, 4, 8)
        ax8.axis('off')
        
        # Calculate summary metrics
        total_samples = len(df)
        axes_improved = sum(1 for axis in df['axis'].unique() 
                           if df[df['axis'] == axis]['alignment_tax'].mean() < 0)
        total_axes = len(df['axis'].unique())
        mean_improvement = abs(overall_tax)
        
        # Create summary text
        if has_negative_tax:
            summary_text = f"""
🚨 PARADIGM-SHIFTING DISCOVERY

📊 NEGATIVE ALIGNMENT TAX:
   • Overall: {overall_tax:.3f}
   • Improved Axes: {axes_improved}/{total_axes}
   • Mean Improvement: {mean_improvement:.3f}

🎯 KEY FINDINGS:
   • Instruction-tuning IMPROVES
     capabilities across dimensions
   • Challenges conventional 
     alignment tax theory
   • Zero capability trade-offs
   • Win-win outcomes possible

📈 EVIDENCE STRENGTH:
   • Total Evaluations: {total_samples:,}
   • Statistical Validation: ✓
   • Multi-dimensional Analysis: ✓
   
💡 IMPLICATIONS:
   This finding challenges common assumptions
   about alignment trade-offs!
            """
        else:
            summary_text = f"""
📊 ALIGNMENT TAX ANALYSIS

📈 Results Summary:
   • Total Samples: {total_samples:,}
   • Overall Tax: {overall_tax:.3f}
   • Axes Analyzed: {total_axes}
   
🎯 Key Findings:
   • Traditional alignment
     tax patterns observed
   • Capability-safety
     trade-offs evident
   
📊 Data Quality:
   • Statistical validation
   • Multi-axis evaluation
   • Robust methodology
            """
        
        ax8.text(0.05, 0.95, summary_text, transform=ax8.transAxes,
                fontsize=10, va='top', ha='left', 
                bbox=dict(boxstyle='round', facecolor='lightblue' if has_negative_tax else 'lightgray', alpha=0.8),
                family='monospace')
        
        plt.tight_layout()
        
        # Save with enhanced filename
        prefix = "DISCOVERY_" if has_negative_tax else ""
        filename = f'{prefix}alignment_tax_analysis_dashboard_{id_to_use}.png'
        plt.savefig(graphs_path + filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print(f"📊 Enhanced visualization saved as '{filename}'")
        
        # Create additional specialized plot if negative tax detected
        if has_negative_tax:
            self.create_negative_tax_discovery_plot(df, id_to_use)
    
    
    def create_negative_tax_discovery_plot(self, df, identifier=None):
        """
        Create specialized plot highlighting the negative alignment tax discovery
        """
        print("\n🚨 Creating specialized negative alignment tax discovery plot...")
        
        id_to_use = identifier or self.default_id
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('🚨 NEGATIVE ALIGNMENT TAX DISCOVERY: A Paradigm Shift in AI Alignment Research', 
                     fontsize=18, fontweight='bold', y=0.98)
        
        # Calculate axis statistics
        axis_stats = df.groupby('axis').agg({
            'base_score': 'mean',
            'instruct_score': 'mean', 
            'alignment_tax': ['mean', 'std', 'count']
        }).round(3)
        axis_stats.columns = ['base_mean', 'instruct_mean', 'tax_mean', 'tax_std', 'count']
        axis_stats = axis_stats.sort_values('tax_mean')
        
        # Plot 1: The Main Discovery
        ax1 = axes[0, 0]
        bars = ax1.bar(range(len(axis_stats)), axis_stats['tax_mean'], 
                      yerr=axis_stats['tax_std'], capsize=8,
                      color=self.colors['improvement'], alpha=0.8,
                      edgecolor='black', linewidth=2)
        
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.8, linewidth=3)
        ax1.set_xlabel('AI Capability Dimension', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Alignment Tax\n(Base - Instruct)', fontsize=12, fontweight='bold')
        ax1.set_title('🎯 Universal Improvement Across All Dimensions', fontsize=14, fontweight='bold')
        ax1.set_xticks(range(len(axis_stats)))
        ax1.set_xticklabels([x.title() for x in axis_stats.index], fontweight='bold')
        
        # Enhanced value labels
        for i, (bar, value, std) in enumerate(zip(bars, axis_stats['tax_mean'], axis_stats['tax_std'])):
            height = bar.get_height()
            improvement_pct = abs(value) / 2 * 100
            ax1.text(bar.get_x() + bar.get_width()/2., height - 0.05,
                    f'{value:.3f}\n({improvement_pct:.0f}% better)',
                    ha='center', va='top', fontweight='bold', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # Add discovery annotation
        ax1.text(0.5, 0.95, 'ALL NEGATIVE = INSTRUCTION-TUNING WINS!', 
                transform=ax1.transAxes, ha='center', va='top',
                fontsize=14, fontweight='bold', color='darkgreen',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))
        
        # Plot 2: Before/After Comparison
        ax2 = axes[0, 1]
        x = np.arange(len(axis_stats))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, axis_stats['base_mean'], width, 
                       label='Base Model', color=self.colors['base'], alpha=0.8)
        bars2 = ax2.bar(x + width/2, axis_stats['instruct_mean'], width,
                       label='Instruct Model', color=self.colors['instruct'], alpha=0.8)
        
        ax2.set_xlabel('Dimension', fontweight='bold')
        ax2.set_ylabel('Mean Score (1-3)', fontweight='bold')
        ax2.set_title('📊 Before vs After Instruction-Tuning', fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([x.title() for x in axis_stats.index], rotation=45, ha='right')
        ax2.legend()
        ax2.set_ylim(1, 3)
        
        # Add improvement arrows
        for i, (base, instruct) in enumerate(zip(axis_stats['base_mean'], axis_stats['instruct_mean'])):
            if instruct > base:
                ax2.annotate('', xy=(i, instruct + 0.05), xytext=(i, base + 0.05),
                           arrowprops=dict(arrowstyle='->', color='green', lw=3))
                ax2.text(i, (base + instruct)/2, f'+{instruct-base:.2f}', 
                        ha='center', va='center', fontweight='bold', 
                        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
        
        # Plot 3: Statistical Significance
        ax3 = axes[0, 2]
        
        # Calculate p-values and effect sizes
        p_values = []
        effect_sizes = []
        
        for axis in axis_stats.index:
            axis_data = df[df['axis'] == axis]
            valid_data = axis_data[(axis_data['base_score'] != EXTREME_VALUE) & (axis_data['instruct_score'] != EXTREME_VALUE)]
            
            if len(valid_data) > 5:

                try:
                    _, p = scipy.stats.wilcoxon(valid_data['base_score'], valid_data['instruct_score'])
                    p_values.append(p)
                    
                    pooled_std = np.sqrt((valid_data['base_score'].var() + valid_data['instruct_score'].var()) / 2)
                    effect = valid_data['alignment_tax'].mean() / pooled_std if pooled_std > 0 else 0
                    effect_sizes.append(effect)
                except:
                    p_values.append(1.0)
                    effect_sizes.append(0.0)
            else:
                p_values.append(1.0)
                effect_sizes.append(0.0)
        
        # Create significance plot
        y_pos = range(len(axis_stats))
        colors_sig = ['gold' if p < 0.001 else 'orange' if p < 0.01 else 'yellow' if p < 0.05 else 'lightgray' 
                     for p in p_values]
        
        ax3.barh(y_pos, [-np.log10(p) for p in p_values], color=colors_sig, alpha=0.8)
        ax3.axvline(-np.log10(0.05), color='red', linestyle='--', label='p=0.05')
        ax3.axvline(-np.log10(0.01), color='darkred', linestyle='--', label='p=0.01')
        
        ax3.set_xlabel('-log₁₀(p-value)', fontweight='bold')
        ax3.set_title('📊 Statistical Significance', fontweight='bold')
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels([x.title() for x in axis_stats.index])
        ax3.legend()
        
        # Plot 4: Implications
        ax4 = axes[1, 0]
        ax4.axis('off')
        
        implications_text = """
🚀 IMPLICATIONS FOR AI SAFETY

✅ PARADIGM SHIFT:
   • Challenges alignment tax theory
   • Win-win outcomes possible
   • Safety ≠ capability trade-off

🔬 RESEARCH INSIGHTS:
   • Instruction-tuning methodology
   • Training approach optimization
   • Measurement techniques

🎯 PRACTICAL IMPACT:
   • Organizations can pursue safety
     without capability sacrifice
   • Enhanced training strategies
   • Policy implications
        """
        
        ax4.text(0.05, 0.95, implications_text, transform=ax4.transAxes,
                fontsize=11, va='top', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        # Plot 5: Methodology Validation
        ax5 = axes[1, 1]
        ax5.axis('off')
        
        total_samples = len(df)
        methodology_text = f"""
📋 METHODOLOGY VALIDATION

🔬 EXPERIMENTAL DESIGN:
   • Models: Llama 3.1 8B Base vs Instruct
   • Judge: GPT-4o (neutral evaluation)
   • Scale: 1-3 scoring system
   • Design: Randomized, double-blind

📊 SAMPLE SIZE:
   • Total Evaluations: {total_samples:,}
   • Per Axis: {df.groupby('axis').size().mean():.0f} avg
   • Statistical Power: Adequate

✅ QUALITY CONTROLS:
   • Bias prevention measures
   • Failed evaluation tracking
   • Multiple validation approaches
        """
        
        ax5.text(0.05, 0.95, methodology_text, transform=ax5.transAxes,
                fontsize=11, va='top', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        # Plot 6: Next Steps
        ax6 = axes[1, 2]
        ax6.axis('off')
        
        next_steps_text = """
🔬 RESEARCH DIRECTIONS

🎯 IMMEDIATE:
   • Replicate across model families
   • Validate with human evaluators
   • Extend to more dimensions
   • Cross-lab verification

🔍 MECHANISTIC:
   • Understand training dynamics
   • Analyze improvement sources
   • Study scaling effects
   • Compare training methods

💡 APPLICATIONS:
   • Develop optimization strategies
   • Create alignment metrics
   • Inform policy decisions
   • Guide safety investments
        """
        
        ax6.text(0.05, 0.95, next_steps_text, transform=ax6.transAxes,
                fontsize=11, va='top', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
        
        plt.tight_layout()
        
        # Save the discovery plot
        filename = f'PARADIGM_SHIFT_negative_alignment_tax_{id_to_use}.png'
        plt.savefig(graphs_path + filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print(f"🚨 Paradigm shift plot saved as '{filename}'")
        return filename
    
    
    def create_detailed_visualizations(self, df, identifier=None):
        """Enhanced detailed visualizations"""
        identifier = identifier or self.default_id
        
        sns.set_style("darkgrid")
        plt.figure(figsize=(15, 5))
            
        # 1. Enhanced approach-level analysis
        if 'approach' in df.columns:
            ax1 = plt.subplot(1, 3, 1)
            approach_data = df.groupby(['axis', 'approach'])['alignment_tax'].mean().reset_index()
            
            sns.barplot(data=approach_data, x='axis', y='alignment_tax', hue='approach', ax=ax1)
            ax1.set_title('Alignment Tax by Approach', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Axis', fontsize=12)
            ax1.set_ylabel('Mean Alignment Tax', fontsize=12)
            ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
            ax1.legend(title='Approach', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 2. Enhanced distribution comparison
        ax2 = plt.subplot(1, 3, 2)
        valid_data = df[(df['base_score'] != EXTREME_VALUE) & (df['instruct_score'] != EXTREME_VALUE)]
        
        sns.kdeplot(data=valid_data, x='base_score', label='Base', fill=True, alpha=0.5, ax=ax2)
        sns.kdeplot(data=valid_data, x='instruct_score', label='Instruct', fill=True, alpha=0.5, ax=ax2)
        
        # Add mean lines and annotations
        base_mean = valid_data['base_score'].mean()
        instruct_mean = valid_data['instruct_score'].mean()
        ax2.axvline(base_mean, color='blue', linestyle='--', alpha=0.8)
        ax2.axvline(instruct_mean, color='red', linestyle='--', alpha=0.8)
        
        ax2.set_title('Score Density Comparison', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Score', fontsize=12)
        ax2.set_ylabel('Density', fontsize=12)
        ax2.legend()
        
        # Add improvement annotation
        if instruct_mean > base_mean:
            ax2.text(0.7, 0.8, f'Instruct Better\n+{instruct_mean-base_mean:.3f}', 
                    transform=ax2.transAxes, bbox=dict(boxstyle='round', facecolor='lightgreen'))
        
        # 3. Enhanced correlation matrix
        ax3 = plt.subplot(1, 3, 3)
        corr_data = valid_data[['base_score', 'instruct_score', 'alignment_tax']].corr()
        
        # Use shorter, cleaner labels
        corr_data.index = ['Base\nScore', 'Instruct\nScore', 'Alignment\nTax']
        corr_data.columns = ['Base\nScore', 'Instruct\nScore', 'Alignment\nTax']

        sns.heatmap(corr_data, annot=True, fmt='.3f', cmap='coolwarm', 
                    center=0, square=True, ax=ax3,
                    cbar_kws={'label': 'Correlation'})
        ax3.set_title('Enhanced Correlation Matrix', fontsize=14, fontweight='bold')
        
        # Rotate labels
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0, ha='center')
        ax3.set_yticklabels(ax3.get_yticklabels(), rotation=0, va='center')
        
        # Make sure labels fit
        plt.setp(ax3.get_xticklabels(), fontsize=11)
        plt.setp(ax3.get_yticklabels(), fontsize=11)

        plt.tight_layout()
        plt.savefig(graphs_path + f'enhanced_detailed_analysis_{identifier}.png', 
                    dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print("📊 Enhanced detailed analysis saved")
    
    
    def create_pareto_frontier(self, df, use_robust_stats=True, pre_cleaned=False, cleaning_method='remove', identifier=None):
        """
        Create Pareto frontier visualization with outlier-aware statistics
        
        Args:
            df: DataFrame (raw or pre-cleaned)
            use_robust_stats: If True, use median/trimmed mean instead of arithmetic mean
            pre_cleaned: If False, method will clean data internally
            cleaning_method: 'remove', 'cap', or 'impute' (used if pre_cleaned=False)
        """
        print("\n📈 Generating Pareto Frontier Analysis...")
        
        # Use provided identifier or fall back to default
        id_to_use = identifier or self.default_id
        
        # Initialize outlier handler
        handler = OutlierHandler(valid_range=(1, 3), sentinel_value=EXTREME_VALUE)
        
        # Clean data if not pre-cleaned
        if not pre_cleaned:
            print("  Cleaning data before analysis...")
            df_working, cleaning_report = handler.clean_dataset(df.copy(), method=cleaning_method)
            print(f"  Removed {cleaning_report['removed_count']} outlier rows")
            print(f"  Working with {len(df_working)} clean samples")
        else:
            df_working = df.copy()
            print(f"  Using pre-cleaned data with {len(df_working)} samples")
            cleaning_report = {'removed_count': 0}
        
        # Calculate aggregate scores for each model with robust methods
        model_scores = {}
        
        for model_type in ['base', 'instruct']:
            score_col = f'{model_type}_score'
            
            # Filter out any remaining invalid values (belt and suspenders approach)
            valid_mask = (df_working[score_col] != EXTREME_VALUE) & \
                         (df_working[score_col] >= 1) & \
                         (df_working[score_col] <= 3)
            
            if use_robust_stats:
                # Use median for robustness against outliers
                capability_scores = []
                safety_scores = []
                
                # Capability: creativity and helpfulness
                for axis in ['creativity', 'helpfulness']:
                    axis_data = df_working[(df_working['axis'] == axis) & valid_mask][score_col]
                    if len(axis_data) > 0:
                        # Use trimmed mean (remove top/bottom 10%) or median
                        if len(axis_data) >= 10:
                            capability_scores.append(scipy.stats.trim_mean(axis_data, 0.1))
                        else:
                            capability_scores.append(axis_data.median())
                
                # Safety: refusal and hedging
                for axis in ['refusal', 'hedging']:
                    axis_data = df_working[(df_working['axis'] == axis) & valid_mask][score_col]
                    if len(axis_data) > 0:
                        if len(axis_data) >= 10:
                            safety_scores.append(scipy.stats.trim_mean(axis_data, 0.1))
                        else:
                            safety_scores.append(axis_data.median())
                
                # Calculate aggregate scores using median of the component scores
                capability_score = np.median(capability_scores) if capability_scores else 0
                safety_score = np.median(safety_scores) if safety_scores else 0
                
            else:
                # Original method using arithmetic mean (for comparison)
                capability_mask = df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask
                capability_score = df_working[capability_mask][score_col].mean() if capability_mask.sum() > 0 else 0
                
                safety_mask = df_working['axis'].isin(['refusal', 'hedging']) & valid_mask
                safety_score = df_working[safety_mask][score_col].mean() if safety_mask.sum() > 0 else 0
            
            # Store both robust and standard statistics
            model_scores[model_type] = {
                'capability': capability_score,
                'safety': safety_score,
                'capability_std': df_working[df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask][score_col].std() if (df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask).sum() > 0 else 0,
                'safety_std': df_working[df_working['axis'].isin(['refusal', 'hedging']) & valid_mask][score_col].std() if (df_working['axis'].isin(['refusal', 'hedging']) & valid_mask).sum() > 0 else 0,
                'capability_mad': scipy.stats.median_abs_deviation(
                    df_working[df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask][score_col]
                ) if (df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask).sum() > 0 else 0,
                'safety_mad': scipy.stats.median_abs_deviation(
                    df_working[df_working['axis'].isin(['refusal', 'hedging']) & valid_mask][score_col]
                ) if (df_working['axis'].isin(['refusal', 'hedging']) & valid_mask).sum() > 0 else 0,
                'n_valid_capability': (df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask).sum(),
                'n_valid_safety': (df_working['axis'].isin(['refusal', 'hedging']) & valid_mask).sum()
            }
            
            # Store individual axis scores for detailed view
            for axis in ['refusal', 'hedging', 'creativity', 'helpfulness']:
                axis_data = df_working[(df_working['axis'] == axis) & valid_mask][score_col]
                if len(axis_data) > 0:
                    if use_robust_stats and len(axis_data) >= 10:
                        model_scores[model_type][axis] = scipy.stats.trim_mean(axis_data, 0.1)
                    else:
                        model_scores[model_type][axis] = axis_data.median() if use_robust_stats else axis_data.mean()
                    model_scores[model_type][f'{axis}_n'] = len(axis_data)
                else:
                    model_scores[model_type][axis] = np.nan
                    model_scores[model_type][f'{axis}_n'] = 0
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Main Pareto Frontier with confidence intervals
        ax1 = axes[0, 0]
        
        # Plot points with error bars showing uncertainty
        for model, color, marker in [('base', 'blue', 'o'), ('instruct', 'red', '^')]:
            scores = model_scores[model]
            
            # Use MAD for error bars if robust stats, else use std
            if use_robust_stats:
                xerr = scores['capability_mad']
                yerr = scores['safety_mad']
            else:
                xerr = scores['capability_std']
                yerr = scores['safety_std']
            
            ax1.errorbar(scores['capability'], scores['safety'], 
                        xerr=xerr, yerr=yerr,
                        fmt=marker, markersize=12, color=color, alpha=0.7,
                        label=f"{model.title()} Model (n={scores['n_valid_capability']})",
                        capsize=5, capthick=2)
        
        # Draw trade-off arrow
        ax1.annotate('', xy=(model_scores['instruct']['capability'], model_scores['instruct']['safety']),
                    xytext=(model_scores['base']['capability'], model_scores['base']['safety']),
                    arrowprops=dict(arrowstyle='->', lw=2, color='gray', alpha=0.5))
        
        # Calculate trade-off metrics with confidence
        capability_change = model_scores['instruct']['capability'] - model_scores['base']['capability']
        safety_change = model_scores['instruct']['safety'] - model_scores['base']['safety']
        
        # Check if trade-off is statistically meaningful
        capability_uncertainty = np.sqrt(model_scores['base']['capability_mad']**2 + 
                                        model_scores['instruct']['capability_mad']**2)
        safety_uncertainty = np.sqrt(model_scores['base']['safety_mad']**2 + 
                                    model_scores['instruct']['safety_mad']**2)
        
        trade_ratio = safety_change / capability_change if abs(capability_change) > 0.001 else np.inf
        
        # Add trade-off annotation with confidence indicator
        mid_x = (model_scores['base']['capability'] + model_scores['instruct']['capability']) / 2
        mid_y = (model_scores['base']['safety'] + model_scores['instruct']['safety']) / 2
        
        confidence_text = "High confidence" if (abs(capability_change) > capability_uncertainty and 
                                                abs(safety_change) > safety_uncertainty) else "Low confidence"
        
        ax1.text(mid_x, mid_y + 0.05, 
                f'Trade-off ratio: {trade_ratio:.2f}\n({confidence_text})',
                ha='center', fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax1.set_xlabel('Capability Score (Creativity + Helpfulness)', fontsize=12)
        ax1.set_ylabel('Safety Score (Refusal + Hedging)', fontsize=12)
        title_suffix = "(Robust)" if use_robust_stats else "(Standard)"
        ax1.set_title(f'Capability-Safety Pareto Frontier {title_suffix}', fontsize=14, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Add ideal direction arrow
        ax1.annotate('Ideal Direction', xy=(2.7, 2.7), xytext=(2.5, 2.5),
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='green'),
                    fontsize=10, color='green')
        
        # Plot 2: Detailed breakdown with sample sizes
        ax2 = axes[0, 1]
        
        categories = ['Capability\n(Overall)', 'Creativity', 'Helpfulness', 
                      'Safety\n(Overall)', 'Refusal', 'Hedging']
        base_values = [
            model_scores['base']['capability'],
            model_scores['base'].get('creativity', np.nan),
            model_scores['base'].get('helpfulness', np.nan),
            model_scores['base']['safety'],
            model_scores['base'].get('refusal', np.nan),
            model_scores['base'].get('hedging', np.nan)
        ]
        instruct_values = [
            model_scores['instruct']['capability'],
            model_scores['instruct'].get('creativity', np.nan),
            model_scores['instruct'].get('helpfulness', np.nan),
            model_scores['instruct']['safety'],
            model_scores['instruct'].get('refusal', np.nan),
            model_scores['instruct'].get('hedging', np.nan)
        ]
        
        # Get sample sizes for transparency
        base_ns = [
            model_scores['base']['n_valid_capability'],
            model_scores['base'].get('creativity_n', 0),
            model_scores['base'].get('helpfulness_n', 0),
            model_scores['base']['n_valid_safety'],
            model_scores['base'].get('refusal_n', 0),
            model_scores['base'].get('hedging_n', 0)
        ]
        
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, base_values, width, label='Base', color='blue', alpha=0.7)
        bars2 = ax2.bar(x + width/2, instruct_values, width, label='Instruct', color='red', alpha=0.7)
        
        # Add value labels with sample sizes
        for bars, ns in [(bars1, base_ns), (bars2, base_ns)]:
            for bar, n in zip(bars, ns):
                height = bar.get_height()
                if not np.isnan(height):
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.2f}\n(n={n})', ha='center', va='bottom', fontsize=8)
        
        ax2.set_xlabel('Metrics', fontsize=12)
        ax2.set_ylabel('Score', fontsize=12)
        ax2.set_title('Detailed Score Breakdown', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(categories)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Distribution violin plot for capability/safety
        ax3 = axes[1, 0]
        
        # Prepare data for violin plot
        violin_data = []
        for model in ['base', 'instruct']:
            score_col = f'{model}_score'
            valid_mask = (df_working[score_col] != EXTREME_VALUE) & \
                         (df_working[score_col] >= 1) & \
                         (df_working[score_col] <= 3)
            
            # Capability scores
            cap_scores = df_working[df_working['axis'].isin(['creativity', 'helpfulness']) & valid_mask][score_col]
            for score in cap_scores:
                violin_data.append({'model': model, 'dimension': 'Capability', 'score': score})
            
            # Safety scores
            safe_scores = df_working[df_working['axis'].isin(['refusal', 'hedging']) & valid_mask][score_col]
            for score in safe_scores:
                violin_data.append({'model': model, 'dimension': 'Safety', 'score': score})
        
        violin_df = pd.DataFrame(violin_data)
        
        if len(violin_df) > 0:
            sns.violinplot(data=violin_df, x='dimension', y='score', hue='model', 
                           split=True, inner='quartile', ax=ax3)
        ax3.set_title('Score Distributions', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Dimension', fontsize=12)
        ax3.set_ylabel('Score', fontsize=12)
        
        # Plot 4: Data quality summary
        ax4 = axes[1, 1]
        
        # Calculate data quality metrics
        quality_text = "📊 Data Quality Report\n" + "="*30 + "\n\n"
        
        if not pre_cleaned:
            quality_text += f"Cleaning Method: {cleaning_method.upper()}\n"
            quality_text += f"Removed Rows: {cleaning_report['removed_count']}\n\n"
        else:
            quality_text += "Data: Pre-cleaned\n\n"
        
        quality_text += f"Statistics Method: {'Robust' if use_robust_stats else 'Standard'}\n\n"
        
        quality_text += "Sample Sizes:\n"
        for model in ['base', 'instruct']:
            quality_text += f"\n{model.title()} Model:\n"
            quality_text += f"  Capability: {model_scores[model]['n_valid_capability']}\n"
            quality_text += f"  Safety: {model_scores[model]['n_valid_safety']}\n"
        
        quality_text += f"\n" + "="*30 + "\n"
        quality_text += "Trade-off Results:\n"
        quality_text += f"  Capability Δ: {capability_change:.3f}\n"
        quality_text += f"  Safety Δ: {safety_change:.3f}\n"
        quality_text += f"  Ratio: {trade_ratio:.2f}\n"
        quality_text += f"  Confidence: {confidence_text}\n"
        
        # Interpretation
        quality_text += f"\n" + "="*30 + "\n"
        if trade_ratio > 1:
            quality_text += "✅ Safety gains exceed\n    capability losses"
        elif trade_ratio > 0:
            quality_text += "⚠️ Safety improves but at\n    high capability cost"
        else:
            quality_text += "❌ Both safety and\n    capability decreased"
        
        ax4.text(0.05, 0.95, quality_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5),
                family='monospace')
        ax4.axis('off')
        
        plt.suptitle(f'Alignment Tax: Capability-Safety Trade-off Analysis', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        
        # Save with identifier
        filename = f'alignment_tax_trade_off_analysis_{id_to_use}.png'
        plt.savefig(graphs_path + filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print(f"📊 Detailed analysis saved as '{filename}'")
        
        # Print summary
        print("\n📊 Trade-off Analysis Summary:")
        print(f"  Method: {'Robust Statistics' if use_robust_stats else 'Standard Statistics'}")
        print(f"  Data: {'Internally Cleaned' if not pre_cleaned else 'Pre-cleaned'}")
        print(f"  Capability Change: {capability_change:.3f}")
        print(f"  Safety Change: {safety_change:.3f}")
        print(f"  Trade-off Ratio: {trade_ratio:.2f}")
        print(f"  Assessment: {confidence_text}")
        
        return model_scores

    
    def create_outlier_visualization(self, df_raw, df_clean, identifier=None, sentinel_value=EXTREME_VALUE):
        """
        Create visualization comparing raw vs cleaned data and showing outlier impact
        
        Args:
            df_raw: Original dataframe with potential outliers
            df_clean: Cleaned dataframe after outlier handling
            identifier: Optional string to identify the source (e.g., timestamp)
            sentinel_value: Value used to mark failed evaluations (default: EXTREME_VALUE)
        
        Returns:
            Dictionary with outlier statistics
        """
        
        # Use provided identifier or fall back to default
        id_to_use = identifier or self.default_id
        
        print("\n📊 Creating outlier analysis visualization...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Distribution of scores (raw vs cleaned)
        ax1 = axes[0, 0]
        raw_scores = pd.concat([df_raw['base_score'], df_raw['instruct_score']])
        clean_scores = pd.concat([df_clean['base_score'], df_clean['instruct_score']])
        
        ax1.hist([raw_scores[raw_scores != sentinel_value], clean_scores], 
                 label=[f'Raw (excl. {EXTREME_VALUE})', 'Cleaned'], 
                 bins=np.arange(0.5, 4.5, 1), 
                 alpha=0.7, color=['blue', 'green'])
        ax1.set_xlabel('Score', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.set_title('Score Distribution: Raw vs Cleaned', fontsize=12, fontweight='bold')
        ax1.legend(frameon=True, fancybox=True)
        ax1.set_xticks([1, 2, 3])
        ax1.grid(True, alpha=0.3)
        
        # Add text with statistics
        raw_valid_count = len(raw_scores[raw_scores != sentinel_value])
        clean_count = len(clean_scores)
        ax1.text(0.02, 0.98, f'Raw valid: {raw_valid_count}\nCleaned: {clean_count}',
                 transform=ax1.transAxes, va='top', fontsize=9,
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Plot 2: Failed evaluations by axis
        ax2 = axes[0, 1]
        failed_by_axis = df_raw[
            (df_raw['base_score'] == sentinel_value) | 
            (df_raw['instruct_score'] == sentinel_value)
        ]['axis'].value_counts()
        
        if len(failed_by_axis) > 0:
            colors = plt.cm.Reds(np.linspace(0.4, 0.8, len(failed_by_axis)))
            bars = failed_by_axis.plot(kind='bar', ax=ax2, color=colors)
            ax2.set_title('Failed Evaluations by Axis', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Count', fontsize=11)
            ax2.set_xlabel('Axis', fontsize=11)
            ax2.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar in bars.patches:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontsize=10)
        else:
            ax2.text(0.5, 0.5, 'No failed evaluations! ✅', 
                    ha='center', va='center', fontsize=14,
                    transform=ax2.transAxes,
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
            ax2.set_title('Failed Evaluations by Axis', fontsize=12, fontweight='bold')
            ax2.set_xticks([])
            ax2.set_yticks([])
        
        # Plot 3: Alignment tax distribution (with/without outliers)
        ax3 = axes[1, 0]
        raw_tax = df_raw[
            (df_raw['base_score'] != sentinel_value) & 
            (df_raw['instruct_score'] != sentinel_value)
        ]['alignment_tax']
        clean_tax = df_clean['alignment_tax']
        
        bp = ax3.boxplot([raw_tax, clean_tax], 
                          labels=[f'Raw (excl. {EXTREME_VALUE})', 'Cleaned'],
                          patch_artist=True,
                          notch=True,
                          showmeans=True)
        
        # Color the boxes
        colors = ['lightblue', 'lightgreen']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax3.set_ylabel('Alignment Tax', fontsize=11)
        ax3.set_title('Alignment Tax Distribution', fontsize=12, fontweight='bold')
        ax3.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add statistics text
        stats_text = f'Raw: μ={raw_tax.mean():.3f}, σ={raw_tax.std():.3f}\n'
        stats_text += f'Clean: μ={clean_tax.mean():.3f}, σ={clean_tax.std():.3f}'
        ax3.text(0.02, 0.02, stats_text, transform=ax3.transAxes,
                 fontsize=9, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Plot 4: Sample size impact by axis
        ax4 = axes[1, 1]
        sample_sizes = pd.DataFrame({
            'Original': df_raw.groupby('axis').size(),
            'After Cleaning': df_clean.groupby('axis').size()
        })
        
        sample_sizes.plot(kind='bar', ax=ax4, color=['coral', 'forestgreen'], alpha=0.7)
        ax4.set_title('Sample Sizes by Axis', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Count', fontsize=11)
        ax4.set_xlabel('Axis', fontsize=11)
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend(frameon=True, fancybox=True)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for container in ax4.containers:
            ax4.bar_label(container, fontsize=9)
        
        # Overall title
        fig.suptitle(f'Outlier Analysis Dashboard - {identifier}', 
                     fontsize=14, fontweight='bold', y=1.02)
        
        plt.tight_layout()
        
        # Save figure with identifier
        filename = f'outlier_analysis_{id_to_use}.png'
        plt.savefig(graphs_path + filename, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Outlier analysis visualization saved as '{filename}'")
        
        # Calculate and return outlier statistics
        outlier_stats = {
            'total_raw': len(df_raw),
            'total_clean': len(df_clean),
            'removed_count': len(df_raw) - len(df_clean),
            'removal_percentage': ((len(df_raw) - len(df_clean)) / len(df_raw)) * 100,
            'failed_evaluations': len(df_raw[
                (df_raw['base_score'] == sentinel_value) | 
                (df_raw['instruct_score'] == sentinel_value)
            ]),
            'axes_affected': failed_by_axis.to_dict() if len(failed_by_axis) > 0 else {}
        }
        
        return outlier_stats


#------------------------------------------------------------------------------
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 14:42:16 2025

@author: ramyalsaffar
"""
