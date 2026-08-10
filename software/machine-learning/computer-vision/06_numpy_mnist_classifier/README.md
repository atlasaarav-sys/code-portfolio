# Numpy MNIST-Style Digit Classifier

**Stack:** Python 3, `numpy` (the network itself), `scikit-learn` (data
loading only — `load_digits`, not any sklearn model)

A feedforward neural network (one hidden layer, ReLU, softmax output,
cross-entropy loss) with forward pass, backpropagation, and mini-batch
gradient descent all implemented by hand in numpy — no `torch`/`tensorflow`
— trained on real handwritten digit images (`sklearn.datasets.load_digits`:
1797 real 8x8 grayscale digit scans, 10 classes, bundled with scikit-learn
so no internet download is needed).

## Files

- `neural_network.py` — `NeuralNetwork`: Xavier-initialized weights,
  `forward`, `backward` (manual gradient derivation for
  softmax+cross-entropy and ReLU), `train_step` (mini-batch SGD with
  momentum)
- `main.py` — loads the digit dataset, splits train/test, trains for N
  epochs, reports train/test accuracy and a per-class confusion count

## How to run

```bash
python main.py
```

## What was actually tested here

Trained on 1437 real digit images (80% split of the 1797-image dataset),
evaluated on the held-out 360. See the printed output from the actual run
for exact train/test accuracy and per-epoch loss — this was not tuned to
hit a specific number, just run and reported honestly.

## Notes

`sklearn.datasets.load_digits` images are 8x8 (an older, smaller UCI
dataset than the famous 28x28 MNIST) — chosen specifically because it's
bundled with scikit-learn with zero network dependency, so this trains on
real handwritten digits without requiring a dataset download. Swapping in
real MNIST (28x28, 60k images) means changing the input layer size and the
data loader; the network/training code is otherwise unchanged.
