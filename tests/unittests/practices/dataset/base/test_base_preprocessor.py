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
from practices.dataset.base.base_preprocessor import BasePreprocessor
from practices.utils.build import get_builder


class TestBasePreprocessor(unittest.TestCase):
    def test_build_preprocessor(self):
        preprocessor = BasePreprocessor()

        preprocessor_builder = get_builder("PREPROCESSOR_BUILDER")
        self.assertTrue("BasePreprocessor" in preprocessor_builder)
        
        preprocessor = preprocessor_builder.build("BasePreprocessor", {})
        self.assertIsInstance(preprocessor, BasePreprocessor)

        self.assertRaises(NotImplementedError, preprocessor, None, None)


if __name__ == "__main__":
    unittest.main()

