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
        
        # Schedule-related attributes
        self.is_student = random.choice([True, False])  # Half are students, half are workers
        self.current_location = 'home'  # Current structure type
        self.target_location = 'home'   # Where they're trying to go
        self.schedule_step = 0          # Current step in their daily schedule
        
        # Assign specific structures (will be set by environment)
        self.assigned_home = None
        self.assigned_work_or_school = None
        self.assigned_leisure = None
        
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

    def propose_move(self, environment) -> Tuple[int, int]:
        """
        Propose a move toward the target location based on schedule.
        
        Args:
            environment: The environment containing structure bounds
            
        Returns:
            Tuple[int, int]: Proposed new position (x, y)
        """
        # Check if we're already in the target structure
        if self._is_in_target_structure(environment):
            return self._random_move_within_structure(environment)
        
        # Move toward target structure
        return self._move_toward_structure(environment)
    
    def _is_in_target_structure(self, environment) -> bool:
        """
        Check if the agent is currently in their target structure.
        
        Args:
            environment: The environment containing structure bounds
            
        Returns:
            bool: True if agent is in target structure
        """
        if self.target_location == 'home' and self.assigned_home:
            return self.position in self.assigned_home
        elif self.target_location in ['work', 'school'] and self.assigned_work_or_school:
            return self.position in self.assigned_work_or_school
        elif self.target_location == 'leisure' and self.assigned_leisure:
            return self.position in self.assigned_leisure
        else:
            # Fallback to environment bounds if no assignment
            if self.target_location == 'home':
                return self.position in environment.home_bounds
            elif self.target_location == 'work':
                return self.position in environment.work_bounds
            elif self.target_location == 'school':
                return self.position in environment.school_bounds
            elif self.target_location == 'leisure':
                return self.position in environment.leisure_bounds
            return True  # Default to staying put
    
    def _move_toward_structure(self, environment) -> Tuple[int, int]:
        """
        Move toward the target structure area.
        
        Args:
            environment: The environment containing structure bounds
            
        Returns:
            Tuple[int, int]: Proposed new position
        """
        # Get the bounds of the target structure (use assigned structure if available)
        bounds = None
        if self.target_location == 'home' and self.assigned_home:
            bounds = self.assigned_home
        elif self.target_location in ['work', 'school'] and self.assigned_work_or_school:
            bounds = self.assigned_work_or_school
        elif self.target_location == 'leisure' and self.assigned_leisure:
            bounds = self.assigned_leisure
        else:
            # Fallback to environment bounds
            if self.target_location == 'home':
                bounds = environment.home_bounds
            elif self.target_location == 'work':
                bounds = environment.work_bounds
            elif self.target_location == 'school':
                bounds = environment.school_bounds
            elif self.target_location == 'leisure':
                bounds = environment.leisure_bounds
        
        if not bounds:
            return self.position
        
        # Find the center of the target structure
        center_x = sum(x for x, y in bounds) // len(bounds)
        center_y = sum(y for x, y in bounds) // len(bounds)
        
        # Move toward the center of the structure
        return self._move_toward_target((center_x, center_y))
    
    def _move_toward_target(self, target_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Move toward a target position.
        
        Args:
            target_pos (Tuple[int, int]): Target position to move toward
            
        Returns:
            Tuple[int, int]: Proposed new position
        """
        x, y = self.position
        tx, ty = target_pos
        
        # Calculate direction toward target
        dx = 0
        dy = 0
        
        if x < tx:
            dx = 1
        elif x > tx:
            dx = -1
            
        if y < ty:
            dy = 1
        elif y > ty:
            dy = -1
        
        # Propose move in the direction of the target
        new_x = x + dx
        new_y = y + dy
        
        return (new_x, new_y)
    
    def _random_move_within_structure(self, environment) -> Tuple[int, int]:
        """
        Move randomly within the current structure.
        
        Args:
            environment: The environment containing structure bounds
            
        Returns:
            Tuple[int, int]: Proposed new position
        """
        # Get bounds for current target location (use assigned structure if available)
        bounds = None
        if self.target_location == 'home' and self.assigned_home:
            bounds = self.assigned_home
        elif self.target_location in ['work', 'school'] and self.assigned_work_or_school:
            bounds = self.assigned_work_or_school
        elif self.target_location == 'leisure' and self.assigned_leisure:
            bounds = self.assigned_leisure
        else:
            # Fallback to environment bounds
            if self.target_location == 'home':
                bounds = environment.home_bounds
            elif self.target_location == 'work':
                bounds = environment.work_bounds
            elif self.target_location == 'school':
                bounds = environment.school_bounds
            elif self.target_location == 'leisure':
                bounds = environment.leisure_bounds
        
        if bounds:
            # Filter out the current position to avoid staying in the same place
            available_positions = [pos for pos in bounds if pos != self.position]
            if available_positions:
                return random.choice(available_positions)
            else:
                # If no other positions available, stay put
                return self.position
        else:
            # Fallback to random adjacent move
            x, y = self.position
            possible_moves = []
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                new_x, new_y = x + dx, y + dy
                # Only add valid moves (within bounds and not current position)
                if (0 <= new_x < environment.width and 
                    0 <= new_y < environment.height and 
                    (new_x, new_y) != self.position):
                    possible_moves.append((new_x, new_y))
            
            if possible_moves:
                return random.choice(possible_moves)
            else:
                return self.position
    
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

    def update_schedule(self, step: int) -> None:
        """
        Update the agent's schedule based on the current simulation step.
        
        Args:
            step (int): Current simulation step
        """
        # Daily schedule: 120 steps per day (longer day cycle for more realistic movement)
        day_step = step % 120
        
        if self.is_student:
            # Student schedule (longer periods)
            if 10 <= day_step < 20:  # Morning: go to school
                self.target_location = 'school'
            elif 20 <= day_step < 80:  # School hours: stay at school (60 steps)
                self.target_location = 'school'
            elif 80 <= day_step < 100:  # Afternoon: go to leisure (20 steps)
                self.target_location = 'leisure'
            elif 100 <= day_step < 110:  # Evening: go home
                self.target_location = 'home'
            else:  # Night: stay home
                self.target_location = 'home'
        else:
            # Worker schedule (longer periods)
            if 10 <= day_step < 20:  # Morning: go to work
                self.target_location = 'work'
            elif 20 <= day_step < 80:  # Work hours: stay at work (60 steps)
                self.target_location = 'work'
            elif 80 <= day_step < 100:  # Afternoon: go to leisure (20 steps)
                self.target_location = 'leisure'
            elif 100 <= day_step < 110:  # Evening: go home
                self.target_location = 'home'
            else:  # Night: stay home
                self.target_location = 'home'

    def assign_structures(self, home_bounds, work_school_bounds, leisure_bounds):
        """
        Assign specific structure areas to this agent.
        
        Args:
            home_bounds: List of positions for assigned home structure
            work_school_bounds: List of positions for assigned work/school structure
            leisure_bounds: List of positions for assigned leisure structure
        """
        self.assigned_home = home_bounds
        self.assigned_work_or_school = work_school_bounds
        self.assigned_leisure = leisure_bounds 