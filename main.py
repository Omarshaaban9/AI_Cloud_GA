"""
Main script for Cloud Resource Allocation using Cultural Algorithm
Compares Cultural Algorithm with baseline strategies
"""

import json
import time
from cloud_environment import Task, Resource, simulate
from simulation_generator import random_assignment, fastest_assignment, best_value_assignment
from cultural_algorithm import CulturalAlgorithm
from visualization import plot_comparison, plot_ga_convergence


def load_data_from_json():
    """Load tasks and resources from JSON files"""
    try:
        with open('tasks.json', 'r') as f:
            tasks_data = json.load(f)
        with open('resources.json', 'r') as f:
            resources_data = json.load(f)
        
        tasks = [Task(t['id'], t['length']) for t in tasks_data]
        resources = [Resource(r['id'], r['speed'], r['cost']) for r in resources_data]
        
        return tasks, resources
    except FileNotFoundError:
        print("JSON files not found. Please run simulation_generator.py first or create tasks.json and resources.json")
        return None, None


def run_baseline_strategies(tasks, resources):
    """Run baseline allocation strategies and return results"""
    print("\n" + "="*60)
    print("BASELINE ALLOCATION STRATEGIES")
    print("="*60)
    
    strategies = {
        "Random": random_assignment(tasks, resources),
        "Fastest Resource": fastest_assignment(tasks, resources),
        "Best Value (Speed/Cost)": best_value_assignment(tasks, resources)
    }
    
    results = {}
    for strategy_name, assignment in strategies.items():
        result = simulate(tasks, resources, assignment)
        results[strategy_name] = {
            'assignment': assignment,
            'time': result['total_time'],
            'cost': result['total_cost']
        }
        print(f"\n{strategy_name}:")
        print(f"  Assignment: {assignment}")
        print(f"  Total Time: {result['total_time']:.2f}")
        print(f"  Total Cost: {result['total_cost']:.2f}")
    
    return results




def run_cultural_algorithm(tasks, resources, objective='cost',
                           population_size=50, max_generations=100,
                           mutation_rate=0.1, crossover_rate=0.8):
    """Run Cultural Algorithm and return results"""
    print("\n" + "="*60)
    print(f"CULTURAL ALGORITHM (Objective: {objective.upper()})")
    print("="*60)
    
    ca = CulturalAlgorithm(
        tasks=tasks,
        resources=resources,
        population_size=population_size,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        objective=objective,
        max_generations=max_generations
    )
    
    start_time = time.time()
    best_individual = ca.run(verbose=True)
    elapsed_time = time.time() - start_time
    
    stats = ca.get_statistics()
    stats['elapsed_time'] = elapsed_time
    
    print(f"\nCA Execution Time: {elapsed_time:.2f} seconds")
    
    return stats, ca


def run_experiments():
    """Run complete set of experiments"""
    print("="*60)
    print("CLOUD RESOURCE ALLOCATION - COMPREHENSIVE EXPERIMENTS")
    print("="*60)
    
    # Load data
    tasks, resources = load_data_from_json()
    if tasks is None or resources is None:
        print("\nGenerating sample data...")
        from simulation_generator import generate_random_tasks, generate_random_resources
        tasks = generate_random_tasks(5)
        resources = generate_random_resources(3)
        print("Using generated sample data.")
    
    print(f"\nLoaded {len(tasks)} tasks and {len(resources)} resources")
    print("\nTasks:")
    for task in tasks:
        print(f"  Task {task.id}: Length = {task.length}")
    
    print("\nResources:")
    for resource in resources:
        print(f"  Resource {resource.id}: Speed = {resource.speed:.2f}, Cost = {resource.cost:.2f}")
    
    # Run baseline strategies
    baseline_results = run_baseline_strategies(tasks, resources)
    
    # Run Cultural Algorithm
    print("\n" + "="*60)
    print("RUNNING CULTURAL ALGORITHM")
    print("="*60)
    
    all_results = baseline_results.copy()
    algorithm_results = {}
    
    objective = 'cost'  # Can be changed to 'time' or 'weighted'
    
    # Cultural Algorithm
    ca_stats, ca = run_cultural_algorithm(
        tasks, resources,
        objective=objective,
        population_size=50,
        max_generations=100
    )
    all_results['Cultural Algorithm'] = {
        'time': ca_stats['best_time'],
        'cost': ca_stats['best_cost'],
        'assignment': ca_stats['best_assignment']
    }
    algorithm_results['Cultural Algorithm'] = ca_stats
    
    # Comparison summary
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    print(f"\n{'Strategy':<30} {'Time':<15} {'Cost':<15}")
    print("-" * 60)
    for strategy, result in all_results.items():
        print(f"{strategy:<30} {result['time']:<15.2f} {result['cost']:<15.2f}")
    
    # Find best strategies
    best_time_strategy = min(all_results.items(), key=lambda x: x[1]['time'])
    best_cost_strategy = min(all_results.items(), key=lambda x: x[1]['cost'])
    
    print(f"\nBest Time: {best_time_strategy[0]} ({best_time_strategy[1]['time']:.2f})")
    print(f"Best Cost: {best_cost_strategy[0]} ({best_cost_strategy[1]['cost']:.2f})")
    
    # Generate visualizations
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    try:
        plot_comparison(all_results)
        if ca:
            plot_ga_convergence(ca, "Cultural Algorithm Convergence")
            print("✓ Cultural Algorithm convergence plot generated")
        print("\nVisualizations saved successfully!")
        print("\nNote: To generate plots for different CA settings, run:")
        print("  python generate_ca_plots.py")
    except Exception as e:
        print(f"Error generating visualizations: {e}")
        print("Make sure matplotlib is installed: pip install matplotlib")
    
    return all_results, algorithm_results


if __name__ == "__main__":
    run_experiments()
