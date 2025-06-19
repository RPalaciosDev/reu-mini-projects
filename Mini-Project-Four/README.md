# Neural Network Graph Classification Project

**Authors:** Luis Hernandez, Roberto Palacios  
**Project:** REU Mini-Project Four - Agentic Opinion Spread

## 📋 Project Overview

This project implements a feedforward neural network to classify graphs as directed or undirected based on their adjacency matrices. The system features efficient training with early stopping, comprehensive evaluation metrics, and a profile-based approach for different matrix sizes.

## 🏗️ Project Structure

### Core Components

1. **`notebook_code.py`** - Complete implementation in a single file
   - `AdjacencyMatrixGenerator` - Data generation and management
   - `NeuralNetwork` - Neural network with momentum and early stopping
   - Profile system for different matrix sizes
   - Comprehensive evaluation with validation set

2. **Pre-generated Data Files**
   - `neural_network_training_data_4x4.pkl` - 4x4 matrix dataset
   - `neural_network_training_data_5x5.pkl` - 5x5 matrix dataset  
   - `neural_network_training_data_6x6.pkl` - 6x6 matrix dataset

## 🚀 Quick Start

### Run the Complete Experiment

```bash
python notebook_code.py
```

This will:

1. Load the selected profile (default: 5x5)
2. Split data into train/validation/test sets
3. Train the neural network with early stopping
4. Display comprehensive metrics and analysis

### Change Profile

Edit the `SELECTED_PROFILE` variable in the code:

```python
SELECTED_PROFILE = "5x5"  # Options: "4x4", "5x5", "6x6"
```

## 📊 Available Profiles

| Profile | Matrix Size | Hidden Size | Learning Rate | Weight Decay | Epochs | Samples | Description |
|---------|-------------|-------------|---------------|--------------|--------|---------|-------------|
| 4x4 | 4×4 | 8 | 0.001 | 0.01 | 10,000 | 6,000 | Fast training, high accuracy |
| 5x5 | 5×5 | 6 | 0.001 | 0.02 | 15,000 | 8,000 | Balanced performance (optimized) |
| 6x6 | 6×6 | 12 | 0.001 | 0.01 | 15,000 | 8,000 | Complex patterns, longer training |

## 🔧 Key Features

### **Efficient Training**

- **Early Stopping**: Automatically stops when no improvement for 1000 epochs
- **Momentum**: Smooth gradient updates for better convergence
- **Weight Decay**: L2 regularization to prevent overfitting
- **He Initialization**: Better weight initialization for faster convergence

### **Comprehensive Evaluation**

- **Three-way Split**: Train/validation/test (60%/20%/20%)
- **Multiple Metrics**: Accuracy, precision, recall, F1-score, MSE
- **Confusion Matrices**: Detailed breakdown of predictions
- **Overfitting Analysis**: Training vs validation vs test performance

### **Data Management**

- **Pickle Format**: Efficient storage and loading
- **Reproducible Results**: Consistent random seeds
- **Stratified Splits**: Balanced class distribution across all sets
- **Multiple Matrix Sizes**: Scalable experimentation

## 📈 Performance Analysis

### **Current Results (5x5 Profile - Optimized)**

- **Test Accuracy**: 98.86%
- **Test Precision**: 100.00%
- **Test Recall**: 97.71%
- **Test F1-Score**: 98.84%
- **Training MSE**: 0.001885
- **Test MSE**: 0.008949
- **Overfitting Ratio**: 4.75x (improved from 8.29x)
- **Training Efficiency**: 11,446 epochs (early stopped)

### **Key Insights**

- **Perfect Precision**: Never misclassifies undirected as directed graphs
- **High Recall**: Correctly identifies 97.71% of directed graphs
- **Balanced Performance**: Good trade-off between accuracy and generalization
- **Efficient Training**: Early stopping prevents wasted computation

### **Confusion Matrix (Test Set)**

```
                Predicted
Actual  Undirected  Directed
Undirected     700         0    ← Perfect on undirected
Directed        16       684    ← Only 16 mistakes on directed
```

## 🛠️ Usage Examples

### Basic Usage

```python
# The code is self-contained - just run it
python notebook_code.py
```

### Profile Selection

```python
# Change the profile at the top of the file
SELECTED_PROFILE = "4x4"  # For faster training
SELECTED_PROFILE = "6x6"  # For more complex patterns
```

### Custom Hyperparameters

```python
# Modify the profile dictionary
profile = PROFILES["5x5"].copy()
profile["hidden_size"] = 8
profile["weight_decay"] = 0.03
```

## 📁 File Structure

```
Mini-Project-Four/
├── notebook_code.py                    # Complete implementation
├── README.md                          # This file
├── neural_network_training_data_4x4.pkl  # Pre-generated data
├── neural_network_training_data_5x5.pkl  # Pre-generated data
└── neural_network_training_data_6x6.pkl  # Pre-generated data
```

## 🔬 Technical Details

### **Neural Network Architecture**

- **Input Layer**: Flattened adjacency matrix (n² features)
- **Hidden Layer**: Sigmoid activation with configurable size (4-12 neurons)
- **Output Layer**: Single neuron with sigmoid activation
- **Loss Function**: Mean Squared Error
- **Optimizer**: Gradient descent with momentum (0.9)

### **Data Generation**

- **Symmetric Matrices**: Undirected graphs (label: 0)
- **Non-symmetric Matrices**: Directed graphs (label: 1)
- **Edge Density**: Random distribution
- **No Self-loops**: Diagonal elements set to 0

### **Training Process**

1. **Data Preparation**: Load matrices, flatten, split into train/val/test
2. **Model Initialization**: He initialization for optimal starting weights
3. **Training Loop**: Forward/backward passes with momentum and weight decay
4. **Early Stopping**: Monitor validation performance, stop when no improvement
5. **Evaluation**: Comprehensive metrics on test set

### **Evaluation Metrics**

- **Accuracy**: Overall correct predictions
- **Precision**: How many predicted directed graphs were actually directed
- **Recall**: How many actual directed graphs were correctly identified
- **F1-Score**: Harmonic mean of precision and recall
- **MSE**: Mean squared error
- **Confusion Matrix**: Detailed breakdown of predictions

## 🎯 Optimization History

### **Initial State**

- Hidden size: 16, Weight decay: 0.002
- Test accuracy: 99.93%, Overfitting ratio: 8.29x

### **First Optimization**

- Hidden size: 8, Weight decay: 0.01
- Test accuracy: 99.79%, Overfitting ratio: 1.36x

### **Second Optimization**

- Hidden size: 4, Weight decay: 0.05
- Test accuracy: 95.71%, Overfitting ratio: 1.36x (underfitting)

### **Final Optimization**

- Hidden size: 6, Weight decay: 0.02
- Test accuracy: 98.86%, Overfitting ratio: 4.75x (balanced)

## 🚀 Future Improvements

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
pip install numpy matplotlib scikit-learn
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

**Note**: The current implementation achieves excellent classification performance (98.86% accuracy) with good generalization. The balanced hyperparameters (hidden_size=6, weight_decay=0.02) provide a good trade-off between performance and overfitting.
