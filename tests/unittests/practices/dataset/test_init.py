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
import practices.dataset
from practices.utils.build import get_builder


class TestDataset(unittest.TestCase):
    def test_dataset_indices(self):
        builder = get_builder("DATASET_BUILDER")
        self.assertTrue("BaseDataset" in builder)
        self.assertRaises(NotImplementedError, builder.build, "BaseDataset", {})

        builder = get_builder("TRANSFORM_BUILDER")
        self.assertTrue("BaseTransform" in builder)
        transform = builder.build("BaseTransform", {})
        self.assertIsInstance(transform, practices.dataset.base.base_transform.BaseTransform)

        builder = get_builder("PREPROCESSOR_BUILDER")
        self.assertTrue("BasePreprocessor" in builder)
        preprocessor = builder.build("BasePreprocessor", {})
        self.assertIsInstance(preprocessor, practices.dataset.base.base_preprocessor.BasePreprocessor)



if __name__ == "__main__":
    unittest.main()