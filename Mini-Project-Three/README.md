# Agentic Opinion Spread Simulation

An agent-based model for studying opinion dynamics and information spread in social networks, featuring spatial interactions, integrity-based influence, and dynamic opinion evolution.

## 🎯 Overview

This project simulates how opinions spread through a population of agents with varying levels of integrity. Agents move randomly on a 2D grid, interact with neighbors and friends, and can change their opinions based on these interactions. The model incorporates concepts from social psychology and network theory to explore how information spreads through communities.

## 🔑 Key Features

- **Agent-Based Modeling**: Individual agents with unique positions, opinions, and integrity levels
- **Spatial Interactions**: Agents interact with nearby neighbors based on their integrity-determined range
- **Social Networks**: Friendship connections between agents with similar initial opinions
- **Dynamic Opinion Evolution**: Opinions can change based on interactions and integrity levels
- **High-Integrity Influencers**: Special agents that influence others but remain unchanged themselves
- **Real-Time Visualization**: Animated simulation with live opinion distribution tracking
- **Mathematical Foundation**: Rigorous mathematical model with detailed parameter specifications

## 📁 Project Structure

```
Mini-Project-Three/
├── README.md                          # This file
├── main.py                           # Main simulation runner and visualization
├── agent.py                          # Agent class with behavior logic
├── environment.py                    # Environment class managing the grid world
├── mathematical_model.md             # Detailed mathematical formulation
├── Agentic_Opinion_Spread.ipynb     # Jupyter notebook for interactive exploration
├── simulation-basic.gif             # Example simulation output (basic version)
└── simulation-full-agent.gif        # Example simulation output (full version)
```

## 🚀 Quick Start

### Prerequisites

```bash
pip install numpy matplotlib
```

### Running the Simulation

```bash
cd Mini-Project-Three
python main.py
```

This will launch an animated visualization showing:

- **Left Panel**: Grid visualization with agents colored by opinion (Red, Blue, Green)
- **Right Panel**: Real-time plot of opinion distribution over time
- **Status Information**: Current step count and opinion statistics

## 🧠 Model Components

### Agents

Each agent has the following properties:

- **Position**: (x, y) coordinates on the grid
- **Opinion**: Integer value (0, 1, or 2) representing different viewpoints
- **Integrity**: Float value [0.0, 1.0] representing resistance to opinion change
- **Type**: Regular agent (can change) or High-Integrity agent (fixed)
- **Friends**: List of connected agents with similar initial opinions

### Agent Types

1. **Regular Agents** (90% of population):
   - Initial integrity: Random value between 0.3-0.7
   - Can change opinions and integrity based on interactions
   - Form friendships with agents of the same initial opinion

2. **High-Integrity Agents** (10% of population):
   - Fixed integrity: 1.0 (maximum)
   - Never change their opinions or integrity
   - Can influence other agents but remain unchanged themselves
   - Act as "opinion anchors" in the simulation

### Interaction Mechanisms

#### Spatial Interactions

- Agents interact with others within their integrity-based range (0-3 cells)
- Higher integrity agents have larger influence ranges
- 70% of interactions are positive, 30% are negative

#### Friend Interactions

- Each agent has up to 8 friends with the same initial opinion
- Friend interactions occur with reduced effect strength (1/16th of spatial interactions)
- 1-3 random friends are selected for interaction each step

#### Opinion Change Rules

- Probability of opinion change depends on:
  - Agent's susceptibility (1 - integrity)
  - Influencing agent's strength (integrity)
  - Interaction type (friend vs. spatial)

## 📊 Simulation Parameters

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| Grid Size | 50×50 | Simulation world dimensions |
| Agent Count | 1000 | Total number of agents |
| High-Integrity Ratio | 10% | Fraction of fixed-opinion agents |
| Simulation Steps | 400 | Number of time steps to run |
| Friend Count | 8 | Maximum friends per agent |
| Interaction Range | 0-3 cells | Based on agent integrity |
| Positive Interaction Rate | 70% | Probability of positive interactions |

## 🎮 Customization

### Modifying Parameters

Edit the `main()` function in `main.py`:

```python
def main():
    # Customize these parameters
    env = create_environment(
        width=100,              # Grid width
        height=100,             # Grid height
        num_agents=1200,        # Number of agents
        high_integrity_ratio=0.15  # 15% high-integrity agents
    )
    
    # Customize animation
    animate_simulation(
        env, 
        steps=500,              # Simulation length
        interval=50             # Animation speed (ms)
    )
```

### Agent Behavior

Modify `agent.py` to change:

- Movement patterns (`propose_move` method)
- Interaction effects (`interact` method)
- Friendship formation (`add_friends` method)

### Environment Rules

Modify `environment.py` to change:

- Grid topology
- Interaction scheduling
- Spatial constraints

## 📈 Expected Behaviors

The simulation typically exhibits several interesting phenomena:

1. **Opinion Clustering**: Agents with similar opinions tend to cluster spatially
2. **Influence Cascades**: High-integrity agents can cause opinion changes that propagate
3. **Stability vs. Change**: Balance between friend reinforcement and spatial influence
4. **Emergent Patterns**: Complex dynamics arising from simple local rules

## 🔬 Research Applications

This model is suitable for studying:

- **Social Media Dynamics**: How opinions spread through online networks
- **Political Polarization**: Formation of opinion clusters and echo chambers
- **Information Warfare**: Impact of influential agents on public opinion
- **Community Resilience**: How communities maintain or change beliefs over time
- **Network Effects**: Role of social connections in opinion formation

## 📚 Mathematical Foundation

The simulation is based on a rigorous mathematical model detailed in `mathematical_model.md`. Key equations include:

- **Integrity Update**: `Δφᵢ(t) = α · f(same-opinion, quality, φᵢ) · γ`
- **Opinion Change Probability**: `P(change) = β · (1-φᵢ) · φⱼ · γ`
- **Interaction Range**: `R = min(3, floor(3φᵢ))`

Where α, β are influence parameters and γ is the friend interaction reduction factor.

## 🎨 Visualization Features

The animation provides:

- **Color-coded Agents**: Red (Opinion 0), Blue (Opinion 1), Green (Opinion 2)
- **Real-time Statistics**: Live count of agents per opinion
- **Dynamic Plots**: Opinion distribution evolution over time
- **Step Counter**: Current simulation progress
- **Auto-scaling**: Automatic adjustment of plot ranges

## 🔧 Technical Details

### Performance Considerations

- Grid-based spatial lookup for efficient neighbor finding
- Randomized interaction order to prevent systematic biases
- Optimized visualization with matplotlib's blitting
- Memory-efficient agent storage and movement tracking

### File Dependencies

```
main.py → environment.py, agent.py
environment.py → agent.py
agent.py → (no dependencies)
```

## 🤝 Contributing

To extend this project:

1. **Add New Agent Types**: Implement different behavior patterns
2. **Modify Interaction Rules**: Experiment with different influence mechanisms
3. **Enhance Visualization**: Add new plots or interactive features
4. **Export Capabilities**: Add data logging or animation export
5. **Parameter Studies**: Implement systematic parameter sweeps

## 📄 License

This project is part of an academic research effort. Please cite appropriately if used in academic work.

## 🙋 Support

For questions about the model or implementation, refer to:

- `mathematical_model.md` for theoretical details
- `Agentic_Opinion_Spread.ipynb` for interactive exploration
- Code comments for implementation specifics

---

**Note**: This simulation is designed for research and educational purposes. Real-world opinion dynamics involve many additional factors not captured in this simplified model.
