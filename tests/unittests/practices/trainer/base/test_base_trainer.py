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
from practices.trainer.base.base_trainer import BaseTrainer
from practices.utils.load_config import load_config


class TestBaseTrainer(unittest.TestCase):
    def test_base_trainer(self):
        config = load_config(f"{MODULE_DIR}/configs/base/base.yaml")
        self.assertRaises(NotImplementedError, BaseTrainer, **config)
    

if __name__ == "__main__":
    unittest.main()
