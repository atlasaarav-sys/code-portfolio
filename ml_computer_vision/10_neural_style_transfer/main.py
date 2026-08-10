import argparse

import torch
import torchvision.transforms as T
from PIL import Image

from style_transfer import run_style_transfer

IMAGE_SIZE = 512


def load_image(path, device):
    image = Image.open(path).convert("RGB")
    transform = T.Compose([T.Resize((IMAGE_SIZE, IMAGE_SIZE)), T.ToTensor()])
    return transform(image).unsqueeze(0).to(device)


def save_image(tensor, path):
    image = tensor.squeeze(0).cpu().clamp(0, 1)
    T.ToPILImage()(image).save(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", required=True)
    parser.add_argument("--style", required=True)
    parser.add_argument("--output", default="stylized.jpg")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--style-weight", type=float, default=1e6)
    parser.add_argument("--content-weight", type=float, default=1.0)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    content_img = load_image(args.content, device)
    style_img = load_image(args.style, device)

    result = run_style_transfer(
        content_img, style_img, device,
        num_steps=args.steps,
        style_weight=args.style_weight,
        content_weight=args.content_weight,
    )

    save_image(result, args.output)
    print(f"Saved stylized image to {args.output}")


if __name__ == "__main__":
    main()
