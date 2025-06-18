import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
from environment import Environment
from agent import Agent

def create_environment(width: int = 100, height: int = 100, num_agents: int = 1000, high_integrity_ratio: float = 0.1) -> Environment:
    """
    Create and initialize the environment with agents.
    
    Args:
        width (int): Width of the grid
        height (int): Height of the grid
        num_agents (int): Number of agents to create
        high_integrity_ratio (float): Fraction of agents that should be high integrity (0.0 to 1.0)
        
    Returns:
        Environment: The initialized environment
    """
    env = Environment(width, height)
    
    # Calculate number of high integrity agents
    num_high_integrity = int(num_agents * high_integrity_ratio)
    num_regular_agents = num_agents - num_high_integrity
    
    # Create agents with equal distribution of opinions
    opinions_per_agent = num_regular_agents // 3
    high_integrity_per_opinion = num_high_integrity // 3
    
    # Create structure groups for assignment
    def divide_structure_into_groups(bounds, num_groups):
        """Divide structure bounds into groups for assignment."""
        if not bounds or num_groups <= 0:
            return []
        
        # Sort bounds to group nearby positions
        sorted_bounds = sorted(bounds)
        group_size = len(sorted_bounds) // num_groups
        groups = []
        
        for i in range(num_groups):
            start_idx = i * group_size
            if i == num_groups - 1:  # Last group gets remaining positions
                end_idx = len(sorted_bounds)
            else:
                end_idx = (i + 1) * group_size
            groups.append(sorted_bounds[start_idx:end_idx])
        
        return groups
    
    # Divide structures into groups
    home_groups = divide_structure_into_groups(env.home_bounds, 12)  # 12 home areas
    work_groups = divide_structure_into_groups(env.work_bounds, 6)   # 6 work areas
    school_groups = divide_structure_into_groups(env.school_bounds, 6) # 6 school areas
    leisure_groups = divide_structure_into_groups(env.leisure_bounds, 8) # 8 leisure areas
    
    all_agents = []
    
    # Create regular agents
    for i in range(3):
        for _ in range(opinions_per_agent):
            # Get a random empty cell
            empty_cells = env.get_empty_cells()
            if empty_cells:
                position = empty_cells[np.random.randint(len(empty_cells))]
                agent = Agent(position, opinion=i, is_high_integrity=False)
                all_agents.append(agent)
    
    # Create high integrity agents
    for i in range(3):
        for _ in range(high_integrity_per_opinion):
            # Get a random empty cell
            empty_cells = env.get_empty_cells()
            if empty_cells:
                position = empty_cells[np.random.randint(len(empty_cells))]
                agent = Agent(position, opinion=i, is_high_integrity=True)
                all_agents.append(agent)
    
    # Assign structures to agents
    for idx, agent in enumerate(all_agents):
        # Assign home (cycle through available home groups)
        if home_groups:
            home_group = home_groups[idx % len(home_groups)]
            agent.assigned_home = home_group
        
        # Assign work or school based on agent type
        if agent.is_student and school_groups:
            school_group = school_groups[idx % len(school_groups)]
            agent.assigned_work_or_school = school_group
        elif work_groups:
            work_group = work_groups[idx % len(work_groups)]
            agent.assigned_work_or_school = work_group
        
        # Assign leisure (cycle through available leisure groups)
        if leisure_groups:
            leisure_group = leisure_groups[idx % len(leisure_groups)]
            agent.assigned_leisure = leisure_group
        
        # Add agent to environment
        env.add_agent(agent)
    
    # Add friends to all agents after they are created
    for agent in env.agents:
        agent.add_friends(env.agents, num_friends=8)
    
    return env

def visualize_environment(env: Environment, show: bool = True) -> None:
    """
    Visualize the current state of the environment using matplotlib.
    Empty cells are white, agents are colored by their opinion.
    
    Args:
        env (Environment): The environment to visualize
        show (bool): Whether to display the plot
    """
    # Create a grid where:
    # 0 = empty (white)
    # 1-3 = different opinions (different colors)
    vis_grid = np.zeros((env.height, env.width))
    
    # Map agent positions and opinions to the visualization grid
    for agent in env.agents:
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
    plt.xticks(range(env.width))
    plt.yticks(range(env.height))
    
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

def animate_simulation(env: Environment, steps: int, interval: int = 500) -> None:
    """
    Create an animation of the simulation.
    
    Args:
        env (Environment): The environment to simulate
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
    vis_grid = np.zeros((env.height, env.width))
    for agent in env.agents:
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
    opinion_dist = env.get_opinion_distribution()
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
    ax2.set_ylim(0, len(env.agents))
    ax2.set_xlim(0, steps)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    
    # Add opinion distribution text
    opinion_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes, 
                          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Add step count text
    step_text = ax1.text(0.5, 0.02, '', transform=ax1.transAxes, 
                        horizontalalignment='center', fontsize=12, fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Add schedule information text
    schedule_text = ax1.text(0.02, 0.02, '', transform=ax1.transAxes, 
                           verticalalignment='bottom', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def update(frame):
        env.step()
        # Update grid
        vis_grid = np.zeros((env.height, env.width))
        for agent in env.agents:
            x, y = agent.position
            vis_grid[y, x] = agent.opinion + 1
        img.set_array(vis_grid)
        
        # Update opinion distribution
        opinion_dist = env.get_opinion_distribution()
        time_data.append(frame + 1)
        for i in range(3):
            opinion_data[i].append(opinion_dist.get(i, 0))
            lines[i].set_data(time_data, opinion_data[i])
        
        # Dynamically rescale y-axis based on current data
        all_values = []
        for i in range(3):
            all_values.extend(opinion_data[i])
        
        if all_values:  # Only rescale if we have data
            min_val = min(all_values)
            max_val = max(all_values)
            margin = (max_val - min_val) * 0.1  # 10% margin
            if margin == 0:  # If all values are the same
                margin = 1
            ax2.set_ylim(max(0, min_val - margin), max_val + margin)
        
        # Update opinion text
        opinion_text.set_text('\n'.join([f'Opinion {k}: {v} agents' 
                                       for k, v in sorted(opinion_dist.items())]))
        
        # Update step count text
        step_text.set_text(f'Step {frame + 1}/{steps}')
        
        # Update schedule information
        day_step = frame % 120  # Updated to match new day cycle
        day_number = frame // 120 + 1  # Which day we're on
        # Convert to 24-hour format (120 steps = 24 hours, so 1 step = 0.2 hours = 12 minutes)
        hour = int((day_step / 120) * 24)
        minute = int(((day_step / 120) * 24 - hour) * 60)
        time_str = f"Day {day_number}, {hour:02d}:{minute:02d}"
        
        # Count agents in each location
        location_counts = {'home': 0, 'work': 0, 'school': 0, 'leisure': 0}
        for agent in env.agents:
            location_counts[agent.target_location] += 1
        
        schedule_info = f"Time: {time_str}\n"
        schedule_info += f"Step: {day_step}/120\n"
        schedule_info += f"Home: {location_counts['home']}\n"
        schedule_info += f"Work: {location_counts['work']}\n"
        schedule_info += f"School: {location_counts['school']}\n"
        schedule_info += f"Leisure: {location_counts['leisure']}"
        schedule_text.set_text(schedule_info)
        
        # Stop animation if we've reached the last frame
        if frame >= steps - 1:
            anim.event_source.stop()
        
        return [img, opinion_text, step_text, schedule_text] + lines
    
    anim = animation.FuncAnimation(fig, update, frames=steps, interval=interval, blit=True)
    
    plt.show()

def main():
    # Create and initialize the environment
    env = create_environment(width=100, height=100, num_agents=1200, high_integrity_ratio=0.1)
    
    # Run the simulation with animation (500 steps = ~4 full days)
    animate_simulation(env, steps=500, interval=50)

if __name__ == "__main__":
    main() 