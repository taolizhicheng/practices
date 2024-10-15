import os
import sys


sys.dont_write_bytecode = True

MODULE_DIR = os.environ.get('MODULE_DIR', None)
if MODULE_DIR is not None:
    if not sys.path or sys.path[0] != MODULE_DIR:
        sys.path = [MODULE_DIR] + sys.path
else:
    raise ValueError("MODULE_DIR environment variable not set!")


import unittest
import torch
import torch.optim as optim
from practices.utils.build import get_builder
from practices.scheduler.base.base_scheduler import BaseScheduler


class TestBaseScheduler(unittest.TestCase):
    def test_base_scheduler(self):
        scheduler = BaseScheduler(optimizer=optim.SGD([torch.randn(2, 2)], lr=0.1))
        self.assertRaises(NotImplementedError, scheduler.step)

        builder = get_builder("SCHEDULER_BUILDER")
        self.assertTrue("BaseScheduler" in builder)

        scheduler = builder.build("BaseScheduler", {"optimizer": optim.SGD([torch.randn(2, 2)], lr=0.1)})
        self.assertTrue(isinstance(scheduler, BaseScheduler))
        self.assertRaises(NotImplementedError, scheduler.step)


if __name__ == "__main__":
    unittest.main()
