# Neural Style Transfer

**Stack:** PyTorch, `torchvision` (pretrained VGG19)

The classic Gatys et al. neural style transfer: optimize a generated
image (starting from the content image) so its VGG19 feature activations
match the content image's activations at a deep layer, while its Gram
matrices (feature correlations, which capture "style" independent of
spatial layout) match the style image's Gram matrices at several layers —
all via gradient descent directly on image pixels, not on network weights.

## Files

- `style_transfer.py` — `ContentLoss`/`StyleLoss` modules hooked into a
  frozen, pretrained VGG19; `run_style_transfer()` runs L-BFGS
  optimization directly on the generated image's pixel values
- `main.py` — CLI: `--content`, `--style`, `--output`, `--steps`,
  `--style-weight`/`--content-weight`

## How to run

```bash
pip install torch torchvision pillow
python main.py --content photo.jpg --style painting.jpg --output stylized.jpg --steps 300
```

## Notes — not executed in this environment

Not run here: needs PyTorch + a pretrained VGG19 download (~550MB) plus
real content/style images, none of which fit a portfolio verification
pass. `style_transfer.py` follows the original Gatys et al. formulation
closely (content loss at `conv4_2`, style loss averaged across
`conv1_1`-`conv5_1` with Gram matrices, L-BFGS rather than Adam since it
converges faster for this specific pixel-optimization setup) — it's
written to be run, not to look plausible; expect the normal amount of
debugging any from-scratch training script needs on first real run.
