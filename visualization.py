"""
Visualization module for Cloud Resource Allocation results
"""

import matplotlib.pyplot as plt
from typing import Dict
from cultural_algorithm import CulturalAlgorithm


def plot_comparison(results: Dict):
    """
    Plot comparison of different allocation strategies
    Args:
        results: Dictionary mapping strategy names to results with 'time' and 'cost' keys
    """
    strategies = list(results.keys())
    times = [results[s]['time'] for s in strategies]
    costs = [results[s]['cost'] for s in strategies]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Time comparison
    bars1 = ax1.bar(strategies, times, color='skyblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Strategy', fontsize=12)
    ax1.set_ylabel('Total Time', fontsize=12)
    ax1.set_title('Total Execution Time Comparison', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9)
    
    # Cost comparison
    bars2 = ax2.bar(strategies, costs, color='lightcoral', edgecolor='darkred', alpha=0.7)
    ax2.set_xlabel('Strategy', fontsize=12)
    ax2.set_ylabel('Total Cost', fontsize=12)
    ax2.set_title('Total Cost Comparison', fontsize=14, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('comparison_results.png', dpi=300, bbox_inches='tight')
    print("Saved: comparison_results.png")
    plt.close()


def plot_ga_convergence(algorithm: CulturalAlgorithm, title: str = "Cultural Algorithm Convergence"):
    """
    Plot algorithm convergence over generations (works for both GA and CA)
    Args:
        algorithm: GeneticAlgorithm or CulturalAlgorithm object after running
        title: Plot title
    """
    if not algorithm.best_fitness_history:
        print("No convergence data available")
        return
    
    generations = range(1, len(algorithm.best_fitness_history) + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Fitness convergence
    ax1.plot(generations, algorithm.best_fitness_history, 'b-', linewidth=2, label='Best Fitness')
    ax1.plot(generations, algorithm.avg_fitness_history, 'r--', linewidth=2, label='Average Fitness')
    ax1.set_xlabel('Generation', fontsize=12)
    ax1.set_ylabel('Fitness', fontsize=12)
    ax1.set_title(f'{title} - Fitness', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Since we don't track time/cost per generation, we'll show fitness improvement
    improvement = [(algorithm.best_fitness_history[i] - algorithm.best_fitness_history[0]) / algorithm.best_fitness_history[0] * 100
                   for i in range(len(algorithm.best_fitness_history))]
    
    ax2.plot(generations, improvement, 'g-', linewidth=2)
    ax2.set_xlabel('Generation', fontsize=12)
    ax2.set_ylabel('Improvement (%)', fontsize=12)
    ax2.set_title(f'{title} - Improvement Over Initial', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    filename = title.lower().replace(' ', '_').replace('(', '').replace(')', '') + '.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved: {filename}")
    plt.close()


def plot_results(results: Dict, save_path: str = 'results.png'):
    """
    Generic plotting function for results
    Args:
        results: Dictionary of results
        save_path: Path to save the plot
    """
    # This is a placeholder for additional plotting functions
    pass


def plot_pareto_front(ga_results: Dict):
    """
    Plot Pareto front for multi-objective optimization (time vs cost)
    Args:
        ga_results: Dictionary of GA results with different objectives
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Extract time and cost for each strategy
    strategies = []
    times = []
    costs = []
    
    for strategy, stats in ga_results.items():
        strategies.append(strategy)
        times.append(stats['best_time'])
        costs.append(stats['best_cost'])
    
    # Scatter plot
    scatter = ax.scatter(times, costs, s=100, alpha=0.6, c=range(len(strategies)), cmap='viridis')
    
    # Add labels
    for i, strategy in enumerate(strategies):
        ax.annotate(strategy, (times[i], costs[i]), 
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    ax.set_xlabel('Total Time', fontsize=12)
    ax.set_ylabel('Total Cost', fontsize=12)
    ax.set_title('Pareto Front: Time vs Cost Trade-off', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pareto_front.png', dpi=300, bbox_inches='tight')
    print("Saved: pareto_front.png")
    plt.close()

