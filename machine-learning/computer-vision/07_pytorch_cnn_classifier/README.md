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

## Notes — not executed in this environment

This wasn't run here: PyTorch/torchvision are multi-hundred-MB installs
and CIFAR-10 training needs either real compute time or a GPU to be
meaningful, neither of which fit a portfolio verification pass. The code
is written against the current, real PyTorch API (`nn.Module`,
`DataLoader`, `torch.optim`) — review it before running, and expect to
debug it like any other untested code, since "written correctly" and
"verified correct" are different claims and this repo tries to be explicit
about which is which per project.
