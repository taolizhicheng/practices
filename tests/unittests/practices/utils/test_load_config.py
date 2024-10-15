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
import tempfile
from practices.utils.load_config import load_config


class TestLoadConfig(unittest.TestCase):
    def test_load_config(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            f.write(b'{"a": 1, "b": 2}')
            f.flush()
            f.seek(0)
            self.assertEqual(load_config(f.name), {'a': 1, 'b': 2})


if __name__ == '__main__':
    unittest.main()