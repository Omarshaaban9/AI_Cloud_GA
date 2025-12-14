"""
Cloud Environment Model
Defines Task and Resource classes and simulation function
"""


class Task:
    """Represents a computing task with a specific length/requirement"""
    
    def __init__(self, task_id, length):
        self.id = task_id
        self.length = length


class Resource:
    """Represents a cloud computing resource with speed and cost"""
    
    def __init__(self, resource_id, speed, cost):
        """
        Args:
            resource_id: Unique identifier for the resource
            speed: Processing speed (units per time)
            cost: Cost per unit time
        """
        self.id = resource_id
        self.speed = speed
        self.cost = cost


def simulate(tasks, resources, assignment):
    """
    Simulate execution of tasks on resources based on assignment
    
    Args:
        tasks: List of Task objects
        resources: List of Resource objects
        assignment: List of resource indices, one per task 
                    (assignment[i] = resource index for task at position i in tasks list)
    
    Returns:
        Dictionary with 'total_time' and 'total_cost'
    """
    total_time = 0
    total_cost = 0
    
    # Create a mapping from task.id to task index for robustness
    task_id_to_index = {task.id: idx for idx, task in enumerate(tasks)}
    
    for task in tasks:
        task_index = task_id_to_index[task.id]
        resource = resources[assignment[task_index]]
        execution_time = task.length / resource.speed
        execution_cost = execution_time * resource.cost
        
        total_time += execution_time
        total_cost += execution_cost
    
    return {
        "total_time": total_time,
        "total_cost": total_cost
    }


if __name__ == "__main__":
    # Example usage
    tasks = [
        Task(0, 120),
        Task(1, 200),
        Task(2, 150)
    ]
    
    resources = [
        Resource(0, 10, 5),
        Resource(1, 20, 8)
    ]
    
    assignment = [0, 1, 0]
    
    result = simulate(tasks, resources, assignment)
    print("Simulation Result:", result)
