#!/usr/bin/env python3
"""
Visualization script for AI CLI Tools test results
Generates charts and visual comparisons
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class ResultsVisualizer:
    """Visualize test results with charts and graphs"""
    
    def __init__(self, results_file: str):
        """Initialize with results JSON file"""
        self.results_file = Path(results_file)
        with open(self.results_file) as f:
            self.data = json.load(f)
            
        self.tools = ["claude_code", "codex", "gemini_cli"]
        self.tool_names = {
            "claude_code": "Claude Code",
            "codex": "OpenAI Codex",
            "gemini_cli": "Google Gemini CLI"
        }
        
    def create_overall_comparison(self):
        """Create overall score comparison chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Calculate average scores per tool
        tool_scores = {tool: [] for tool in self.tools}
        
        for test_id, test_data in self.data["tests"].items():
            for tool in self.tools:
                if tool in test_data["evaluations"]:
                    score = test_data["evaluations"][tool]["average_score"]
                    tool_scores[tool].append(score)
        
        # Calculate averages
        avg_scores = {}
        for tool, scores in tool_scores.items():
            avg_scores[tool] = np.mean(scores) if scores else 0
            
        # Create bar chart
        tools_display = [self.tool_names[t] for t in self.tools]
        scores = [avg_scores[t] for t in self.tools]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        bars = ax.bar(tools_display, scores, color=colors, alpha=0.8)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{score:.1f}', ha='center', va='bottom', fontsize=12)
        
        ax.set_ylim(0, 10)
        ax.set_ylabel('Average Score', fontsize=12)
        ax.set_title('Overall Performance Comparison', fontsize=16, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.results_file.parent / "overall_comparison.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    def create_test_breakdown(self):
        """Create detailed test breakdown chart"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Prepare data
        test_names = []
        claude_scores = []
        codex_scores = []
        gemini_scores = []
        
        for test_id, test_data in self.data["tests"].items():
            # Get test name (shortened)
            test_name = test_id.replace("test_", "").replace("_", " ").title()
            if len(test_name) > 20:
                test_name = test_name[:20] + "..."
            test_names.append(test_name)
            
            # Get scores
            evals = test_data["evaluations"]
            claude_scores.append(evals.get("claude_code", {}).get("average_score", 0))
            codex_scores.append(evals.get("codex", {}).get("average_score", 0))
            gemini_scores.append(evals.get("gemini_cli", {}).get("average_score", 0))
        
        # Create grouped bar chart
        x = np.arange(len(test_names))
        width = 0.25
        
        bars1 = ax.bar(x - width, claude_scores, width, label='Claude Code', color='#FF6B6B', alpha=0.8)
        bars2 = ax.bar(x, codex_scores, width, label='OpenAI Codex', color='#4ECDC4', alpha=0.8)
        bars3 = ax.bar(x + width, gemini_scores, width, label='Google Gemini', color='#45B7D1', alpha=0.8)
        
        # Customize chart
        ax.set_xlabel('Test', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.set_title('Detailed Test Performance by Tool', fontsize=16, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(test_names, rotation=45, ha='right')
        ax.legend()
        ax.set_ylim(0, 10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.results_file.parent / "test_breakdown.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    def create_execution_time_comparison(self):
        """Create execution time comparison chart"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Collect execution times
        tool_times = {tool: [] for tool in self.tools}
        
        for test_data in self.data["tests"].values():
            for tool in self.tools:
                if tool in test_data["evaluations"]:
                    time = test_data["evaluations"][tool]["execution_time"]
                    tool_times[tool].append(time)
        
        # Create box plot
        data_to_plot = [tool_times[tool] for tool in self.tools]
        tool_labels = [self.tool_names[tool] for tool in self.tools]
        
        bp = ax.boxplot(data_to_plot, labels=tool_labels, patch_artist=True)
        
        # Customize colors
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel('Execution Time (seconds)', fontsize=12)
        ax.set_title('Execution Time Distribution', fontsize=16, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = self.results_file.parent / "execution_times.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    def create_success_rate_chart(self):
        """Create success rate comparison"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Calculate success rates
        tool_successes = {tool: {"success": 0, "total": 0} for tool in self.tools}
        
        for test_data in self.data["tests"].values():
            for tool in self.tools:
                if tool in test_data["evaluations"]:
                    tool_successes[tool]["total"] += 1
                    if test_data["evaluations"][tool]["success"]:
                        tool_successes[tool]["success"] += 1
        
        # Calculate percentages
        success_rates = {}
        for tool, data in tool_successes.items():
            if data["total"] > 0:
                success_rates[tool] = (data["success"] / data["total"]) * 100
            else:
                success_rates[tool] = 0
                
        # Create pie chart
        labels = [f"{self.tool_names[tool]}\n{rate:.1f}%" for tool, rate in success_rates.items()]
        sizes = list(success_rates.values())
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        explode = (0.05, 0.05, 0.05)  # Slightly separate slices
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='',
               shadow=True, startangle=90)
        ax.axis('equal')
        ax.set_title('Test Success Rates', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.results_file.parent / "success_rates.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    def create_criteria_heatmap(self):
        """Create heatmap of scores by criteria"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Collect all criteria and scores
        criteria_scores = {}
        all_criteria = set()
        
        for test_data in self.data["tests"].values():
            for tool, evaluation in test_data["evaluations"].items():
                if "scores" in evaluation:
                    for criterion, score in evaluation["scores"].items():
                        all_criteria.add(criterion)
                        if criterion not in criteria_scores:
                            criteria_scores[criterion] = {}
                        if tool not in criteria_scores[criterion]:
                            criteria_scores[criterion][tool] = []
                        criteria_scores[criterion][tool].append(score)
        
        # Calculate average scores
        heatmap_data = []
        criteria_list = sorted(list(all_criteria))
        
        for criterion in criteria_list:
            row = []
            for tool in self.tools:
                if tool in criteria_scores.get(criterion, {}):
                    avg_score = np.mean(criteria_scores[criterion][tool])
                else:
                    avg_score = 0
                row.append(avg_score)
            heatmap_data.append(row)
        
        # Create heatmap
        heatmap_data = np.array(heatmap_data)
        im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=10)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(self.tools)))
        ax.set_yticks(np.arange(len(criteria_list)))
        ax.set_xticklabels([self.tool_names[t] for t in self.tools])
        ax.set_yticklabels(criteria_list)
        
        # Rotate the tick labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Average Score', rotation=270, labelpad=15)
        
        # Add text annotations
        for i in range(len(criteria_list)):
            for j in range(len(self.tools)):
                text = ax.text(j, i, f'{heatmap_data[i, j]:.1f}',
                             ha="center", va="center", color="black", fontsize=10)
        
        ax.set_title('Performance Heatmap by Evaluation Criteria', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        output_path = self.results_file.parent / "criteria_heatmap.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    def generate_all_visualizations(self):
        """Generate all visualization charts"""
        print("Generating visualizations...")
        
        charts = []
        
        # Overall comparison
        try:
            chart = self.create_overall_comparison()
            charts.append(chart)
            print(f"✓ Created: {chart.name}")
        except Exception as e:
            print(f"✗ Failed to create overall comparison: {e}")
            
        # Test breakdown
        try:
            chart = self.create_test_breakdown()
            charts.append(chart)
            print(f"✓ Created: {chart.name}")
        except Exception as e:
            print(f"✗ Failed to create test breakdown: {e}")
            
        # Execution times
        try:
            chart = self.create_execution_time_comparison()
            charts.append(chart)
            print(f"✓ Created: {chart.name}")
        except Exception as e:
            print(f"✗ Failed to create execution time chart: {e}")
            
        # Success rates
        try:
            chart = self.create_success_rate_chart()
            charts.append(chart)
            print(f"✓ Created: {chart.name}")
        except Exception as e:
            print(f"✗ Failed to create success rate chart: {e}")
            
        # Criteria heatmap
        try:
            chart = self.create_criteria_heatmap()
            charts.append(chart)
            print(f"✓ Created: {chart.name}")
        except Exception as e:
            print(f"✗ Failed to create criteria heatmap: {e}")
            
        print(f"\nGenerated {len(charts)} visualizations in {self.results_file.parent}")
        return charts


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Visualize AI CLI Tools test results")
    parser.add_argument("results_file", help="Path to results JSON file")
    parser.add_argument("--charts", nargs="+", 
                       choices=["overall", "breakdown", "time", "success", "heatmap"],
                       help="Specific charts to generate (default: all)")
    
    args = parser.parse_args()
    
    # Check if matplotlib is installed
    try:
        import matplotlib
        import seaborn
    except ImportError:
        print("Installing required visualization libraries...")
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "pip", "install", "matplotlib", "seaborn"])
        print("Please run the script again.")
        sys.exit(1)
    
    # Create visualizer
    visualizer = ResultsVisualizer(args.results_file)
    
    if args.charts:
        # Generate specific charts
        chart_methods = {
            "overall": visualizer.create_overall_comparison,
            "breakdown": visualizer.create_test_breakdown,
            "time": visualizer.create_execution_time_comparison,
            "success": visualizer.create_success_rate_chart,
            "heatmap": visualizer.create_criteria_heatmap
        }
        
        for chart_type in args.charts:
            if chart_type in chart_methods:
                try:
                    chart_methods[chart_type]()
                    print(f"✓ Generated {chart_type} chart")
                except Exception as e:
                    print(f"✗ Failed to generate {chart_type}: {e}")
    else:
        # Generate all charts
        visualizer.generate_all_visualizations()


if __name__ == "__main__":
    main()