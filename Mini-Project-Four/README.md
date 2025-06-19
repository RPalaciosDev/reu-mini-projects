# Neural Network Graph Classification Project

**Authors:** Luis Hernandez, Roberto Palacios  
**Project:** REU Mini-Project Four - Agentic Opinion Spread

## 📋 Project Overview

This project implements a feedforward neural network to classify graphs as directed or undirected based on their adjacency matrices. The system is designed with a modular architecture for easy experimentation and analysis.

## 🏗️ Modular Architecture

### Core Modules

1. **`neural_network_trainer.py`** - Main training system
   - `AdjacencyMatrixGenerator` - Data generation and management
   - `NeuralNetwork` - Neural network implementation with momentum
   - `NeuralNetworkTrainer` - Modular experiment management

2. **`experiment_runner.py`** - Main execution script
   - Interactive profile selection
   - Batch experiment execution
   - Results comparison and visualization

3. **`visualization_tools.py`** - Enhanced analysis tools
   - `GraphVisualizer` - Comprehensive plotting and analysis
   - Training curve analysis
   - Confusion matrix and ROC curves
   - Feature importance analysis
   - Comprehensive reporting

## 🚀 Quick Start

### Option 1: Interactive Runner

```bash
python experiment_runner.py
```

This will show available profiles and let you choose which experiment to run.

### Option 2: Direct Training

```python
from neural_network_trainer import NeuralNetworkTrainer

trainer = NeuralNetworkTrainer()
results = trainer.run_experiment("5x5", verbose=True, plot=True)
```

## 📊 Available Profiles

| Profile | Matrix Size | Hidden Size | Learning Rate | Weight Decay | Epochs | Samples | Description |
|---------|-------------|-------------|---------------|--------------|--------|---------|-------------|
| 4x4 | 4×4 | 12 | 0.001 | 0.0002 | 10,000 | 6,000 | Fast training, high accuracy |
| 5x5 | 5×5 | 16 | 0.0005 | 0.002 | 20,000 | 8,000 | Balanced complexity |
| 6x6 | 6×6 | 48 | 0.0001 | 0.002 | 20,000 | 8,000 | Complex patterns |

## 🔧 Key Features

### **Advanced Training Features**

- **Momentum**: Smooth gradient updates for better convergence
- **Weight Decay**: L2 regularization to prevent overfitting
- **Learning Rate Scheduling**: Warmup and decay for optimal training
- **Early Warning System**: Detects training issues automatically

### **Comprehensive Analysis**

- **Overfitting Detection**: Automatic analysis of generalization
- **Training Curves**: Detailed error analysis with smoothing
- **Confusion Matrices**: Classification performance breakdown
- **ROC & PR Curves**: Advanced performance metrics
- **Feature Importance**: Weight analysis for interpretability

### **Data Management**

- **Pickle Format**: Efficient storage and loading
- **Reproducible Results**: Consistent random seeds
- **Stratified Splits**: Balanced train/test sets
- **Multiple Matrix Sizes**: Scalable experimentation

## 📈 Performance Analysis

### **Current Results (5x5 Profile)**

- **Test Accuracy**: 99.93%
- **Test MSE**: 0.001021
- **Training MSE**: 0.000012
- **Overfitting Ratio**: ~85x (indicates overfitting)

### **Recommendations**

1. **Reduce Model Complexity**: Smaller hidden layer
2. **Increase Regularization**: Higher weight decay
3. **Add More Data**: Larger dataset
4. **Early Stopping**: Prevent overfitting

## 🛠️ Usage Examples

### Basic Training

```python
from neural_network_trainer import NeuralNetworkTrainer

trainer = NeuralNetworkTrainer()
results = trainer.run_experiment("5x5")
```

### Custom Profile

```python
# Create custom profile
custom_profile = {
    "matrix_size": 4,
    "hidden_size": 8,
    "learning_rate": 0.001,
    "weight_decay": 0.001,
    "epochs": 5000,
    "num_samples": 3000,
    "data_file": "custom_data.pkl"
}

# Use in trainer
trainer.profiles["custom"] = custom_profile
results = trainer.run_experiment("custom")
```

### Advanced Visualization

```python
from visualization_tools import GraphVisualizer

visualizer = GraphVisualizer()

# Plot training curves
visualizer.plot_training_curves(training_errors, validation_errors)

# Create comprehensive report
visualizer.create_comprehensive_report(training_results, test_results)
```

## 📁 File Structure

```
Mini-Project-Four/
├── neural_network_trainer.py    # Core training system
├── experiment_runner.py         # Main execution script
├── visualization_tools.py       # Analysis and plotting
├── README.md                   # This file
├── neural_network_training_data_4x4.pkl  # Pre-generated data
├── neural_network_training_data_5x5.pkl  # Pre-generated data
└── neural_network_training_data_6x6.pkl  # Pre-generated data
```

## 🔬 Technical Details

### **Neural Network Architecture**

- **Input Layer**: Flattened adjacency matrix (n² features)
- **Hidden Layer**: Sigmoid activation with configurable size
- **Output Layer**: Single neuron with sigmoid activation
- **Loss Function**: Mean Squared Error
- **Optimizer**: Gradient descent with momentum

### **Data Generation**

- **Symmetric Matrices**: Undirected graphs (label: 0)
- **Non-symmetric Matrices**: Directed graphs (label: 1)
- **Edge Density**: Random distribution
- **No Self-loops**: Diagonal elements set to 0

### **Training Process**

1. **Data Preparation**: Generate/load matrices, flatten, split
2. **Model Initialization**: He initialization for weights
3. **Training Loop**: Forward/backward passes with momentum
4. **Monitoring**: Error tracking and early warnings
5. **Evaluation**: Test set performance analysis

## 🎯 Future Improvements

### **Immediate Enhancements**

- [ ] Add dropout regularization
- [ ] Implement batch normalization
- [ ] Add cross-validation
- [ ] Support for larger matrix sizes

### **Advanced Features**

- [ ] Graph neural networks (GNNs)
- [ ] Attention mechanisms
- [ ] Multi-class classification
- [ ] Real-world graph datasets

### **Analysis Tools**

- [ ] Automated hyperparameter tuning
- [ ] Model interpretability tools
- [ ] Performance benchmarking
- [ ] Export to ONNX format

## 📚 Dependencies

```bash
pip install numpy matplotlib seaborn scikit-learn networkx
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the REU Mini-Projects series. See LICENSE file for details.

---

**Note**: The current implementation shows excellent accuracy but some overfitting. Consider the recommendations above for production use.
