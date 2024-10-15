import torch.nn as nn
from .. import MODEL_BUILDER


__all__ = ["BaseModel"]

def __dir__():
    return __all__


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