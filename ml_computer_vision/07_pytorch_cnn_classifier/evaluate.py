"""Load a checkpoint, report test accuracy + a confusion matrix."""

import argparse

import torch
import torchvision
import torchvision.transforms as T
from torch.utils.data import DataLoader

from model import SimpleCNN
from train import CIFAR10_MEAN, CIFAR10_STD

CLASSES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="best_model.pt")
    parser.add_argument("--batch-size", type=int, default=128)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transform = T.Compose([T.ToTensor(), T.Normalize(CIFAR10_MEAN, CIFAR10_STD)])
    test_set = torchvision.datasets.CIFAR10("./data", train=False, download=True, transform=transform)
    test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False)

    model = SimpleCNN(num_classes=10).to(device)
    model.load_state_dict(torch.load(args.checkpoint, map_location=device))
    model.eval()

    confusion = torch.zeros(10, 10, dtype=torch.int64)
    correct, total = 0, 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            for t, p in zip(labels.view(-1), preds.view(-1)):
                confusion[t.long(), p.long()] += 1

    print(f"Test accuracy: {correct / total:.4f} ({correct}/{total})\n")
    print("Confusion matrix (rows=true, cols=predicted):")
    print("           " + " ".join(f"{c[:4]:>5}" for c in CLASSES))
    for i, row in enumerate(confusion):
        print(f"{CLASSES[i]:<10} " + " ".join(f"{v.item():>5}" for v in row))


if __name__ == "__main__":
    main()
