import torch.nn as nn
from .. import LOSS_BUILDER


__all__ = ["BaseLoss"]


@LOSS_BUILDER.register("BaseLoss")
class BaseLoss(nn.Module):
    def __init__(self, **kwargs):
        super().__init__()

    def forward(self, output, label):
        raise NotImplementedError
