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
from practices.dataset.base.base_transform import BaseTransform
from practices.utils.build import get_builder


class TestBaseTransform(unittest.TestCase):
    def test_build_transform(self):
        transform = BaseTransform()

        transform_builder = get_builder("TRANSFORM_BUILDER")
        self.assertTrue("BaseTransform" in transform_builder)

        transform = transform_builder.build("BaseTransform", {})
        self.assertIsInstance(transform, BaseTransform)

        self.assertRaises(NotImplementedError, transform, None)


if __name__ == "__main__":
    unittest.main()

