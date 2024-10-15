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
import practices.postprocessor
from practices.utils.build import get_builder


class TestPostprocessor(unittest.TestCase):
    def test_postprocessor_indices(self):
        builder = get_builder("POSTPROCESSOR_BUILDER")
        self.assertTrue("BasePostprocessor" in builder)

        postprocessor = builder.build("BasePostprocessor", {})
        self.assertRaises(NotImplementedError, postprocessor, None)


if __name__ == "__main__":
    unittest.main()
