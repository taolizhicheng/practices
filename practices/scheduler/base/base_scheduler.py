import torch.optim as optim

from practices.utils.build import get_builder
from practices.optimizer.base.base_optimizer import BaseOptimizer


SCHEDULER_BUILDER = get_builder("SCHEDULER_BUILDER")


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
