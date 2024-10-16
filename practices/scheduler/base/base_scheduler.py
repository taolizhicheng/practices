import torch.optim as optim

from .. import SCHEDULER_BUILDER
from ...optimizer.base.base_optimizer import BaseOptimizer


__all__ = ["BaseScheduler"]

def __dir__():
    return __all__


@SCHEDULER_BUILDER.register("BaseScheduler")
class BaseScheduler:
    def __init__(
        self,
        optimizer: BaseOptimizer,
        **kwargs
    ):
        self.optimizer = optimizer
        self.current_step = -1
        self.kwargs = kwargs

    def step(self, **kwargs):
        raise NotImplementedError

    def __str__(self):
        string = f"{self.__class__.__name__}("
        string += f"\n  optimizer={self.optimizer.__class__.__name__},"
        for key, value in self.kwargs.items():
            string += f"\n  {key}={value},"
        string += "\n)"
        return string

    def __repr__(self):
        return self.__str__()
