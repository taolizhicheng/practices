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
import practices.loss
from practices.utils.build import get_builder


class TestLoss(unittest.TestCase):
    def test_loss_indices(self):
        builder = get_builder("LOSS_BUILDER")
        self.assertTrue("BaseLoss" in builder)

        loss = builder.build("BaseLoss", {})
        self.assertRaises(NotImplementedError, loss.forward, None, None)


if __name__ == "__main__":
    unittest.main()
