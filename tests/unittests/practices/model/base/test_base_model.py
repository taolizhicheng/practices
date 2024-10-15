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
from practices.model.base.base_model import BaseModel
from practices.utils.build import get_builder


class TestBaseModel(unittest.TestCase):
    def test_base_model(self):
        self.assertRaises(NotImplementedError, BaseModel, device="cuda")

        model_builder = get_builder("MODEL_BUILDER")
        self.assertTrue("BaseModel" in model_builder)

        self.assertRaises(NotImplementedError, model_builder.build, "BaseModel", {"devide": "cuda"})


if __name__ == "__main__":
    unittest.main()
