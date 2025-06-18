# Mathematical Model for Agent Interaction Scheme

## **1. Agent State Representation**

For each agent $i$ at time $t$:

- **Position**: $\vec{x}_i(t) = (x_i(t), y_i(t)) \in \mathbb{Z}^2$
- **Opinion**: $o_i(t) \in \{0, 1, 2\}$
- **Integrity**: $\phi_i(t) \in [0, 1]$
- **Type**: $\tau_i \in \{\text{regular}, \text{high-integrity}\}$
- **Agent Role**: $\rho_i \in \{\text{student}, \text{worker}\}$
- **Friends**: $\mathcal{F}_i \subseteq \{1, 2, \ldots, N\}$ (set of friend agent indices)
- **Assigned Structures**: $\{\mathcal{H}_i, \mathcal{W}_i, \mathcal{L}_i\}$ (home, work/school, leisure)
- **Target Location**: $\ell_i(t) \in \{\text{home}, \text{work}, \text{school}, \text{leisure}\}$

## **2. Initial Conditions**

### **High Integrity Agents** ($\tau_i = \text{high-integrity}$)

$$\phi_i(0) = 1.0, \quad \phi_i(t) = 1.0 \quad \forall t > 0$$

### **Regular Agents** ($\tau_i = \text{regular}$)

$$\phi_i(0) \sim \text{Uniform}(0.3, 0.7)$$

### **Agent Role Assignment**

$$\rho_i \sim \text{Bernoulli}(0.5) \quad \text{where } \rho_i = 1 \Rightarrow \text{student}, \rho_i = 0 \Rightarrow \text{worker}$$

### **Friend Network Initialization**

For each agent $i$, friends are selected such that:

- $|\mathcal{F}_i| \leq 8$ (maximum 8 friends)
- $j \in \mathcal{F}_i \implies o_i(0) = o_j(0)$ (same opinion requirement)
- $j \in \mathcal{F}_i \implies i \in \mathcal{F}_j$ (bidirectional friendships)

### **Structure Assignment**

Agents are assigned to structure groups using modular arithmetic:

- $\mathcal{H}_i = \text{home\_groups}[i \bmod |\text{home\_groups}|]$
- $\mathcal{W}_i = \text{work\_groups}[i \bmod |\text{work\_groups}|]$ or $\text{school\_groups}[i \bmod |\text{school\_groups}|]$
- $\mathcal{L}_i = \text{leisure\_groups}[i \bmod |\text{leisure\_groups}|]$

## **3. Movement Dynamics**

### **Schedule-Based Target Location**

For each agent $i$ at time $t$, the target location is determined by:

$$\ell_i(t) = \begin{cases}
\text{home} & \text{if } t \bmod 120 \in [0, 10) \cup [110, 120) \\
\text{work/school} & \text{if } t \bmod 120 \in [10, 80) \text{ and } \rho_i = \text{worker/student} \\
\text{leisure} & \text{if } t \bmod 120 \in [80, 110) \\
\text{home} & \text{otherwise}
\end{cases}$$

### **Movement Proposal**

At each time step, agents propose moves based on their target location:

$$\vec{x}_i(t+1) = \begin{cases}
\vec{x}_i(t) + \vec{\delta}_{\text{random}}(t) & \text{if agent is in target structure} \\
\vec{x}_i(t) + \vec{\delta}_{\text{directed}}(t) & \text{if agent is moving toward target structure}
\end{cases}$$

Where:
- $\vec{\delta}_{\text{random}}(t)$ is a random move within the current structure
- $\vec{\delta}_{\text{directed}}(t)$ is a directed move toward the target structure center

## **4. Interaction Range**

The interaction range for agent $i$ is determined by:
$$R_i(t) = \min(3, \lfloor \phi_i(t) \times 3 \rfloor)$$

**Note**: This differs from the original model - it uses $\lfloor \phi_i(t) \times 3 \rfloor$ instead of $\lfloor 3\phi_i(t) \rfloor$.

## **5. Interaction Probability**

### **Spatial Interaction Condition**

For agents $i$ and $j$ at positions $\vec{x}_i(t)$ and $\vec{x}_j(t)$:

$$\text{Interact}_{ij}(t) = \begin{cases}
1 & \text{if } \max(|x_i(t) - x_j(t)|, |y_i(t) - y_j(t)|) \leq R_i(t) \\
0 & \text{otherwise}
\end{cases}$$

**Note**: This uses the $L_\infty$ (Chebyshev) distance, not the originally stated $L_\infty$ norm.

### **Friend Interaction Selection**

For each agent $i$ at time $t$:
$$\mathcal{S}_i(t) \subseteq \mathcal{F}_i \text{ where } |\mathcal{S}_i(t)| \sim \text{Uniform}\{1, 2, 3\}$$

## **6. Interaction Quality**

For each interaction, the quality is determined by:
$$Q_{ij}(t) \sim \text{Bernoulli}(0.7)$$

Where $Q_{ij}(t) = 1$ represents a positive interaction and $Q_{ij}(t) = 0$ represents a negative interaction.

## **7. Integrity Update Dynamics**

For regular agents only ($\tau_i = \text{regular}$):

$$\Delta\phi_i(t) = \alpha \cdot f(\text{same-opinion}_{ij}(t), Q_{ij}(t), \phi_i(t)) \cdot \gamma_{ij}(t)$$

Where $\alpha = 0.1$ is the base influence strength, $\gamma_{ij}(t)$ is the friend reduction factor:

$$\gamma_{ij}(t) = \begin{cases}
0.0625 & \text{if } j \in \mathcal{S}_i(t) \text{ (friend interaction)} \\
1.0 & \text{if } \text{Interact}_{ij}(t) = 1 \text{ (spatial interaction)}
\end{cases}$$

And:

$$f(s, q, \phi) = \begin{cases}
(1 - \phi) & \text{if } s = 1 \land q = 1 \quad \text{(positive, same opinion)} \\
-\phi & \text{if } s = 0 \land q = 1 \quad \text{(positive, different opinion)} \\
-\phi & \text{if } s = 1 \land q = 0 \quad \text{(negative, same opinion)} \\
(1 - \phi) & \text{if } s = 0 \land q = 0 \quad \text{(negative, different opinion)}
\end{cases}$$

The integrity update rule:
$$\phi_i(t+1) = \max(0, \min(1, \phi_i(t) + \Delta\phi_i(t)))$$

## **8. Opinion Change Dynamics**

For regular agents only ($\tau_i = \text{regular}$):

The probability of opinion change is:
$$P(\text{change}_{ij}(t)) = \beta \cdot (1 - \phi_i(t)) \cdot \phi_j(t) \cdot \gamma_{ij}(t)$$

Where $\beta = 0.5$ is the scale factor and $\gamma_{ij}(t)$ is the friend reduction factor (same as above).

The opinion change rule:
$$o_i(t+1) = \begin{cases}
o_j(t) & \text{with probability } P(\text{change}_{ij}(t)) \\
o_i(t) & \text{with probability } 1 - P(\text{change}_{ij}(t))
\end{cases}$$

## **9. Complete Interaction Model**

For each time step $t$:

1. **Schedule Update Phase**:
   $$\ell_i(t+1) = \text{schedule\_function}(t+1, \rho_i)$$

2. **Movement Phase**:
   $$\vec{x}_i(t+1) = \text{propose\_move}(\vec{x}_i(t), \ell_i(t+1), \mathcal{H}_i, \mathcal{W}_i, \mathcal{L}_i)$$

3. **Friend Interaction Phase**:
   For each agent $i$:
   - Select $\mathcal{S}_i(t) \subseteq \mathcal{F}_i$ with $|\mathcal{S}_i(t)| \in \{1, 2, 3\}$
   - For each $j \in \mathcal{S}_i(t)$:
     - Generate $Q_{ij}(t) \sim \text{Bernoulli}(0.7)$
     - Update $\phi_i(t+1)$ and $\phi_j(t+1)$ using integrity dynamics with friend reduction
     - Update $o_i(t+1)$ and $o_j(t+1)$ using opinion dynamics with friend reduction

4. **Spatial Interaction Phase**:
   For each agent $i$:
   - Calculate $R_i(t) = \min(3, \lfloor \phi_i(t) \times 3 \rfloor)$
   - For each agent $j$ where $\text{Interact}_{ij}(t) = 1$:
     - Generate $Q_{ij}(t) \sim \text{Bernoulli}(0.7)$
     - Update $\phi_i(t+1)$ and $\phi_j(t+1)$ using integrity dynamics
     - Update $o_i(t+1)$ and $o_j(t+1)$ using opinion dynamics

## **10. System-Level Dynamics**

### **Opinion Distribution**:
$$N_k(t) = \sum_{i=1}^{N} \mathbb{I}[o_i(t) = k]$$

### **Average Integrity**:
$$\bar{\phi}(t) = \frac{1}{N} \sum_{i=1}^{N} \phi_i(t)$$

### **Location Distribution**:
$$L_\ell(t) = \sum_{i=1}^{N} \mathbb{I}[\ell_i(t) = \ell] \quad \text{for } \ell \in \{\text{home}, \text{work}, \text{school}, \text{leisure}\}$$

## **11. Key Mathematical Properties**

### **Stability Conditions**:
- High integrity agents ($\phi_i = 1$) are fixed points for integrity and opinion dynamics
- High integrity agents can influence regular agents but are immune to influence themselves
- The system has potential absorbing states when all agents have the same opinion
- Integrity is bounded: $\phi_i(t) \in [0, 1]$ for all $t$
- Schedule is deterministic and cyclic with period 120

### **Convergence Behavior**:
- The system can converge to opinion consensus or maintain multiple opinion clusters
- High integrity agents act as "opinion anchors" that resist change
- Structure-based movement creates temporal clustering effects
- Friend networks provide persistent influence channels with reduced effect

## **12. Parameter Summary**

| Parameter | Value | Description |
|-----------|-------|-------------|
| $\alpha$ | 0.1 | Base influence strength for integrity changes |
| $\beta$ | 0.5 | Scale factor for opinion change probability |
| $p_{positive}$ | 0.7 | Probability of positive interactions |
| $\phi_{high}$ | 1.0 | Integrity level for high-integrity agents |
| $\phi_{min}$ | 0.3 | Minimum initial integrity for regular agents |
| $\phi_{max}$ | 0.7 | Maximum initial integrity for regular agents |
| $R_{max}$ | 3 | Maximum interaction range |
| $N_{opinions}$ | 3 | Number of possible opinions |
| $N_{friends}$ | 8 | Maximum number of friends per agent |
| $\gamma_{friend}$ | 0.0625 | Friend interaction reduction factor (1/16th effect) |
| $N_{friend\_interactions}$ | 1-3 | Number of friend interactions per step |
| $T_{schedule}$ | 120 | Schedule cycle length (steps per day) |
| $N_{home\_groups}$ | 12 | Number of home structure groups |
| $N_{work\_groups}$ | 6 | Number of work structure groups |
| $N_{school\_groups}$ | 6 | Number of school structure groups |
| $N_{leisure\_groups}$ | 8 | Number of leisure structure groups |

## **13. Implementation Notes**

This mathematical model corresponds to the current implementation in:
- `agent.py`: Agent behavior, interaction logic, and schedule management
- `environment.py`: Spatial dynamics, structure definitions, and interaction scheduling
- `main.py`: System initialization and simulation control

The model captures the essential dynamics of the agent-based opinion spread simulation, including:
- Integrity-based influence mechanisms
- Spatial and social network interactions
- Schedule-driven movement patterns
- Structure-based agent grouping
- Temporal dynamics with daily cycles

The key insight is that this system combines **spatial clustering** (through scheduled movement to structures), **social influence** (through friend networks), and **integrity-based resistance** (through high-integrity agents) to create complex opinion dynamics that can lead to either consensus or persistent disagreement depending on initial conditions and parameter settings.
