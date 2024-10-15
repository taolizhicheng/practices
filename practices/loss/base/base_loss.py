import torch.nn as nn
from practices.utils.build import get_builder


__all__ = ["BaseLoss"]


LOSS_BUILDER = get_builder("LOSS_BUILDER")


@LOSS_BUILDER.register("BaseLoss")
class BaseLoss(nn.Module):
    def __init__(self, **kwargs):
        super().__init__()

    def forward(self, output, label):
        raise NotImplementedError
