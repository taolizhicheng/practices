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
from practices.loss.base.base_loss import BaseLoss
from practices.utils.build import get_builder


class TestBaseLoss(unittest.TestCase):
    def test_base_loss(self):
        loss = BaseLoss()
        self.assertRaises(NotImplementedError, loss.forward, None, None)

        loss_builder = get_builder("LOSS_BUILDER")
        self.assertTrue("BaseLoss" in loss_builder)

        self.assertIsInstance(loss_builder.build("BaseLoss", {}), BaseLoss)


if __name__ == "__main__":
    unittest.main()