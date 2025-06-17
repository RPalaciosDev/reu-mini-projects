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
        1. Moves to a random adjacent cell if possible
        2. Interacts with agents within their influence range (based on integrity)
        """
        # Shuffle agents to randomize order of movement and interaction
        random.shuffle(self.agents)
        
        # Move agents
        for agent in self.agents:
            proposed_move = agent.propose_move()
            self.move_agent(agent, proposed_move)
        
        # Shuffle again before interactions to ensure random order
        random.shuffle(self.agents)
        
        # Handle interactions with integrity-based range
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
                                agent.interact(other_agent)
                                break  # Found it, stop searching

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