import numpy as np
from typing import List, Tuple, Optional
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation

class Environment:
    def __init__(self, width: int = 100, height: int = 100):
        """
        Initialize the grid environment.
        
        Args:
            width (int): Width of the grid
            height (int): Height of the grid
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # Initialize with 0's to represent empty cell
        self.agents: List[Agent] = []
        
    def add_agent(self, agent: 'Agent') -> bool:
        """
        Add an agent to the environment at its current position.
        
        Args:
            agent (Agent): The agent to add
            
        Returns:
            bool: True if agent was successfully added, False otherwise
        """
        x, y = agent.position
        if 0 <= x < self.width and 0 <= y < self.height and self.grid[y, x] == 0:
            self.grid[y, x] = 1  # Mark cell as occupied
            self.agents.append(agent)
            return True
        return False
    
    def remove_agent(self, agent: 'Agent') -> None:
        """
        Remove an agent from the environment.
        
        Args:
            agent (Agent): The agent to remove
        """
        if agent in self.agents:
            x, y = agent.position
            self.grid[y, x] = 0  # Mark cell as empty
            self.agents.remove(agent)
    
    def move_agent(self, agent: 'Agent', new_position: Tuple[int, int]) -> bool:
        """
        Move an agent to a new position if the cell is empty.
        
        Args:
            agent (Agent): The agent to move
            new_position (Tuple[int, int]): New position (x, y)
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        x, y = new_position
        if 0 <= x < self.width and 0 <= y < self.height and self.grid[y, x] == 0:
            old_x, old_y = agent.position
            self.grid[old_y, old_x] = 0  # Clear old position
            self.grid[y, x] = 1  # Mark new position as occupied
            agent.position = new_position
            return True
        return False
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get a list of all empty cell positions.
        
        Returns:
            List[Tuple[int, int]]: List of (x, y) coordinates of empty cells
        """
        return [(x, y) for y in range(self.height) for x in range(self.width) 
                if self.grid[y, x] == 0]

    def step(self) -> None:
        """
        Run one step of the simulation where each agent:
        1. Moves to a random adjacent cell if possible
        2. Interacts with any agents in adjacent cells
        """
        # Shuffle agents to randomize order of movement and interaction
        random.shuffle(self.agents)
        
        # Move agents
        for agent in self.agents:
            agent.move(self)
        
        # Shuffle again before interactions to ensure random order
        random.shuffle(self.agents)
        
        # Handle interactions
        for agent in self.agents:
            x, y = agent.position
            # Check adjacent cells for other agents
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Find any agent at this position
                    for other_agent in self.agents:
                        if other_agent.position == (nx, ny):
                            agent.interact(other_agent)

    def get_opinion_distribution(self) -> dict:
        """
        Get the current distribution of opinions among agents.
        
        Returns:
            dict: Dictionary mapping opinions to counts
        """
        opinion_counts = {}
        for agent in self.agents:
            opinion_counts[agent.opinion] = opinion_counts.get(agent.opinion, 0) + 1
        return opinion_counts

    def visualize(self, show: bool = True) -> None:
        """
        Visualize the current state of the environment using matplotlib.
        Empty cells are white, agents are colored by their opinion.
        """
        # Create a grid where:
        # 0 = empty (white)
        # 1-3 = different opinions (different colors)
        vis_grid = np.zeros((self.height, self.width))
        
        # Map agent positions and opinions to the visualization grid
        for agent in self.agents:
            x, y = agent.position
            vis_grid[y, x] = agent.opinion + 1  # +1 because 0 is reserved for empty cells
        
        # Create custom colormap
        colors = ['white', 'red', 'blue', 'green']  # white for empty, then colors for opinions
        max_opinion = int(vis_grid.max())  # Convert to int for indexing
        cmap = ListedColormap(colors[:max_opinion + 1])
        
        # Create the plot
        plt.figure(figsize=(10, 10))
        plt.imshow(vis_grid, cmap=cmap, vmin=0, vmax=len(colors)-1)
        plt.grid(True, which='both', color='black', linewidth=0.5)
        plt.xticks(range(self.width))
        plt.yticks(range(self.height))
        
        # Add a legend
        legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', label='Empty')]
        for i, color in enumerate(colors[1:], 1):
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, facecolor=color, 
                                               label=f'Opinion {i-1}'))
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.title('Environment State')
        if show:
            plt.show()
        plt.close()

    def animate_simulation(self, steps: int, interval: int = 500) -> None:
        """
        Create an animation of the simulation.
        
        Args:
            steps (int): Number of steps to simulate
            interval (int): Time between frames in milliseconds
        """
        # Create figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), 
                                      gridspec_kw={'width_ratios': [2, 1]})
        
        # Create custom colormap
        colors = ['white', 'red', 'blue', 'green']
        cmap = ListedColormap(colors)
        
        # Initialize the grid plot
        vis_grid = np.zeros((self.height, self.width))
        for agent in self.agents:
            x, y = agent.position
            vis_grid[y, x] = agent.opinion + 1
        
        img = ax1.imshow(vis_grid, cmap=cmap, vmin=0, vmax=len(colors)-1)
        ax1.grid(True, which='both', color='black', linewidth=0.5)
        # Remove tick marks and labels
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.set_title('Agent Positions')
        
        # Add legend to grid plot
        legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', label='Empty')]
        for i, color in enumerate(colors[1:], 1):
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, facecolor=color, 
                                               label=f'Opinion {i-1}'))
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # Initialize the time series plot
        opinion_dist = self.get_opinion_distribution()
        time_data = [0]  # Time points
        opinion_data = {0: [opinion_dist.get(0, 0)],  # Opinion 0 counts
                       1: [opinion_dist.get(1, 0)],  # Opinion 1 counts
                       2: [opinion_dist.get(2, 0)]}  # Opinion 2 counts
        
        # Create lines for each opinion
        lines = []
        for i in range(3):
            line, = ax2.plot(time_data, opinion_data[i], color=colors[i+1], 
                           label=f'Opinion {i}', linewidth=2)
            lines.append(line)
        
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Number of Agents')
        ax2.set_title('Opinion Distribution Over Time')
        ax2.set_ylim(0, len(self.agents))
        ax2.set_xlim(0, steps)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # Add opinion distribution text
        opinion_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, 
                              verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        def update(frame):
            self.step()
            # Update grid
            vis_grid = np.zeros((self.height, self.width))
            for agent in self.agents:
                x, y = agent.position
                vis_grid[y, x] = agent.opinion + 1
            img.set_array(vis_grid)
            
            # Update opinion distribution
            opinion_dist = self.get_opinion_distribution()
            time_data.append(frame + 1)
            for i in range(3):
                opinion_data[i].append(opinion_dist.get(i, 0))
                lines[i].set_data(time_data, opinion_data[i])
            
            # Update opinion text
            opinion_text.set_text('\n'.join([f'Opinion {k}: {v} agents' 
                                           for k, v in sorted(opinion_dist.items())]))
            
            # Update the figure title
            plt.suptitle(f'Step {frame + 1}/{steps}', y=0.95, fontsize=12, fontweight='bold')
            
            # Stop animation if we've reached the last frame
            if frame >= steps - 1:
                anim.event_source.stop()
            
            return [img, opinion_text] + lines
        
        # Adjust figure layout
        plt.subplots_adjust(top=0.9, wspace=0.3)
        
        anim = animation.FuncAnimation(fig, update, frames=steps, 
                                     interval=interval, blit=False)
        plt.show()
        plt.close()

class Agent:
    def __init__(self, position: Tuple[int, int], opinion: int = 0):
        """
        Initialize an agent.
        
        Args:
            position (Tuple[int, int]): Initial position (x, y)
            opinion (int): Initial opinion (default: 0)
        """
        self.position = position
        self.opinion = opinion
        self.influence_strength = random.uniform(0.5, 1.0)  # Random influence strength
        self.openness = random.uniform(0.1, 0.9)  # Random openness to new opinions
    
    def move(self, environment: Environment) -> bool:
        """
        Move the agent to a random adjacent empty cell.
        
        Args:
            environment (Environment): The environment to move in
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        x, y = self.position
        possible_moves = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1)
        ]
        random.shuffle(possible_moves)
        
        for new_pos in possible_moves:
            if environment.move_agent(self, new_pos):
                return True
        return False
    
    def interact(self, other_agent: 'Agent') -> None:
        """
        Interact with another agent and potentially influence their opinion.
        The probability of opinion change is determined by:
        - This agent's influence_strength (how persuasive they are)
        - The other agent's openness (how willing they are to change)
        
        Args:
            other_agent (Agent): The agent to interact with
        """
        if random.random() < self.influence_strength * other_agent.openness:
            other_agent.opinion = self.opinion

# Example usage
if __name__ == "__main__":
    # Create environment
    env = Environment(width=100, height=100)  # Full size grid
    
    # Create agents with equal distribution of opinions
    agents_per_opinion = 500 // 3  # Divide total agents by number of opinions
    
    # Create all agents first, then assign positions randomly
    all_agents = []
    for opinion in range(3):  # For each opinion (0, 1, 2)
        for _ in range(agents_per_opinion):
            agent = Agent(position=(0, 0), opinion=opinion)  # Temporary position
            all_agents.append(agent)
    
    # Shuffle agents to randomize order
    random.shuffle(all_agents)
    
    # Assign positions randomly
    empty_cells = env.get_empty_cells()
    for agent in all_agents:
        if empty_cells:
            pos = random.choice(empty_cells)
            empty_cells.remove(pos)  # Remove used position
            agent.position = pos
            env.add_agent(agent)
    
    # Print initial state
    print("Initial state:")
    print(f"Number of agents: {len(env.agents)}")
    print("Initial opinion distribution:", env.get_opinion_distribution())
    
    # Run and animate simulation
    print("\nRunning animated simulation for 100 steps...")
    env.animate_simulation(steps=100, interval=100)  # 100ms between frames
    
    # Print final state
    print("\nFinal state:")
    print("Final opinion distribution:", env.get_opinion_distribution())
