import os
import sys


sys.dont_write_bytecode = True

MODULE_DIR = os.environ.get('MODULE_DIR', None)
if MODULE_DIR is not None:
    if not sys.path or sys.path[0] != MODULE_DIR:
        sys.path = [MODULE_DIR] + sys.path
else:
    raise ValueError("MODULE_DIR environment variable not set!")


import torch
import unittest
from practices.optimizer.base.base_optimizer import SGD
from practices.utils.build import get_builder


class TestOptimizer(unittest.TestCase):
    def test_optimizer(self):
        builder = get_builder("OPTIMIZER_BUILDER")
        sgd = builder.build("SGD", {"params": [torch.randn(2, 2)], "lr": 0.1})
        self.assertTrue(isinstance(sgd, SGD))


if __name__ == "__main__":
    unittest.main()