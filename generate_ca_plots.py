"""
Generate Cultural Algorithm performance plots for different parameter settings
Required: "plot of the performance across the generations for each setting"
"""

import json
import matplotlib.pyplot as plt
from cloud_environment import Task, Resource
from cultural_algorithm import CulturalAlgorithm
from simulation_generator import generate_random_tasks, generate_random_resources


def generate_plots_for_different_settings():
    """Generate CA performance plots for different parameter settings"""
    
    # Generate test data
    print("Generating test data...")
    tasks = generate_random_tasks(5, min_length=50, max_length=500)
    resources = generate_random_resources(3, min_speed=5, max_speed=30, min_cost=3, max_cost=15)
    
    print(f"Tasks: {[t.length for t in tasks]}")
    print(f"Resources: {[(r.speed, r.cost) for r in resources]}\n")
    
    # Different settings to test
    settings = [
        {
            'name': 'Setting 1: Default',
            'population_size': 50,
            'max_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.2,
            'influence_rate': 0.3
        },
        {
            'name': 'Setting 2: Small Population',
            'population_size': 30,
            'max_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.2,
            'influence_rate': 0.3
        },
        {
            'name': 'Setting 3: Large Population',
            'population_size': 100,
            'max_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.2,
            'influence_rate': 0.3
        },
        {
            'name': 'Setting 4: Low Mutation',
            'population_size': 50,
            'max_generations': 100,
            'mutation_rate': 0.05,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.2,
            'influence_rate': 0.3
        },
        {
            'name': 'Setting 5: High Mutation',
            'population_size': 50,
            'max_generations': 100,
            'mutation_rate': 0.2,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.2,
            'influence_rate': 0.3
        },
        {
            'name': 'Setting 6: Low Crossover',
            'population_size': 50,
            'max_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.5,
            'acceptance_rate': 0.2,
            'influence_rate': 0.3
        },
        {
            'name': 'Setting 7: High Influence Rate',
            'population_size': 50,
            'max_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.2,
            'influence_rate': 0.5
        },
        {
            'name': 'Setting 8: High Acceptance Rate',
            'population_size': 50,
            'max_generations': 100,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'acceptance_rate': 0.4,
            'influence_rate': 0.3
        }
    ]
    
    # Run CA for each setting and collect data
    all_results = []
    
    for setting in settings:
        print(f"\nRunning {setting['name']}...")
        print(f"  Population: {setting['population_size']}, "
              f"Mutation: {setting['mutation_rate']}, "
              f"Crossover: {setting['crossover_rate']}, "
              f"Acceptance: {setting['acceptance_rate']}, "
              f"Influence: {setting['influence_rate']}")
        
        ca = CulturalAlgorithm(
            tasks=tasks,
            resources=resources,
            population_size=setting['population_size'],
            max_generations=setting['max_generations'],
            mutation_rate=setting['mutation_rate'],
            crossover_rate=setting['crossover_rate'],
            acceptance_rate=setting['acceptance_rate'],
            influence_rate=setting['influence_rate'],
            objective='cost'
        )
        
        ca.run(verbose=False)
        stats = ca.get_statistics()
        
        all_results.append({
            'setting': setting['name'],
            'ca': ca,
            'stats': stats,
            'params': setting
        })
        
        print(f"  Final Cost: {stats['best_cost']:.2f}, Time: {stats['best_time']:.2f}")
    
    # Generate plots
    print("\n" + "="*60)
    print("GENERATING PERFORMANCE PLOTS")
    print("="*60)
    
    # Plot 1: All settings on one graph (fitness convergence)
    fig, ax = plt.subplots(figsize=(12, 8))
    for result in all_results:
        generations = range(1, len(result['ca'].best_fitness_history) + 1)
        ax.plot(generations, result['ca'].best_fitness_history, 
               linewidth=2, label=result['setting'], alpha=0.8)
    
    ax.set_xlabel('Generation', fontsize=12)
    ax.set_ylabel('Best Fitness', fontsize=12)
    ax.set_title('Cultural Algorithm Performance Across Generations - All Settings', 
                fontsize=14, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('ca_performance_all_settings.png', dpi=300, bbox_inches='tight')
    print("Saved: ca_performance_all_settings.png")
    plt.close()
    
    # Plot 2: Individual plots for each setting
    num_settings = len(all_results)
    cols = 2
    rows = (num_settings + 1) // 2
    
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4*rows))
    axes = axes.flatten() if num_settings > 1 else [axes]
    
    for idx, result in enumerate(all_results):
        ax = axes[idx]
        generations = range(1, len(result['ca'].best_fitness_history) + 1)
        
        ax.plot(generations, result['ca'].best_fitness_history, 'b-', 
               linewidth=2, label='Best Fitness')
        ax.plot(generations, result['ca'].avg_fitness_history, 'r--', 
               linewidth=2, label='Average Fitness')
        
        ax.set_xlabel('Generation', fontsize=10)
        ax.set_ylabel('Fitness', fontsize=10)
        ax.set_title(result['setting'], fontsize=11, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
    
    # Hide extra subplots
    for idx in range(num_settings, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('ca_performance_individual_settings.png', dpi=300, bbox_inches='tight')
    print("Saved: ca_performance_individual_settings.png")
    plt.close()
    
    # Plot 3: Comparison of final results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    setting_names = [r['setting'] for r in all_results]
    final_costs = [r['stats']['best_cost'] for r in all_results]
    final_times = [r['stats']['best_time'] for r in all_results]
    
    ax1.barh(range(len(setting_names)), final_costs, color='lightcoral', alpha=0.7)
    ax1.set_yticks(range(len(setting_names)))
    ax1.set_yticklabels(setting_names, fontsize=9)
    ax1.set_xlabel('Final Cost', fontsize=12)
    ax1.set_title('Final Cost Comparison - Different Settings', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    ax2.barh(range(len(setting_names)), final_times, color='skyblue', alpha=0.7)
    ax2.set_yticks(range(len(setting_names)))
    ax2.set_yticklabels(setting_names, fontsize=9)
    ax2.set_xlabel('Final Time', fontsize=12)
    ax2.set_title('Final Time Comparison - Different Settings', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ca_settings_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: ca_settings_comparison.png")
    plt.close()
    
    print("\nAll plots generated successfully!")
    print("\nGenerated files:")
    print("  1. ca_performance_all_settings.png - All settings on one graph")
    print("  2. ca_performance_individual_settings.png - Individual plots for each setting")
    print("  3. ca_settings_comparison.png - Final results comparison")


if __name__ == "__main__":
    generate_plots_for_different_settings()

