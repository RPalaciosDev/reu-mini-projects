# Mini Project 2

**Authors:** Roberto Palacios, Sam Guven

## Assumptions

Assume a random (undirected) graph/network of $N$ nodes/vertices that has exactly $C$ connections/links/edges.

- The $C$ connections are randomly distributed between any pair of nodes.
- Further assume that you let a 'random walker' walk around on that network.
- The random walker can only hop from a node/vertex to another node/vertex if these two nodes are connected by a link/edge.
- The maximum number of edges for $N$ nodes is the fastest time it takes to travel to all the nodes.

## Problems and Solutions

### 1. How long does it take a random walker on average to visit each and every node on a network of $N$ nodes and $C$ edges?

- It takes a random walker according to our code, approximately 229.62 seconds to get to all $N$ nodes with $C$ edges.

### 2. Are there any prerequisites that the network must satisfy before a random walker can visit all nodes?

- The Network must be connected
- There must be at least $N-1$ edges for it to be connected
- Probably needs to be strongly connected, or no isolated nodes with very weak probabilities to get there
- $N$ and $C$ are both finite
- No sections where the random walker could get probably trapped between two nodes or a subset of nodes

### 3. How does the average visiting time scale as a function of $N$ and $C$, i.e., as you increase $N$ and $C$?

- $N$ has a maximum and Minimum amount of $C$'s it can have
- We see from the graph that the average visiting time decreases as we increase the number of Edges
- But if we increase the number of nodes, then the average visiting time increases

### 4. What happens when $C$ is lowered? Is there a critical value?

- Yes, $C$ cannot be lower than $N-1$, so $C = N-1$ would be the critical value or the minimum time it takes to get to each node

### 5. How could you improve the random walker's strategy so that visiting all nodes would be more efficient?

- We thought the greedy cover walk would improve the random walker's strategy, where every step leads to the node with the fewest visits or a subsection of the graph that has the fewest visits

## Analysis

The random walk on a graph with $N$ nodes and $C$ connections, where the path to different nodes (states) has different probabilities (connections) to get to other nodes for the undirected graph.

### 1. Average Visiting Time Analysis

- To see how long it takes for a random walker on average, we need to run many simulations of different $N$ and $C$ values, get a cover time for each of those, and see what the average time is of those cover times
- We first used Python and ChatGPT to take all the different values of $N$ and $C$ and their cover time values and fitted them to the equation:
  $$T(N, C) \approx 3.626 \cdot (N \log N) + 3274.172 \cdot (\frac{1}{C}) - 170.014$$
- Graphed that equation against the data points of $N$, $C$, and $T$ to show the fitted equation fit
- We used both that and the average of the cover time values, and we got 229.62 seconds for both of the average cover time values

### 2. Network Prerequisites Analysis

- There are a lot of small things that would not allow the random walker to reach every node or to have a probable chance of eventually reaching every node
- In doing this, we listed a lot of prerequisites, but the main one that generally encompasses all of the others is that the graph has to be connected

### 3. Scaling Analysis

- Based on the heatmap in our code, every $N$ value has a maximum and minimum number of edges that a node can have
- We can isolate both $N$ and $C$ and see what changes increasing $N$ and $C$ does to the cover time
- A common thing we found was that increasing the number of edges decreased the cover time, and increasing the number of nodes increased the cover time
- This also leads us to the fact that the maximum number of edges for $N$ nodes is the fastest time it takes to travel to all the nodes

### 4. Critical Value Analysis

- This is the opposite of what we saw in the previous questions, where it turns out that the lower the $C$ value, the more the cover time increases
- So the critical value when we lower $C$ will be whatever the lowest amount of edges would be for a given number of nodes
- $C$ cannot be lower than $N-1$, so $C = N-1$ would be the critical value or the minimum time it takes to get to each node

### 5. Strategy Improvement Analysis

- There are a lot more efficient ways to improve the random walkers' strategy, but the one we decided to go with is a greedy cover walk
- A greedy cover walk where every step leads to the node with the fewest visits or a subsection of the graph that has the fewest visits
