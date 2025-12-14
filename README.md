# Cloud Resource Allocation using Cultural Algorithm

## Project Overview

This project implements **Cultural Algorithm (CA)** for optimal cloud resource allocation, solving the problem of assigning computing tasks to available cloud resources to minimize cost, execution time, or a weighted combination of both.

## Project Description

**Context and Problem Statement:** Cloud computing demands efficient resource allocation to balance load and reduce operational costs. This project uses evolutionary algorithms (Cultural Algorithm) and systematic search (Backtracking) to devise optimal resource allocation strategies.

**Key Terms and Concepts:**
- **Resource Allocation:** Assigning computing resources to tasks in an optimal way
- **Cultural Algorithm (CA):** An evolutionary algorithm that maintains a belief space with cultural knowledge to guide population evolution
- **Belief Space:** Cultural knowledge including situational, normative, and domain knowledge
- **Fitness Evaluation:** Assessing solutions based on cost and performance metrics

## Features

- ✅ Python simulation that models cloud tasks and resource constraints
- ✅ **Cultural Algorithm** with Belief Space (Situational, Normative, Domain Knowledge)
- ✅ Multiple fitness objectives (cost minimization, time minimization, weighted)
- ✅ Comparison with baseline allocation strategies (Random, Fastest Resource, Best Value)
- ✅ **Graphical User Interface (GUI)** with proper input/output design
- ✅ Experimental data visualization and performance plots
- ✅ Comprehensive evaluation metrics
- ✅ **State Space Representation** documentation
- ✅ **Comprehensive Report** with problem definition, literature review, and diagrams
- ✅ **Discussion & Analysis** document covering all algorithm parameters

## Project Structure

```
AI_Cloud_GA/
├── cloud_environment.py           # Task and Resource classes, simulation function
├── cultural_algorithm.py          # Cultural Algorithm with Belief Space
├── simulation_generator.py        # Data generation and baseline strategies
├── main.py                        # Main experiment runner (command-line)
├── gui.py                         # Graphical User Interface
├── visualization.py               # Plotting and visualization functions
├── generate_ca_plots.py           # Generate performance plots for different settings
├── REPORT.md                      # Comprehensive project report
├── DISCUSSION_ANALYSIS.md         # Detailed analysis document
├── REQUIREMENTS_CHECKLIST.md      # Requirements verification
├── tasks.json                     # Sample task data (generated)
├── resources.json                 # Sample resource data (generated)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

**Note:** The GUI requires `tkinter` which is usually included with Python. If not available, install it:
- **Windows/Mac:** Usually pre-installed
- **Linux:** `sudo apt-get install python3-tk` (Ubuntu/Debian)

## Usage

### Option 1: Graphical User Interface (Recommended)

Launch the GUI application:

```bash
python gui.py
```

The GUI provides:
- **Input Configuration Tab:** Generate or load tasks and resources
- **Algorithm Execution Tab:** Select algorithm, set parameters, and run
- **Results & Visualization Tab:** View results and performance plots

### Option 2: Command-Line Interface

**Generate Data:**
```bash
python simulation_generator.py
```

**Run Experiments:**
```bash
python main.py
```

This will run:
- Baseline strategies (Random, Fastest, Best Value)
- Cultural Algorithm

### Option 3: Use Existing Data

If you already have `tasks.json` and `resources.json` files:

```bash
python main.py
```

## How It Works

### 1. Problem Representation

- **Tasks:** Represented by their computational length/requirements
- **Resources:** Represented by processing speed and cost per unit time
- **Solution (Chromosome/State):** A list assigning each task to a resource
- **State Space:** All possible assignments (M^N states)
- **Actions:** Assigning a task to a resource

State space representation is documented in REPORT.md Section 3.

### 2. Cultural Algorithm Components

**Population Space:**
- **Initialization:** Random population of assignment solutions
- **Fitness Evaluation:** Calculates total time and cost for each solution
- **Selection:** Tournament selection to choose parents
- **Crossover:** Single-point crossover to create offspring
- **Mutation:** Randomly changes some task assignments
- **Elitism:** Preserves best solutions across generations

**Belief Space:**
- **Situational Knowledge:** Best individual found so far
- **Normative Knowledge:** Preferred resources for each task position
- **Domain Knowledge:** Population statistics (average fitness, variance, resource usage)
- **Influence:** Belief space guides population evolution

### 3. Objectives

All algorithms can optimize for:
- **Cost:** Minimize total execution cost
- **Time:** Minimize total execution time
- **Weighted:** Balance between time and cost (0.4×time + 0.6×cost)

### 4. Baseline Strategies

For comparison, the project includes:
- **Random:** Random task-to-resource assignment
- **Fastest Resource:** Assign all tasks to the fastest resource
- **Best Value:** Assign all tasks to resource with best speed/cost ratio

## Output

The program generates:

1. **Console Output:**
   - Baseline strategy results
   - GA convergence progress
   - Final comparison summary

2. **Visualization Files:**
   - `comparison_results.png`: Bar charts comparing all strategies
   - `ga_convergence_*.png`: Convergence plots for each GA objective
   - `pareto_front.png`: Time vs cost trade-off visualization

## Example Output

```
================================================================
CLOUD RESOURCE ALLOCATION - GENETIC ALGORITHM
================================================================

Loaded 5 tasks and 6 resources

BASELINE ALLOCATION STRATEGIES
================================================================
Random:
  Total Time: 45.23
  Total Cost: 1234.56

GENETIC ALGORITHM (Objective: COST)
================================================================
Generation 10/100 - Best Fitness: 0.000812, Time: 38.45, Cost: 1123.45
...
Final Best - Time: 35.67, Cost: 1089.12

COMPARISON SUMMARY
================================================================
Strategy                  Time            Cost           
---------------------------------------------------------------
Random                    45.23           1234.56        
GA (Cost)                 35.67           1089.12        
...
```

## Configuration

You can modify GA parameters in `main.py`:

```python
ga = GeneticAlgorithm(
    tasks=tasks,
    resources=resources,
    population_size=50,      # Population size
    mutation_rate=0.1,       # Mutation probability
    crossover_rate=0.8,      # Crossover probability
    elitism_count=2,         # Number of elite individuals
    objective='cost',        # 'cost', 'time', or 'weighted'
    max_generations=100      # Maximum generations
)
```

## Evaluation Metrics

The project evaluates solutions based on:
- **Total Execution Time:** Sum of execution times for all tasks
- **Total Cost:** Sum of execution costs for all tasks
- **Fitness Score:** GA-specific metric (higher is better)
- **Convergence:** Improvement over generations

## Academic Context

This project is part of:
- **Course:** AI310 & CS361 Artificial Intelligence
- **Institution:** Helwan University, Faculty of Computing & Artificial Intelligence
- **Semester:** Fall 2025-2026

## Requirements/Deliverables

✅ A Python simulation that models cloud tasks and resource constraints  
✅ An algorithm based on GAs with clearly defined evaluation metrics  
✅ Experimental data and plots demonstrating how the model outperforms standard models  
✅ Comprehensive codebase with documentation  

## Future Enhancements

Potential improvements:
- Multi-objective optimization with Pareto front analysis
- Dynamic resource allocation (tasks arriving over time)
- Load balancing constraints
- Resource capacity limits
- More sophisticated crossover and mutation operators

## License

This project is for educational purposes.

## Authors

Developed as part of the AI310/CS361 course project requirements.

