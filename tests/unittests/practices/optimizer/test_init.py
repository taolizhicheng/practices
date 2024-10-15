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
import practices.optimizer
from practices.utils.build import get_builder


class TestOptimizer(unittest.TestCase):
    def test_optimizer_indices(self):
        builder = get_builder("OPTIMIZER_BUILDER")
        self.assertTrue("BaseOptimizer" in builder)
        self.assertTrue("Optimizer" in builder)
        self.assertTrue("ASGD" in builder)
        self.assertTrue("Adadelta" in builder)
        self.assertTrue("Adagrad" in builder)
        self.assertTrue("Adam" in builder)
        self.assertTrue("AdamW" in builder)
        self.assertTrue("Adamax" in builder)
        self.assertTrue("LBFGS" in builder)
        self.assertTrue("NAdam" in builder)
        self.assertTrue("RAdam" in builder)
        self.assertTrue("RMSprop" in builder)
        self.assertTrue("Rprop" in builder)
        self.assertTrue("SGD" in builder)
        self.assertTrue("SparseAdam" in builder)

        self.assertEquals(len(builder), 15)

if __name__ == "__main__":
    unittest.main()
