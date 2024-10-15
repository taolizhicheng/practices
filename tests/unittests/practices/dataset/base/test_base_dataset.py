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
from practices.dataset.base.base_dataset import BaseDataset
from practices.utils.build import get_builder


class TestBaseDataset(unittest.TestCase):
    def test_build_dataset(self):
        self.assertRaises(NotImplementedError, BaseDataset)

        dataset_builder = get_builder("DATASET_BUILDER")
        self.assertTrue("BaseDataset" in dataset_builder)

        self.assertRaises(NotImplementedError, dataset_builder.build, "BaseDataset", {})


if __name__ == "__main__":
    unittest.main()
