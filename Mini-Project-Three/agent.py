from typing import Tuple
import random

class Agent:
    def __init__(self, position: Tuple[int, int], opinion: int = 0):
        """
        Initialize an agent with a position and opinion.
        
        Args:
            position (Tuple[int, int]): Initial position (x, y)
            opinion (int): Initial opinion (0, 1, or 2)
        """
        self.position = position
        self.opinion = opinion
    
    def propose_move(self) -> Tuple[int, int]:
        """
        Propose a move to a random adjacent cell.
        
        Returns:
            Tuple[int, int]: Proposed new position (x, y)
        """
        x, y = self.position
        # Get all possible adjacent positions
        possible_moves = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            possible_moves.append((nx, ny))
        
        # Return a random adjacent position
        return random.choice(possible_moves)
    
    def interact(self, other_agent: 'Agent') -> None:
        """
        Interact with another agent, potentially changing opinions.
        
        Args:
            other_agent (Agent): The agent to interact with
        """
        # If opinions are different, there's a chance they'll change
        if self.opinion != other_agent.opinion:
            # 50% chance for each agent to change their opinion
            if random.random() < 0.5:
                self.opinion = other_agent.opinion
            if random.random() < 0.5:
                other_agent.opinion = self.opinion 