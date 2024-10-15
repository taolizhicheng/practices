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
import practices.scheduler
from practices.utils.build import get_builder


class TestScheduler(unittest.TestCase):
    def test_scheduler_indices(self):
        builder = get_builder("SCHEDULER_BUILDER")
        self.assertTrue("BaseScheduler" in builder)

        scheduler = builder.build(
            "BaseScheduler",
            {"optimizer": torch.optim.SGD([torch.randn(2, 2)], lr=0.1)}
        )
        
        self.assertRaises(NotImplementedError, scheduler.step)


if __name__ == "__main__":
    unittest.main()
