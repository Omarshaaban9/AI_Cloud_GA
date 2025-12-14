"""
Cultural Algorithm (CA) for Cloud Resource Allocation
Implements CA with Belief Space for optimal task-to-resource assignments
"""

import random
import copy
from typing import List, Tuple, Dict, Optional
from cloud_environment import Task, Resource, simulate


class Individual:
    """Represents a single solution (chromosome) in the CA population space"""
    
    def __init__(self, assignment: List[int], tasks: List[Task], resources: List[Resource]):
        """
        Args:
            assignment: List of resource indices, one per task
            tasks: List of Task objects
            resources: List of Resource objects
        """
        self.assignment = assignment
        self.tasks = tasks
        self.resources = resources
        self.fitness = None
        self.fitness_score = None  # (time, cost)
    
    def evaluate_fitness(self, objective: str = 'cost'):
        """
        Evaluate fitness of this individual
        Args:
            objective: 'cost', 'time', or 'weighted'
        """
        result = simulate(self.tasks, self.resources, self.assignment)
        total_time = result['total_time']
        total_cost = result['total_cost']
        
        self.fitness_score = (total_time, total_cost)
        
        if objective == 'cost':
            self.fitness = 1.0 / (1.0 + total_cost)
        elif objective == 'time':
            self.fitness = 1.0 / (1.0 + total_time)
        elif objective == 'weighted':
            normalized_time = total_time / 1000.0
            normalized_cost = total_cost / 10000.0
            self.fitness = 1.0 / (1.0 + 0.4 * normalized_time + 0.6 * normalized_cost)
        else:
            raise ValueError(f"Unknown objective: {objective}")
        
        return self.fitness
    
    def __str__(self):
        return f"Assignment: {self.assignment}, Fitness: {self.fitness:.4f}"


class BeliefSpace:
    """
    Belief Space in Cultural Algorithm
    Stores cultural knowledge that influences population evolution
    
    Components:
    1. Situational Knowledge: Best individual found so far
    2. Normative Knowledge: Acceptable ranges for each gene position
    3. Domain Knowledge: Statistical information about the population
    """
    
    def __init__(self, num_tasks: int, num_resources: int):
        """
        Initialize belief space
        
        Args:
            num_tasks: Number of tasks
            num_resources: Number of resources
        """
        self.num_tasks = num_tasks
        self.num_resources = num_resources
        
        # Situational Knowledge: Best individual
        self.best_individual: Optional[Individual] = None
        self.best_fitness = float('-inf')
        
        # Normative Knowledge: Acceptable ranges for each task position
        # For each task position, store which resources are commonly used
        self.normative_ranges = [
            {
                'lower': 0,  # Minimum resource index
                'upper': num_resources - 1,  # Maximum resource index
                'preferred': list(range(num_resources))  # Preferred resources
            }
            for _ in range(num_tasks)
        ]
        
        # Domain Knowledge: Statistics about population
        self.domain_stats = {
            'avg_fitness': 0.0,
            'fitness_variance': 0.0,
            'resource_usage': [0] * num_resources  # Usage count per resource
        }
    
    def update(self, population: List[Individual], accepted: List[Individual]):
        """
        Update belief space based on accepted individuals
        
        Args:
            population: Current population
            accepted: Individuals accepted for belief space update
        """
        if not accepted:
            return
        
        # Update Situational Knowledge (best individual)
        for individual in accepted:
            if individual.fitness > self.best_fitness:
                self.best_fitness = individual.fitness
                self.best_individual = copy.deepcopy(individual)
        
        # Update Normative Knowledge
        # Analyze which resources are commonly used for each task position
        for task_idx in range(self.num_tasks):
            resource_counts = [0] * self.num_resources
            for individual in accepted:
                resource_idx = individual.assignment[task_idx]
                resource_counts[resource_idx] += 1
            
            # Update preferred resources (most commonly used)
            max_count = max(resource_counts)
            if max_count > 0:
                self.normative_ranges[task_idx]['preferred'] = [
                    i for i, count in enumerate(resource_counts) 
                    if count >= max_count * 0.5  # Resources used at least 50% as much as most common
                ]
            else:
                self.normative_ranges[task_idx]['preferred'] = list(range(self.num_resources))
        
        # Update Domain Knowledge
        if population:
            fitnesses = [ind.fitness for ind in population]
            self.domain_stats['avg_fitness'] = sum(fitnesses) / len(fitnesses)
            variance = sum((f - self.domain_stats['avg_fitness'])**2 for f in fitnesses) / len(fitnesses)
            self.domain_stats['fitness_variance'] = variance
            
            # Update resource usage statistics
            self.domain_stats['resource_usage'] = [0] * self.num_resources
            for individual in population:
                for resource_idx in individual.assignment:
                    self.domain_stats['resource_usage'][resource_idx] += 1
    
    def influence(self, individual: Individual, influence_rate: float = 0.3):
        """
        Influence individual based on belief space knowledge
        
        Args:
            individual: Individual to be influenced
            influence_rate: Probability of applying influence (0.0 to 1.0)
        """
        if random.random() > influence_rate:
            return
        
        # Situational Knowledge Influence: Copy some genes from best individual
        if self.best_individual is not None and random.random() < 0.2:
            num_genes = random.randint(1, max(1, len(individual.assignment) // 3))
            positions = random.sample(range(len(individual.assignment)), num_genes)
            for pos in positions:
                individual.assignment[pos] = self.best_individual.assignment[pos]
        
        # Normative Knowledge Influence: Prefer resources in normative ranges
        for task_idx in range(len(individual.assignment)):
            if random.random() < 0.3:  # 30% chance to apply normative influence
                preferred = self.normative_ranges[task_idx]['preferred']
                if preferred:
                    individual.assignment[task_idx] = random.choice(preferred)


class CulturalAlgorithm:
    """
    Cultural Algorithm for Cloud Resource Allocation
    
    Cultural Algorithm has two spaces:
    1. Population Space: Set of candidate solutions (like GA)
    2. Belief Space: Cultural knowledge that influences evolution
    """
    
    def __init__(self, tasks: List[Task], resources: List[Resource],
                 population_size: int = 50,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.8,
                 elitism_count: int = 2,
                 objective: str = 'cost',
                 max_generations: int = 100,
                 acceptance_rate: float = 0.2,
                 influence_rate: float = 0.3):
        """
        Initialize Cultural Algorithm
        
        Args:
            tasks: List of Task objects
            resources: List of Resource objects
            population_size: Number of individuals in population
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
            elitism_count: Number of best individuals to preserve
            objective: 'cost', 'time', or 'weighted'
            max_generations: Maximum number of generations
            acceptance_rate: Fraction of population accepted for belief space update
            influence_rate: Probability of belief space influencing individuals
        """
        self.tasks = tasks
        self.resources = resources
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.objective = objective
        self.max_generations = max_generations
        self.acceptance_rate = acceptance_rate
        self.influence_rate = influence_rate
        
        # Population Space
        self.population: List[Individual] = []
        self.generation = 0
        self.best_fitness_history: List[float] = []
        self.avg_fitness_history: List[float] = []
        self.best_individual: Individual = None
        
        # Belief Space
        self.belief_space = BeliefSpace(len(tasks), len(resources))
    
    def initialize_population(self):
        """Create initial random population"""
        self.population = []
        for _ in range(self.population_size):
            assignment = [random.randint(0, len(self.resources) - 1) 
                         for _ in range(len(self.tasks))]
            individual = Individual(assignment, self.tasks, self.resources)
            individual.evaluate_fitness(self.objective)
            self.population.append(individual)
        
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.best_individual = copy.deepcopy(self.population[0])
        
        # Initialize belief space
        self.belief_space.update(self.population, self.population[:int(self.population_size * self.acceptance_rate)])
    
    def selection(self) -> Tuple[Individual, Individual]:
        """Tournament selection - select two parents"""
        tournament_size = 3
        tournament1 = random.sample(self.population, min(tournament_size, len(self.population)))
        tournament2 = random.sample(self.population, min(tournament_size, len(self.population)))
        
        parent1 = max(tournament1, key=lambda x: x.fitness)
        parent2 = max(tournament2, key=lambda x: x.fitness)
        
        return parent1, parent2
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """Single-point crossover"""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        point = random.randint(1, len(self.tasks) - 1)
        
        child1_assignment = parent1.assignment[:point] + parent2.assignment[point:]
        child2_assignment = parent2.assignment[:point] + parent1.assignment[point:]
        
        child1 = Individual(child1_assignment, self.tasks, self.resources)
        child2 = Individual(child2_assignment, self.tasks, self.resources)
        
        return child1, child2
    
    def mutate(self, individual: Individual):
        """Mutate an individual"""
        if random.random() > self.mutation_rate:
            return
        
        num_mutations = random.randint(1, max(1, len(self.tasks) // 4))
        for _ in range(num_mutations):
            task_idx = random.randint(0, len(self.tasks) - 1)
            individual.assignment[task_idx] = random.randint(0, len(self.resources) - 1)
    
    def evolve(self):
        """Run one generation of evolution"""
        new_population = []
        
        # Elitism: keep best individuals
        for i in range(self.elitism_count):
            new_population.append(copy.deepcopy(self.population[i]))
        
        # Generate rest of population
        while len(new_population) < self.population_size:
            parent1, parent2 = self.selection()
            child1, child2 = self.crossover(parent1, parent2)
            
            # Apply belief space influence BEFORE mutation
            self.belief_space.influence(child1, self.influence_rate)
            self.belief_space.influence(child2, self.influence_rate)
            
            self.mutate(child1)
            self.mutate(child2)
            
            child1.evaluate_fitness(self.objective)
            child2.evaluate_fitness(self.objective)
            
            new_population.append(child1)
            if len(new_population) < self.population_size:
                new_population.append(child2)
        
        # Update population
        self.population = new_population[:self.population_size]
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Update best individual
        if self.population[0].fitness > self.best_individual.fitness:
            self.best_individual = copy.deepcopy(self.population[0])
        
        # Update belief space with accepted individuals
        num_accepted = max(1, int(self.population_size * self.acceptance_rate))
        accepted = self.population[:num_accepted]
        self.belief_space.update(self.population, accepted)
        
        # Record statistics
        self.best_fitness_history.append(self.best_individual.fitness)
        avg_fitness = sum(ind.fitness for ind in self.population) / len(self.population)
        self.avg_fitness_history.append(avg_fitness)
        
        self.generation += 1
    
    def run(self, verbose: bool = True) -> Individual:
        """Run the cultural algorithm"""
        self.initialize_population()
        
        if verbose:
            print(f"Initial Best Fitness: {self.best_individual.fitness:.6f}")
            result = simulate(self.tasks, self.resources, self.best_individual.assignment)
            print(f"Initial Best - Time: {result['total_time']:.2f}, Cost: {result['total_cost']:.2f}")
        
        for generation in range(self.max_generations):
            self.evolve()
            
            if verbose and (generation + 1) % 10 == 0:
                result = simulate(self.tasks, self.resources, self.best_individual.assignment)
                print(f"Generation {generation + 1}/{self.max_generations} - "
                      f"Best Fitness: {self.best_individual.fitness:.6f}, "
                      f"Time: {result['total_time']:.2f}, Cost: {result['total_cost']:.2f}")
        
        if verbose:
            print(f"\nFinal Best Fitness: {self.best_individual.fitness:.6f}")
            result = simulate(self.tasks, self.resources, self.best_individual.assignment)
            print(f"Final Best - Time: {result['total_time']:.2f}, Cost: {result['total_cost']:.2f}")
            print(f"Final Assignment: {self.best_individual.assignment}")
        
        return self.best_individual
    
    def get_statistics(self) -> Dict:
        """Get statistics about the CA run"""
        result = simulate(self.tasks, self.resources, self.best_individual.assignment)
        return {
            'best_fitness': self.best_individual.fitness,
            'best_time': result['total_time'],
            'best_cost': result['total_cost'],
            'best_assignment': self.best_individual.assignment,
            'generations': self.generation,
            'fitness_history': self.best_fitness_history,
            'avg_fitness_history': self.avg_fitness_history,
            'belief_space_stats': {
                'best_fitness': self.belief_space.best_fitness,
                'avg_fitness': self.belief_space.domain_stats['avg_fitness'],
                'resource_usage': self.belief_space.domain_stats['resource_usage']
            }
        }


if __name__ == "__main__":
    # Example usage
    from cloud_environment import Task, Resource
    
    tasks = [
        Task(0, 120),
        Task(1, 200),
        Task(2, 150)
    ]
    
    resources = [
        Resource(0, 10, 5),
        Resource(1, 20, 8)
    ]
    
    ca = CulturalAlgorithm(
        tasks, resources,
        population_size=30,
        max_generations=50,
        objective='cost'
    )
    
    best = ca.run()
    stats = ca.get_statistics()
    print("\nCA Statistics:", stats)

