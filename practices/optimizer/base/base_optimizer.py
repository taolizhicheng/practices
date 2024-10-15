import torch.optim as optim

from .. import OPTIMIZER_BUILDER


__all__ = [
    "BaseOptimizer",
    "Optimizer",
    "ASGD",
    "Adadelta",
    "Adagrad",
    "Adam",
    "AdamW",
    "Adamax",
    "LBFGS",
    "NAdam",
    "RAdam",
    "RMSprop",
    "Rprop",
    "SGD",
    "SparseAdam",
]

def __dir__():
    return __all__


BaseOptimizer = optim.Optimizer
OPTIMIZER_BUILDER.register("BaseOptimizer", BaseOptimizer)

Optimizer = optim.Optimizer
OPTIMIZER_BUILDER.register("Optimizer", Optimizer)

ASGD = optim.ASGD
OPTIMIZER_BUILDER.register("ASGD", ASGD)

Adadelta = optim.Adadelta
OPTIMIZER_BUILDER.register("Adadelta", Adadelta)

Adagrad = optim.Adagrad
OPTIMIZER_BUILDER.register("Adagrad", Adagrad)

Adam = optim.Adam
OPTIMIZER_BUILDER.register("Adam", Adam)

AdamW = optim.AdamW
OPTIMIZER_BUILDER.register("AdamW", AdamW)

Adamax = optim.Adamax
OPTIMIZER_BUILDER.register("Adamax", Adamax)

LBFGS = optim.LBFGS
OPTIMIZER_BUILDER.register("LBFGS", LBFGS)

NAdam = optim.NAdam
OPTIMIZER_BUILDER.register("NAdam", NAdam)

RAdam = optim.RAdam
OPTIMIZER_BUILDER.register("RAdam", RAdam)

RMSprop = optim.RMSprop
OPTIMIZER_BUILDER.register("RMSprop", RMSprop)

Rprop = optim.Rprop
OPTIMIZER_BUILDER.register("Rprop", Rprop)

SGD = optim.SGD
OPTIMIZER_BUILDER.register("SGD", SGD)

SparseAdam = optim.SparseAdam
OPTIMIZER_BUILDER.register("SparseAdam", SparseAdam)