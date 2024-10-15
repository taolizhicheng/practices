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
from practices.utils.build import get_builder
from practices.postprocessor.base.base_postprocessor import BasePostprocessor


class TestBasePostprocessor(unittest.TestCase):
    def test_base_postprocessor(self):
        postprocessor = BasePostprocessor()
        self.assertRaises(NotImplementedError, postprocessor, None)

        builder = get_builder("POSTPROCESSOR_BUILDER")
        self.assertTrue("BasePostprocessor" in builder)

        postprocessor = builder.build("BasePostprocessor", {})
        self.assertIsInstance(postprocessor, BasePostprocessor)


if __name__ == "__main__":
    unittest.main()
