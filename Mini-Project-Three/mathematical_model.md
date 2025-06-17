# Mathematical Model for Agent Interaction Scheme

## **1. Agent State Representation**

For each agent $i$ at time $t$:

- **Position**: $\vec{x}_i(t) = (x_i(t), y_i(t)) \in \mathbb{Z}^2$
- **Opinion**: $o_i(t) \in \{0, 1, 2\}$
- **Integrity**: $\phi_i(t) \in [0, 1]$
- **Type**: $\tau_i \in \{\text{regular}, \text{high-integrity}\}$
- **Friends**: $\mathcal{F}_i \subseteq \{1, 2, \ldots, N\}$ (set of friend agent indices)

## **2. Initial Conditions**

### **High Integrity Agents** ($\tau_i = \text{high-integrity}$)

$$\phi_i(0) = 1.0, \quad \phi_i(t) = 1.0 \quad \forall t > 0$$

### **Regular Agents** ($\tau_i = \text{regular}$)

$$\phi_i(0) \sim \text{Uniform}(0.3, 0.7)$$

### **Friend Network Initialization**

For each agent $i$, friends are selected such that:

- $|\mathcal{F}_i| \leq 8$ (maximum 8 friends)
- $j \in \mathcal{F}_i \implies o_i(0) = o_j(0)$ (same opinion requirement)
- $j \in \mathcal{F}_i \implies i \in \mathcal{F}_j$ (bidirectional friendships)

## **3. Movement Dynamics**

At each time step, each agent proposes a move to an adjacent cell:
$$\vec{x}_i(t+1) = \vec{x}_i(t) + \vec{\delta}_i(t)$$

Where $\vec{\delta}_i(t) \in \{(1,0), (-1,0), (0,1), (0,-1)\}$ is chosen uniformly at random, subject to boundary and occupancy constraints.

## **4. Interaction Range**

The interaction range for agent $i$ is determined by:
$$R_i(t) = \min(3, \lfloor 3\phi_i(t) \rfloor)$$

## **5. Interaction Probability**

For agents $i$ and $j$ at positions $\vec{x}_i(t)$ and $\vec{x}_j(t)$:

### **Spatial Interaction Condition**

$$\text{Interact}_{ij}(t) = \begin{cases}
1 & \text{if } \|\vec{x}_i(t) - \vec{x}_j(t)\|_\infty \leq R_i(t) \\
0 & \text{otherwise}
\end{cases}$$

**Note**: High integrity agents can interact with agents of different opinions and influence them, but they themselves are immune to integrity and opinion changes.

## **6. Interaction Quality**

For each interaction, the quality is determined by:
$$Q_{ij}(t) \sim \text{Bernoulli}(0.7)$$

Where $Q_{ij}(t) = 1$ represents a positive interaction and $Q_{ij}(t) = 0$ represents a negative interaction.

## **7. Integrity Update Dynamics**

For regular agents only ($\tau_i = \text{regular}$):

$$\Delta\phi_i(t) = \alpha \cdot f(\text{same-opinion}_{ij}(t), Q_{ij}(t), \phi_i(t)) \cdot \gamma_{ij}(t)$$

Where $\alpha = 0.1$ is the base influence strength, $\gamma_{ij}(t)$ is the friend reduction factor:

$$\gamma_{ij}(t) = \begin{cases}
0.0625 & \text{if } j \in \mathcal{F}_i \text{ (friend interaction)} \\
1.0 & \text{otherwise (spatial interaction)}
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

1. **Movement Phase**:
   $$\vec{x}_i(t+1) = \vec{x}_i(t) + \vec{\delta}_i(t)$$

2. **Friend Interaction Phase**:
   For each agent $i$:
   - Select a random subset $\mathcal{S}_i(t) \subseteq \mathcal{F}_i$ with $|\mathcal{S}_i(t)| \in \{1, 2, 3\}$
   - For each $j \in \mathcal{S}_i(t)$:
     - Generate $Q_{ij}(t) \sim \text{Bernoulli}(0.7)$
     - Update $\phi_i(t+1)$ and $\phi_j(t+1)$ using integrity dynamics with friend reduction (only for regular agents)
     - Update $o_i(t+1)$ and $o_j(t+1)$ using opinion dynamics with friend reduction (only for regular agents)

3. **Spatial Interaction Phase**:
   For each pair of agents $(i,j)$:

   $$\text{Interaction}_{ij}(t) = \text{Interact}_{ij}(t)$$

   If $\text{Interaction}_{ij}(t) = 1$:
   - Generate $Q_{ij}(t) \sim \text{Bernoulli}(0.7)$
   - Update $\phi_i(t+1)$ and $\phi_j(t+1)$ using integrity dynamics (only for regular agents)
   - Update $o_i(t+1)$ and $o_j(t+1)$ using opinion dynamics (only for regular agents)

## **10. System-Level Dynamics**

### **Opinion Distribution**:
$$N_k(t) = \sum_{i=1}^{N} \mathbb{I}[o_i(t) = k]$$

Where $N_k(t)$ is the number of agents with opinion $k$ at time $t$.

### **Average Integrity**:
$$\bar{\phi}(t) = \frac{1}{N} \sum_{i=1}^{N} \phi_i(t)$$

## **11. Key Mathematical Properties**

### **Stability Conditions**:
- High integrity agents ($\phi_i = 1$) are fixed points for integrity and opinion dynamics
- High integrity agents can influence regular agents but are immune to influence themselves
- The system has absorbing states when all agents have the same opinion
- Integrity is bounded: $\phi_i(t) \in [0, 1]$ for all $t$

### **Convergence Behavior**:
- The system can converge to opinion consensus or maintain multiple opinion clusters
- High integrity agents act as "influencers" that can cause others to lose integrity when interacting across opinion differences
- The interaction range creates spatial clustering effects

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

## **13. Implementation Notes**

This mathematical model corresponds to the current implementation in:
- `agent.py`: Agent behavior and interaction logic
- `environment.py`: Spatial dynamics and interaction scheduling
- `main.py`: System initialization and simulation control

The model captures the essential dynamics of the agent-based opinion spread simulation, including the integrity-based influence mechanisms, spatial interactions, and the role of high-integrity agents as opinion stabilizers.
