# PyTorch CNN Classifier

**Stack:** PyTorch, `torchvision`

A standard CNN image classifier (Conv -> BatchNorm -> ReLU blocks, max
pooling, a small fully-connected head) for CIFAR-10-style 10-class 32x32
color images, with a full training loop (data augmentation, learning-rate
scheduling, train/val split, checkpointing).

## Files

- `model.py` — `SimpleCNN`: 3 convolutional blocks (32/64/128 channels)
  with batch norm + max pooling, followed by a 2-layer classifier head
  with dropout
- `train.py` — training loop: `torchvision.datasets.CIFAR10` (downloads on
  first run), standard augmentation (random crop + horizontal flip,
  normalization), `CrossEntropyLoss`, Adam + `CosineAnnealingLR`,
  per-epoch train/val accuracy, saves the best checkpoint
- `evaluate.py` — loads a saved checkpoint, reports test-set accuracy and
  a confusion matrix

## How to run

```bash
pip install torch torchvision
python train.py --epochs 20 --batch-size 128
python evaluate.py --checkpoint best_model.pt
```

## Notes

Written against the current PyTorch API (`nn.Module`, `DataLoader`,
`torch.optim`). CIFAR-10 training benefits from a GPU but isn't required.
