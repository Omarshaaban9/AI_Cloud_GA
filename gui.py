"""
GUI Application for Cloud Resource Allocation
Provides user interface for input, algorithm selection, and result visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

from cloud_environment import Task, Resource, simulate
from cultural_algorithm import CulturalAlgorithm


class CloudAllocationGUI:
    """Main GUI application for cloud resource allocation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Resource Allocation System")
        self.root.geometry("1200x800")
        
        self.tasks = []
        self.resources = []
        self.results = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Input Configuration
        self.input_frame = ttk.Frame(notebook)
        notebook.add(self.input_frame, text="Input Configuration")
        self.setup_input_tab()
        
        # Tab 2: Algorithm Execution
        self.algorithm_frame = ttk.Frame(notebook)
        notebook.add(self.algorithm_frame, text="Algorithm Execution")
        self.setup_algorithm_tab()
        
        # Tab 3: Results & Visualization
        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame, text="Results & Visualization")
        self.setup_results_tab()
    
    def setup_input_tab(self):
        """Setup input configuration tab"""
        # Left panel: Tasks
        tasks_frame = ttk.LabelFrame(self.input_frame, text="Tasks Configuration", padding=10)
        tasks_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(tasks_frame, text="Number of Tasks:").pack(anchor=tk.W)
        self.num_tasks_var = tk.IntVar(value=5)
        ttk.Spinbox(tasks_frame, from_=1, to=20, textvariable=self.num_tasks_var, width=10).pack(anchor=tk.W, pady=5)
        
        ttk.Button(tasks_frame, text="Generate Random Tasks", 
                  command=self.generate_tasks).pack(pady=10)
        
        # Tasks list
        ttk.Label(tasks_frame, text="Tasks (ID, Length):").pack(anchor=tk.W, pady=(10, 5))
        self.tasks_tree = ttk.Treeview(tasks_frame, columns=("ID", "Length"), show="headings", height=10)
        self.tasks_tree.heading("ID", text="Task ID")
        self.tasks_tree.heading("Length", text="Length")
        self.tasks_tree.column("ID", width=100)
        self.tasks_tree.column("Length", width=150)
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)
        
        # Right panel: Resources
        resources_frame = ttk.LabelFrame(self.input_frame, text="Resources Configuration", padding=10)
        resources_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(resources_frame, text="Number of Resources:").pack(anchor=tk.W)
        self.num_resources_var = tk.IntVar(value=3)
        ttk.Spinbox(resources_frame, from_=1, to=10, textvariable=self.num_resources_var, width=10).pack(anchor=tk.W, pady=5)
        
        ttk.Button(resources_frame, text="Generate Random Resources", 
                  command=self.generate_resources).pack(pady=10)
        
        # Resources list
        ttk.Label(resources_frame, text="Resources (ID, Speed, Cost):").pack(anchor=tk.W, pady=(10, 5))
        self.resources_tree = ttk.Treeview(resources_frame, columns=("ID", "Speed", "Cost"), show="headings", height=10)
        self.resources_tree.heading("ID", text="Resource ID")
        self.resources_tree.heading("Speed", text="Speed")
        self.resources_tree.heading("Cost", text="Cost")
        self.resources_tree.column("ID", width=100)
        self.resources_tree.column("Speed", width=100)
        self.resources_tree.column("Cost", width=100)
        self.resources_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom panel: File operations
        file_frame = ttk.Frame(self.input_frame)
        file_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(file_frame, text="Load from JSON", command=self.load_from_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Save to JSON", command=self.save_to_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
    
    def setup_algorithm_tab(self):
        """Setup algorithm execution tab"""
        # Left panel: Algorithm selection and parameters
        config_frame = ttk.LabelFrame(self.algorithm_frame, text="Algorithm Configuration", padding=10)
        config_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Algorithm selection
        ttk.Label(config_frame, text="Algorithm:").pack(anchor=tk.W, pady=5)
        ttk.Label(config_frame, text="Cultural Algorithm", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Objective selection
        ttk.Label(config_frame, text="Objective:").pack(anchor=tk.W, pady=(10, 5))
        self.objective_var = tk.StringVar(value="cost")
        for obj in ["cost", "time", "weighted"]:
            ttk.Radiobutton(config_frame, text=obj.capitalize(), variable=self.objective_var, 
                          value=obj).pack(anchor=tk.W)
        
        # CA/GA Parameters
        params_frame = ttk.LabelFrame(config_frame, text="Algorithm Parameters", padding=5)
        params_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(params_frame, text="Population Size:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.pop_size_var = tk.IntVar(value=50)
        ttk.Spinbox(params_frame, from_=10, to=200, textvariable=self.pop_size_var, width=10).grid(row=0, column=1, pady=2)
        
        ttk.Label(params_frame, text="Max Generations:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.max_gen_var = tk.IntVar(value=100)
        ttk.Spinbox(params_frame, from_=10, to=500, textvariable=self.max_gen_var, width=10).grid(row=1, column=1, pady=2)
        
        ttk.Label(params_frame, text="Mutation Rate:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.mutation_var = tk.DoubleVar(value=0.1)
        ttk.Spinbox(params_frame, from_=0.0, to=1.0, increment=0.05, 
                   textvariable=self.mutation_var, width=10).grid(row=2, column=1, pady=2)
        
        ttk.Label(params_frame, text="Crossover Rate:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.crossover_var = tk.DoubleVar(value=0.8)
        ttk.Spinbox(params_frame, from_=0.0, to=1.0, increment=0.05, 
                   textvariable=self.crossover_var, width=10).grid(row=3, column=1, pady=2)
        
        # Execute button
        ttk.Button(config_frame, text="Run Algorithm", command=self.run_algorithm).pack(pady=20)
        
        # Right panel: Output log
        output_frame = ttk.LabelFrame(self.algorithm_frame, text="Execution Log", padding=10)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=30, width=60)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(output_frame, text="Clear Log", command=lambda: self.output_text.delete(1.0, tk.END)).pack(pady=5)
    
    def setup_results_tab(self):
        """Setup results and visualization tab"""
        # Results display
        results_display_frame = ttk.LabelFrame(self.results_frame, text="Results Summary", padding=10)
        results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_display_frame, height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Visualization frame
        viz_frame = ttk.LabelFrame(self.results_frame, text="Visualization", padding=10)
        viz_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.viz_canvas = None
        self.viz_frame = viz_frame
    
    def generate_tasks(self):
        """Generate random tasks"""
        import random
        num = self.num_tasks_var.get()
        self.tasks = [Task(i, random.randint(50, 500)) for i in range(num)]
        self.update_tasks_display()
        self.log(f"Generated {num} random tasks")
    
    def generate_resources(self):
        """Generate random resources"""
        import random
        num = self.num_resources_var.get()
        self.resources = [
            Resource(i, random.uniform(5, 30), random.uniform(3, 15)) 
            for i in range(num)
        ]
        self.update_resources_display()
        self.log(f"Generated {num} random resources")
    
    def update_tasks_display(self):
        """Update tasks treeview"""
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        for task in self.tasks:
            self.tasks_tree.insert("", tk.END, values=(task.id, task.length))
    
    def update_resources_display(self):
        """Update resources treeview"""
        for item in self.resources_tree.get_children():
            self.resources_tree.delete(item)
        for resource in self.resources:
            self.resources_tree.insert("", tk.END, values=(resource.id, f"{resource.speed:.2f}", f"{resource.cost:.2f}"))
    
    def load_from_json(self):
        """Load tasks and resources from JSON files"""
        try:
            tasks_file = filedialog.askopenfilename(title="Select Tasks JSON", filetypes=[("JSON", "*.json")])
            if tasks_file:
                with open(tasks_file, 'r') as f:
                    tasks_data = json.load(f)
                self.tasks = [Task(t['id'], t['length']) for t in tasks_data]
                self.update_tasks_display()
            
            resources_file = filedialog.askopenfilename(title="Select Resources JSON", filetypes=[("JSON", "*.json")])
            if resources_file:
                with open(resources_file, 'r') as f:
                    resources_data = json.load(f)
                self.resources = [Resource(r['id'], r['speed'], r['cost']) for r in resources_data]
                self.update_resources_display()
            
            self.log("Loaded data from JSON files")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON: {str(e)}")
    
    def save_to_json(self):
        """Save tasks and resources to JSON files"""
        try:
            tasks_file = filedialog.asksaveasfilename(title="Save Tasks JSON", defaultextension=".json", filetypes=[("JSON", "*.json")])
            if tasks_file:
                tasks_data = [{"id": t.id, "length": t.length} for t in self.tasks]
                with open(tasks_file, 'w') as f:
                    json.dump(tasks_data, f, indent=2)
            
            resources_file = filedialog.asksaveasfilename(title="Save Resources JSON", defaultextension=".json", filetypes=[("JSON", "*.json")])
            if resources_file:
                resources_data = [{"id": r.id, "speed": r.speed, "cost": r.cost} for r in self.resources]
                with open(resources_file, 'w') as f:
                    json.dump(resources_data, f, indent=2)
            
            self.log("Saved data to JSON files")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON: {str(e)}")
    
    def clear_all(self):
        """Clear all tasks and resources"""
        self.tasks = []
        self.resources = []
        self.update_tasks_display()
        self.update_resources_display()
        self.log("Cleared all data")
    
    def log(self, message):
        """Add message to output log"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def run_algorithm(self):
        """Run selected algorithm"""
        if not self.tasks or not self.resources:
            messagebox.showwarning("Warning", "Please configure tasks and resources first!")
            return
        
        objective = self.objective_var.get()
        
        self.log(f"\n{'='*60}")
        self.log(f"Running Cultural Algorithm with objective: {objective}")
        self.log(f"{'='*60}")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._run_algorithm_thread, args=(objective,))
        thread.daemon = True
        thread.start()
    
    def _run_algorithm_thread(self, objective):
        """Run algorithm in separate thread"""
        try:
            ca = CulturalAlgorithm(
                self.tasks, self.resources,
                population_size=self.pop_size_var.get(),
                max_generations=self.max_gen_var.get(),
                mutation_rate=self.mutation_var.get(),
                crossover_rate=self.crossover_var.get(),
                objective=objective
            )
            best = ca.run(verbose=False)
            stats = ca.get_statistics()
            self.results['Cultural Algorithm'] = stats
            self.log(f"\nCultural Algorithm Result:")
            self.log(f"Assignment: {stats['best_assignment']}")
            self.log(f"Total Time: {stats['best_time']:.2f}")
            self.log(f"Total Cost: {stats['best_cost']:.2f}")
            self.log(f"Best Fitness: {stats['best_fitness']:.6f}")
            
            self.update_results_display()
            self.log("\nAlgorithm execution completed!")
        
        except Exception as e:
            self.log(f"\nError: {str(e)}")
            messagebox.showerror("Error", f"Algorithm execution failed: {str(e)}")
    
    def update_results_display(self):
        """Update results display"""
        self.results_text.delete(1.0, tk.END)
        
        if not self.results:
            self.results_text.insert(tk.END, "No results yet. Run an algorithm first.")
            return
        
        self.results_text.insert(tk.END, "RESULTS SUMMARY\n")
        self.results_text.insert(tk.END, "="*60 + "\n\n")
        
        for algo_name, result in self.results.items():
            self.results_text.insert(tk.END, f"{algo_name}:\n")
            self.results_text.insert(tk.END, f"  Assignment: {result.get('assignment', result.get('best_assignment', 'N/A'))}\n")
            self.results_text.insert(tk.END, f"  Total Time: {result.get('total_time', result.get('best_time', 'N/A')):.2f}\n")
            self.results_text.insert(tk.END, f"  Total Cost: {result.get('total_cost', result.get('best_cost', 'N/A')):.2f}\n")
            if 'nodes_explored' in result:
                self.results_text.insert(tk.END, f"  Nodes Explored: {result['nodes_explored']}\n")
            self.results_text.insert(tk.END, "\n")
        
        # Update visualization
        self.update_visualization()
    
    def update_visualization(self):
        """Update visualization"""
        if not self.results:
            return
        
        # Clear previous visualization
        if self.viz_canvas:
            self.viz_canvas.get_tk_widget().destroy()
        
        # Create new figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        algorithms = list(self.results.keys())
        times = []
        costs = []
        
        for algo in algorithms:
            result = self.results[algo]
            times.append(result.get('total_time', result.get('best_time', 0)))
            costs.append(result.get('total_cost', result.get('best_cost', 0)))
        
        # Time comparison
        ax1.bar(algorithms, times, color='skyblue', edgecolor='navy', alpha=0.7)
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Total Time')
        ax1.set_title('Execution Time Comparison')
        ax1.tick_params(axis='x', rotation=45)
        
        # Cost comparison
        ax2.bar(algorithms, costs, color='lightcoral', edgecolor='darkred', alpha=0.7)
        ax2.set_xlabel('Algorithm')
        ax2.set_ylabel('Total Cost')
        ax2.set_title('Execution Cost Comparison')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Embed in tkinter
        self.viz_canvas = FigureCanvasTkAgg(fig, self.viz_frame)
        self.viz_canvas.draw()
        self.viz_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    """Main function to run GUI"""
    root = tk.Tk()
    app = CloudAllocationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

