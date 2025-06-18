import numpy as np
from typing import List, Tuple
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
from agent import Agent

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
        self.step_count = 0  # Track simulation steps
        
        # Define structure bounds
        self.home_bounds = []
        self.work_bounds = []
        self.school_bounds = []
        self.leisure_bounds = []
        
        # Set up structure bounds
        self._setup_structure_bounds()
        
    def _setup_structure_bounds(self):
        """Set up the bounds for different structure types distributed across the grid."""
        # Clear existing bounds
        self.home_bounds = []
        self.work_bounds = []
        self.school_bounds = []
        self.leisure_bounds = []
        
        # Define structure size (larger structures for better visibility)
        structure_size = 12
        spacing = 4  # Space between structures
        
        # HOME STRUCTURES - Top half of the grid
        home_positions = [
            (10, 10), (35, 8), (60, 12), (85, 10),      # Top row
            (15, 30), (45, 28), (75, 32), (90, 35),     # Second row
            (5, 50), (30, 48), (55, 52), (80, 50)       # Third row
        ]
        
        for center_x, center_y in home_positions:
            if center_x + structure_size//2 < self.width and center_y + structure_size//2 < self.height:
                start_x = max(0, center_x - structure_size//2)
                start_y = max(0, center_y - structure_size//2)
                
                for x in range(start_x, min(start_x + structure_size, self.width)):
                    for y in range(start_y, min(start_y + structure_size, self.height)):
                        self.home_bounds.append((x, y))
        
        # WORK STRUCTURES - Bottom left quarter
        work_positions = [
            (15, 70), (40, 75), (20, 90),               # Concentrated in bottom left
            (45, 85), (10, 85), (35, 65)
        ]
        
        for center_x, center_y in work_positions:
            if center_x + structure_size//2 < self.width and center_y + structure_size//2 < self.height:
                start_x = max(0, center_x - structure_size//2)
                start_y = max(0, center_y - structure_size//2)
                
                for x in range(start_x, min(start_x + structure_size, self.width)):
                    for y in range(start_y, min(start_y + structure_size, self.height)):
                        self.work_bounds.append((x, y))
        
        # SCHOOL STRUCTURES - Bottom right quarter  
        school_positions = [
            (65, 70), (85, 75), (70, 90),               # Concentrated in bottom right
            (90, 85), (55, 85), (80, 65)
        ]
        
        for center_x, center_y in school_positions:
            if center_x + structure_size//2 < self.width and center_y + structure_size//2 < self.height:
                start_x = max(0, center_x - structure_size//2)
                start_y = max(0, center_y - structure_size//2)
                
                for x in range(start_x, min(start_x + structure_size, self.width)):
                    for y in range(start_y, min(start_y + structure_size, self.height)):
                        self.school_bounds.append((x, y))
        
        # LEISURE STRUCTURES - Scattered throughout but avoiding residential areas
        leisure_size = 8  # Smaller leisure structures
        leisure_positions = [
            (25, 65),   # Between work and home areas
            (75, 45),   # Right side, between home and school
            (50, 75),   # Center bottom
            (20, 40),   # Left side
            (85, 40),   # Right side
            (50, 20),   # Center top
            (10, 65),   # Far left
            (90, 65),   # Far right
        ]
        
        for center_x, center_y in leisure_positions:
            if center_x + leisure_size//2 < self.width and center_y + leisure_size//2 < self.height:
                start_x = max(0, center_x - leisure_size//2)
                start_y = max(0, center_y - leisure_size//2)
                
                for x in range(start_x, min(start_x + leisure_size, self.width)):
                    for y in range(start_y, min(start_y + leisure_size, self.height)):
                        self.leisure_bounds.append((x, y))
    
    def add_agent(self, agent: Agent) -> bool:
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
    
    def remove_agent(self, agent: Agent) -> None:
        """
        Remove an agent from the environment.
        
        Args:
            agent (Agent): The agent to remove
        """
        if agent in self.agents:
            x, y = agent.position
            self.grid[y, x] = 0  # Mark cell as empty
            self.agents.remove(agent)
    
    def validate_move(self, agent, new_position: Tuple[int, int]) -> bool:
        """
        Validate if a move is possible.
        
        Args:
            agent: The agent trying to move
            new_position (Tuple[int, int]): Proposed new position (x, y)
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        x, y = new_position
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.grid[y, x] == 0)
    
    def move_agent(self, agent: Agent, new_position: Tuple[int, int]) -> bool:
        """
        Move an agent to a new position if the move is valid.
        
        Args:
            agent (Agent): The agent to move
            new_position (Tuple[int, int]): New position (x, y)
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if self.validate_move(agent, new_position):
            old_x, old_y = agent.position
            x, y = new_position
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
        1. Updates their schedule based on current step
        2. Moves toward their target location based on schedule
        3. Interacts with a subset of their friends (reduced effect)
        4. Interacts with agents within their influence range (based on integrity)
        """
        # Shuffle agents to randomize order of movement and interaction
        random.shuffle(self.agents)
        
        # Update schedules and move agents
        for agent in self.agents:
            agent.update_schedule(self.step_count)
            proposed_move = agent.propose_move(self)
            self.move_agent(agent, proposed_move)
        
        # Shuffle again before interactions to ensure random order
        random.shuffle(self.agents)
        
        # Handle friend interactions (each agent interacts with 1-3 random friends)
        for agent in self.agents:
            if agent.friends:
                # Pick 1-3 random friends to interact with this step
                num_friend_interactions = random.randint(1, min(3, len(agent.friends)))
                friends_to_interact_with = random.sample(agent.friends, num_friend_interactions)
                for friend in friends_to_interact_with:
                    agent.interact(friend, is_friend_interaction=True)
        
        # Shuffle again before spatial interactions
        random.shuffle(self.agents)
        
        # Handle spatial interactions with integrity-based range
        for agent in self.agents:
            x, y = agent.position
            
            # Calculate interaction range based on integrity (0-3 cells)
            max_range = min(3, int(agent.integrity * 3))
            
            # Check all cells within the agent's influence range
            for dx in range(-max_range, max_range + 1):
                for dy in range(-max_range, max_range + 1):
                    # Skip the agent's own cell
                    if dx == 0 and dy == 0:
                        continue
                    
                    nx, ny = x + dx, y + dy
                    
                    # Check if the cell is within grid bounds and occupied
                    if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny, nx] == 1:
                        # Find the agent at this position (much faster with grid lookup)
                        for other_agent in self.agents:
                            if other_agent.position == (nx, ny):
                                agent.interact(other_agent, is_friend_interaction=False)
                                break  # Found it, stop searching
        
        # Increment step counter
        self.step_count += 1

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