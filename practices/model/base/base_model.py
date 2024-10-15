import torch.nn as nn
from practices.utils.build import get_builder

__all__ = ["BaseModel"]


MODEL_BUILDER = get_builder("MODEL_BUILDER")


@MODEL_BUILDER.register("BaseModel")
class BaseModel(nn.Module):
    def __init__(self, device: str = "cpu", **kwargs):
        super().__init__()
        self.build_model(**kwargs)
        
        self.device = device
        self.to(device)

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, path: str = None):
        torch.save(self.state_dict(), path)

    def load(self, path: str = None):
        self.load_state_dict(torch.load(path), strict=True)

    def build_model(self, **kwargs):
        raise NotImplementedError