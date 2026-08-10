"""Gatys et al. neural style transfer via a frozen pretrained VGG19."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

CONTENT_LAYERS = ["conv4_2"]
STYLE_LAYERS = ["conv1_1", "conv2_1", "conv3_1", "conv4_1", "conv5_1"]

# Maps VGG19's sequential module indices to human-readable layer names.
VGG19_LAYER_NAMES = {
    0: "conv1_1", 2: "conv1_2",
    5: "conv2_1", 7: "conv2_2",
    10: "conv3_1", 12: "conv3_2", 14: "conv3_3", 16: "conv3_4",
    19: "conv4_1", 21: "conv4_2", 23: "conv4_3", 25: "conv4_4",
    28: "conv5_1", 30: "conv5_2", 32: "conv5_3", 34: "conv5_4",
}


def gram_matrix(features):
    b, c, h, w = features.size()
    flat = features.view(b * c, h * w)
    gram = flat @ flat.t()
    return gram / (b * c * h * w)  # normalize so loss scale is independent of feature map size


class ContentLoss(nn.Module):
    def __init__(self, target):
        super().__init__()
        self.target = target.detach()

    def forward(self, x):
        self.loss = F.mse_loss(x, self.target)
        return x


class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super().__init__()
        self.target_gram = gram_matrix(target_feature).detach()

    def forward(self, x):
        self.loss = F.mse_loss(gram_matrix(x), self.target_gram)
        return x


def build_model_with_losses(content_img, style_img, device):
    vgg = models.vgg19(weights=models.VGG19_Weights.DEFAULT).features.to(device).eval()
    for param in vgg.parameters():
        param.requires_grad_(False)

    model = nn.Sequential()
    content_losses, style_losses = [], []

    x_content, x_style = content_img.clone(), style_img.clone()

    for i, layer in enumerate(vgg.children()):
        name = VGG19_LAYER_NAMES.get(i, f"layer_{i}")
        if isinstance(layer, nn.ReLU):
            layer = nn.ReLU(inplace=False)  # avoid in-place ops interfering with the loss modules' saved activations

        model.add_module(name, layer)
        x_content = layer(x_content)
        x_style = layer(x_style)

        if name in CONTENT_LAYERS:
            content_loss = ContentLoss(x_content)
            model.add_module(f"content_loss_{name}", content_loss)
            content_losses.append(content_loss)

        if name in STYLE_LAYERS:
            style_loss = StyleLoss(x_style)
            model.add_module(f"style_loss_{name}", style_loss)
            style_losses.append(style_loss)

        if name in VGG19_LAYER_NAMES.values() and name == "conv5_1":
            break  # no need to run the rest of the network past the deepest layer we use

    return model, content_losses, style_losses


def run_style_transfer(content_img, style_img, device, num_steps=300,
                        style_weight=1e6, content_weight=1.0):
    model, content_losses, style_losses = build_model_with_losses(content_img, style_img, device)

    generated = content_img.clone().requires_grad_(True)
    optimizer = torch.optim.LBFGS([generated])

    step = [0]
    while step[0] < num_steps:
        def closure():
            with torch.no_grad():
                generated.clamp_(0, 1)

            optimizer.zero_grad()
            model(generated)

            content_score = sum(cl.loss for cl in content_losses)
            style_score = sum(sl.loss for sl in style_losses)
            total_loss = content_weight * content_score + style_weight * style_score
            total_loss.backward()

            step[0] += 1
            if step[0] % 50 == 0:
                print(f"step {step[0]}: content_loss={content_score.item():.4f} "
                      f"style_loss={style_score.item():.4f}")

            return total_loss

        optimizer.step(closure)

    with torch.no_grad():
        generated.clamp_(0, 1)
    return generated
