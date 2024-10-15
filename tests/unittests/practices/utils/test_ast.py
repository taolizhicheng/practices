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
from practices.utils.ast import get_register_info_from_file, get_register_info_from_directory


class TestAST(unittest.TestCase):
    def test_get_register_info_from_file(self):
        path = f"{MODULE_DIR}/practices/dataset/base/base_dataset.py"
        info = get_register_info_from_file(path)
        
        self.assertEquals(len(info), 1)
        self.assertTrue("DATASET_BUILDER" in info)

        self.assertEquals(len(info["DATASET_BUILDER"]), 1)
        index = info["DATASET_BUILDER"][0]

        self.assertEquals(index[0], "BaseDataset")
        self.assertEquals(index[1], "practices.dataset.base.base_dataset")
        self.assertEquals(index[2], "BaseDataset")

    def test_get_register_info_from_directory(self):
        directory = f"{MODULE_DIR}/practices/dataset/base"
        info = get_register_info_from_directory(directory)

        self.assertEquals(len(info), 3)
        self.assertTrue("DATASET_BUILDER" in info)
        self.assertTrue("PREPROCESSOR_BUILDER" in info)
        self.assertTrue("TRANSFORM_BUILDER" in info)

        self.assertEquals(len(info["DATASET_BUILDER"]), 1)
        index = info["DATASET_BUILDER"][0]
        self.assertEquals(index[0], "BaseDataset")
        self.assertEquals(index[1], "practices.dataset.base.base_dataset")
        self.assertEquals(index[2], "BaseDataset")

        self.assertEquals(len(info["PREPROCESSOR_BUILDER"]), 1)
        index = info["PREPROCESSOR_BUILDER"][0]
        self.assertEquals(index[0], "BasePreprocessor")
        self.assertEquals(index[1], "practices.dataset.base.base_preprocessor")
        self.assertEquals(index[2], "BasePreprocessor")

        self.assertEquals(len(info["TRANSFORM_BUILDER"]), 1)
        index = info["TRANSFORM_BUILDER"][0]
        self.assertEquals(index[0], "BaseTransform")
        self.assertEquals(index[1], "practices.dataset.base.base_transform")
        self.assertEquals(index[2], "BaseTransform")


if __name__ == "__main__":
    unittest.main()
