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

    def step(self, **kwargs):
        raise NotImplementedError
