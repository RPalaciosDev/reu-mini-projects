# Belief Dynamics Simulation

This project implements discrete-time models of belief dynamics in a closed, well-mixed population. It explores how different social influence mechanisms affect the evolution of beliefs within a population over time.

## Overview

The simulation models a population where individuals can hold one of three possible states:

- **Believers** (b)
- **Skeptics/Non-believers** (n)
- **Agnostics/Undecided** (a)

The models track how these proportions change over time based on various conversion mechanisms and social influence rules.

## Models Implemented

### 1. Minimal Two-State Model

- Simplest model with only believers and non-believers
- Uses basic conversion rates between states
- Demonstrates fundamental dynamics of belief adoption and abandonment

### 2. Three-State Model with Neutral Group

- Adds an agnostic/undecided population
- Implements conversion rates between all three states
- Shows how a neutral group affects belief dynamics

### 3. Social Pressure Model

- Introduces social influence based on majority pressure
- Larger groups exert more influence on others
- Demonstrates how social pressure can lead to consensus or polarization

### 4. Inverse-Popularity Model

- Implements a "support the underdog" mechanism
- Smaller groups receive more support from the undecided
- Shows how minority protection can prevent complete consensus

## Key Features

- **Mass Conservation**: All models maintain \(p_b + p_n + p_a = 1\)
- **Visualization**: Time series plots of population proportions
- **Parameter Control**: Adjustable conversion rates and influence parameters
- **Multiple Scenarios**: Compare different social influence mechanisms

## Usage

1. Open `Systems_with_a_Small_Number_of_Variables.ipynb` in Jupyter Notebook
2. Run the cells sequentially to see different models in action
3. Modify parameters to explore different scenarios:
   - Conversion rates between states
   - Social pressure strength (r)
   - Initial population proportions
   - Number of time steps

## Dependencies

- Python 3.x
- matplotlib
- Jupyter Notebook

## Key Parameters

- **Conversion Rates**: Control spontaneous switching between states
- **Campaign Intensity (r)**: Controls strength of social influence
- **Epsilon (ε)**: Small constant to prevent division by zero
- **Time Steps**: Number of iterations to run the simulation

## Insights

The models demonstrate how simple rules can lead to complex population dynamics:

- Consensus formation
- Polarization
- Oscillating states
- Stable mixed populations

## Extensions

The framework can be extended to include:

- Memory effects
- Time-varying rates
- Network structure
- Additional opinion states
- External influences

## Author

This project was created as part of a research experience for undergraduates (REU) program.

## License

This project is open source and available for educational and research purposes.
