from typing import Tuple, List
import random

class Agent:
    def __init__(self, position: Tuple[int, int], opinion: int = 0, is_high_integrity: bool = False):
        """
        Initialize an agent with a position, opinion, and integrity.
        
        Args:
            position (Tuple[int, int]): Initial position (x, y)
            opinion (int): Initial opinion (0, 1, or 2)
            is_high_integrity (bool): Whether this agent has fixed high integrity
        """
        self.position = position
        self.opinion = opinion
        self.is_high_integrity = is_high_integrity
        self.friends: List['Agent'] = []  # List of friend agents
        
        # Set integrity based on agent type
        if is_high_integrity:
            self.integrity = 1.0  # 100% integrity, never changes
        else:
            self.integrity = random.uniform(0.3, 0.7)  # Random initial integrity
    
    def add_friend(self, friend: 'Agent') -> None:
        """
        Add a friend to this agent's social circle.
        
        Args:
            friend (Agent): The agent to add as a friend
        """
        if friend not in self.friends and friend != self:
            self.friends.append(friend)
            # Make it bidirectional
            if self not in friend.friends:
                friend.friends.append(self)
    
    def remove_friend(self, friend: 'Agent') -> None:
        """
        Remove a friend from this agent's social circle.
        
        Args:
            friend (Agent): The agent to remove as a friend
        """
        if friend in self.friends:
            self.friends.remove(friend)
            # Make it bidirectional
            if self in friend.friends:
                friend.friends.remove(self)
    
    def add_friends(self, all_agents: List['Agent'], num_friends: int = 8) -> None:
        """
        Add friends to this agent with the same opinion.
        
        Args:
            all_agents (List[Agent]): All agents in the simulation
            num_friends (int): Maximum number of friends to add
        """
        # Filter out self and existing friends, and only include agents with same opinion
        available_agents = [agent for agent in all_agents 
                          if agent != self and agent not in self.friends and agent.opinion == self.opinion]
        
        # Add friends (all will have same opinion)
        friends_added = 0
        while friends_added < num_friends and available_agents:
            # Pick a random agent with same opinion
            friend = random.choice(available_agents)
            available_agents.remove(friend)
            
            # Add friend (bidirectional)
            self.add_friend(friend)
            friends_added += 1

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
    
    def interact(self, other_agent: 'Agent', is_friend_interaction: bool = False) -> None:
        """
        Interact with another agent, potentially changing opinions and integrity.
        
        Args:
            other_agent (Agent): The agent to interact with
            is_friend_interaction (bool): Whether this is a friend interaction (reduced effect)
        """
        # Determine if this is a positive or negative interaction (70% positive, 30% negative)
        is_positive = random.random() < 0.7
        
        # Determine if agents have the same opinion
        same_opinion = (self.opinion == other_agent.opinion)
        
        # Update integrity based on interaction type
        # High integrity agents can influence others but don't change their own integrity
        if not self.is_high_integrity:
            self._update_integrity(same_opinion, is_positive, is_friend_interaction)
        
        if not other_agent.is_high_integrity:
            other_agent._update_integrity(same_opinion, is_positive, is_friend_interaction)
        
        # Check if opinions should change based on integrity
        # High integrity agents can influence others but don't change their own opinions
        if not self.is_high_integrity:
            self._maybe_change_opinion(other_agent, is_friend_interaction)
        
        if not other_agent.is_high_integrity:
            other_agent._maybe_change_opinion(self, is_friend_interaction)
    
    def _update_integrity(self, same_opinion: bool, is_positive: bool, is_friend_interaction: bool = False) -> None:
        """
        Update agent's integrity based on interaction type.
        
        Args:
            same_opinion (bool): Whether the interaction was with same opinion
            is_positive (bool): Whether the interaction was positive
            is_friend_interaction (bool): Whether this is a friend interaction (reduced effect)
        """
        if self.is_high_integrity:
            return  # High integrity agents don't change integrity
        
        # Define base influence strength
        INFLUENCE_STRENGTH = 0.1
        
        # Reduce effect for friend interactions (1/16th of normal effect)
        if is_friend_interaction:
            INFLUENCE_STRENGTH *= 0.0625
        
        # Calculate change based on interaction type
        if same_opinion and is_positive:
            # Positive interaction with same opinion → increase integrity
            # Higher integrity agents are more influential
            change = INFLUENCE_STRENGTH * (1.0 - self.integrity)
            self.integrity = min(1.0, self.integrity + change)
        elif not same_opinion and is_positive:
            # Positive interaction with different opinion → decrease integrity
            change = INFLUENCE_STRENGTH * self.integrity
            self.integrity = max(0.0, self.integrity - change)
        elif same_opinion and not is_positive:
            # Negative interaction with same opinion → decrease integrity
            change = INFLUENCE_STRENGTH * self.integrity
            self.integrity = max(0.0, self.integrity - change)
        elif not same_opinion and not is_positive:
            # Negative interaction with different opinion → increase integrity
            change = INFLUENCE_STRENGTH * (1.0 - self.integrity)
            self.integrity = min(1.0, self.integrity + change)
    
    def _maybe_change_opinion(self, other_agent: 'Agent', is_friend_interaction: bool = False) -> None:
        """
        Maybe change opinion based on integrity level and other agent's influence.
        
        Args:
            other_agent (Agent): The agent that might influence this one
            is_friend_interaction (bool): Whether this is a friend interaction (reduced effect)
        """
        if self.is_high_integrity:
            return  # High integrity agents never change opinions
        
        # Calculate change probability based on:
        # 1. This agent's susceptibility (1.0 - integrity)
        # 2. Other agent's influence strength (integrity)
        susceptibility = 1.0 - self.integrity
        influence_strength = other_agent.integrity
        change_probability = susceptibility * influence_strength * 0.5  # Scale factor
        
        # Reduce effect for friend interactions (1/16th of normal effect)
        if is_friend_interaction:
            change_probability *= 0.0625
        
        if random.random() < change_probability:
            self.opinion = other_agent.opinion 