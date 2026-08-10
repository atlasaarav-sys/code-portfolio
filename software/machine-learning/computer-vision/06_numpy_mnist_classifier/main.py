import numpy as np
from sklearn.datasets import load_digits

from neural_network import NeuralNetwork


def one_hot(y, num_classes):
    out = np.zeros((len(y), num_classes))
    out[np.arange(len(y)), y] = 1
    return out


def main():
    digits = load_digits()
    X = digits.data.astype(np.float64) / 16.0  # pixel values are 0-16, normalize to 0-1
    y = digits.target

    rng = np.random.default_rng(0)
    indices = rng.permutation(len(X))
    split = int(0.8 * len(X))
    train_idx, test_idx = indices[:split], indices[split:]

    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    print(f"Loaded {len(X)} real handwritten digit images (8x8), 10 classes")
    print(f"Train: {len(X_train)}  Test: {len(X_test)}\n")

    net = NeuralNetwork(input_size=64, hidden_size=32, output_size=10)
    y_train_onehot = one_hot(y_train, 10)

    epochs = 200
    batch_size = 32
    for epoch in range(epochs):
        perm = rng.permutation(len(X_train))
        epoch_loss = 0.0
        n_batches = 0
        for start in range(0, len(X_train), batch_size):
            batch_idx = perm[start:start + batch_size]
            loss = net.train_step(X_train[batch_idx], y_train_onehot[batch_idx], lr=0.3, momentum=0.9)
            epoch_loss += loss
            n_batches += 1

        if (epoch + 1) % 40 == 0 or epoch == 0:
            train_acc = np.mean(net.predict(X_train) == y_train)
            print(f"Epoch {epoch + 1:3d}: loss={epoch_loss / n_batches:.4f}  train_acc={train_acc:.4f}")

    test_preds = net.predict(X_test)
    test_acc = np.mean(test_preds == y_test)
    print(f"\nFinal test accuracy: {test_acc:.4f} ({int(test_acc * len(y_test))}/{len(y_test)})")

    print("\nPer-class test accuracy:")
    for digit in range(10):
        mask = y_test == digit
        if mask.sum() > 0:
            class_acc = np.mean(test_preds[mask] == digit)
            print(f"  digit {digit}: {class_acc:.2f} ({mask.sum()} samples)")


if __name__ == "__main__":
    main()
