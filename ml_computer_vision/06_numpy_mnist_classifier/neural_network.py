"""A feedforward NN (1 hidden layer, ReLU, softmax) with manual backprop."""

import numpy as np


def relu(x):
    return np.maximum(0, x)


def relu_grad(x):
    return (x > 0).astype(np.float64)


def softmax(x):
    shifted = x - np.max(x, axis=1, keepdims=True)  # numerical stability
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=1, keepdims=True)


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, seed=42):
        rng = np.random.default_rng(seed)
        # Xavier/Glorot initialization: keeps activation variance stable
        # across layers instead of exploding/vanishing at initialization.
        self.W1 = rng.normal(0, np.sqrt(2.0 / input_size), (input_size, hidden_size))
        self.b1 = np.zeros(hidden_size)
        self.W2 = rng.normal(0, np.sqrt(2.0 / hidden_size), (hidden_size, output_size))
        self.b2 = np.zeros(output_size)

        # Momentum buffers
        self.vW1 = np.zeros_like(self.W1)
        self.vb1 = np.zeros_like(self.b1)
        self.vW2 = np.zeros_like(self.W2)
        self.vb2 = np.zeros_like(self.b2)

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = relu(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = softmax(self.z2)
        return self.a2

    def loss(self, y_pred, y_true_onehot):
        eps = 1e-9
        return -np.mean(np.sum(y_true_onehot * np.log(y_pred + eps), axis=1))

    def backward(self, X, y_true_onehot, y_pred):
        n = X.shape[0]

        # dL/dz2 for softmax + cross-entropy simplifies to (y_pred - y_true).
        dz2 = (y_pred - y_true_onehot) / n
        dW2 = self.a1.T @ dz2
        db2 = dz2.sum(axis=0)

        da1 = dz2 @ self.W2.T
        dz1 = da1 * relu_grad(self.z1)
        dW1 = X.T @ dz1
        db1 = dz1.sum(axis=0)

        return dW1, db1, dW2, db2

    def train_step(self, X, y_true_onehot, lr=0.1, momentum=0.9):
        y_pred = self.forward(X)
        loss = self.loss(y_pred, y_true_onehot)
        dW1, db1, dW2, db2 = self.backward(X, y_true_onehot, y_pred)

        self.vW1 = momentum * self.vW1 - lr * dW1
        self.vb1 = momentum * self.vb1 - lr * db1
        self.vW2 = momentum * self.vW2 - lr * dW2
        self.vb2 = momentum * self.vb2 - lr * db2

        self.W1 += self.vW1
        self.b1 += self.vb1
        self.W2 += self.vW2
        self.b2 += self.vb2

        return loss

    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)
