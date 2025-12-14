"""
Simulation Data Generator and Baseline Strategies
Generates test data and implements baseline allocation strategies
"""

import random
import json
from cloud_environment import Task, Resource, simulate


def generate_random_tasks(num_tasks, min_length=50, max_length=500):
    """Generate random tasks"""
    tasks = []
    for i in range(num_tasks):
        length = random.randint(min_length, max_length)
        tasks.append(Task(i, length))
    return tasks


def generate_random_resources(num_resources, min_speed=5, max_speed=30, 
                              min_cost=3, max_cost=15):
    """Generate random resources"""
    resources = []
    for i in range(num_resources):
        speed = random.uniform(min_speed, max_speed)
        cost = random.uniform(min_cost, max_cost)
        resources.append(Resource(i, speed, cost))
    return resources


def save_to_json(tasks, resources, tasks_file='tasks.json', resources_file='resources.json'):
    """Save tasks and resources to JSON files"""
    tasks_data = [{"id": t.id, "length": t.length} for t in tasks]
    resources_data = [{"id": r.id, "speed": r.speed, "cost": r.cost} for r in resources]
    
    with open(tasks_file, 'w') as f:
        json.dump(tasks_data, f, indent=2)
    
    with open(resources_file, 'w') as f:
        json.dump(resources_data, f, indent=2)
    
    print(f"Saved {len(tasks)} tasks to {tasks_file}")
    print(f"Saved {len(resources)} resources to {resources_file}")


def random_assignment(tasks, resources):
    """Random assignment strategy"""
    return [random.randint(0, len(resources) - 1) for _ in range(len(tasks))]


def fastest_assignment(tasks, resources):
    """Assign all tasks to the fastest resource"""
    fastest_idx = max(range(len(resources)), key=lambda i: resources[i].speed)
    return [fastest_idx for _ in range(len(tasks))]


def best_value_assignment(tasks, resources):
    """Assign all tasks to resource with best speed/cost ratio"""
    best_idx = max(range(len(resources)), 
                   key=lambda i: resources[i].speed / resources[i].cost)
    return [best_idx for _ in range(len(tasks))]


def cheapest_assignment(tasks, resources):
    """Assign all tasks to the cheapest resource"""
    cheapest_idx = min(range(len(resources)), key=lambda i: resources[i].cost)
    return [cheapest_idx for _ in range(len(tasks))]


if __name__ == "__main__":
    print("="*60)
    print("SIMULATION DATA GENERATOR")
    print("="*60)
    
    # Get user input
    num_tasks = int(input("Enter number of tasks: ") or "5")
    num_resources = int(input("Enter number of resources: ") or "3")
    
    print("\nGenerating random data...")
    tasks = generate_random_tasks(num_tasks)
    resources = generate_random_resources(num_resources)
    
    print("\nGenerated Tasks:")
    for task in tasks:
        print(f"  Task {task.id}: Length = {task.length}")
    
    print("\nGenerated Resources:")
    for resource in resources:
        print(f"  Resource {resource.id}: Speed = {resource.speed:.2f}, Cost = {resource.cost:.2f}")
    
    # Save to JSON
    save = input("\nSave to JSON files? (y/n): ").lower() == 'y'
    if save:
        save_to_json(tasks, resources)
        print("\nData saved successfully!")
    
    # Test baseline strategies
    print("\n" + "="*60)
    print("BASELINE STRATEGY RESULTS")
    print("="*60)
    
    strategies = {
        "Random": random_assignment(tasks, resources),
        "Fastest Resource": fastest_assignment(tasks, resources),
        "Best Value": best_value_assignment(tasks, resources),
        "Cheapest": cheapest_assignment(tasks, resources)
    }
    
    for name, assignment in strategies.items():
        result = simulate(tasks, resources, assignment)
        print(f"\n{name}:")
        print(f"  Assignment: {assignment}")
        print(f"  Total Time: {result['total_time']:.2f}")
        print(f"  Total Cost: {result['total_cost']:.2f}")

