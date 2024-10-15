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
from practices.metric.base.base_metric import BaseMetric


class TestBaseMetric(unittest.TestCase):
    def test_base_metric(self):
        metric = BaseMetric()
        
        self.assertRaises(NotImplementedError, metric.reset)
        self.assertRaises(NotImplementedError, metric.update, None, None)
        self.assertRaises(NotImplementedError, metric.compute)

        builder = get_builder("METRIC_BUILDER")
        self.assertTrue("BaseMetric" in builder)

        metric = builder.build("BaseMetric", {})
        self.assertIsInstance(metric, BaseMetric)
        self.assertRaises(NotImplementedError, metric.reset)
        self.assertRaises(NotImplementedError, metric.update, None, None)
        self.assertRaises(NotImplementedError, metric.compute)


if __name__ == "__main__":
    unittest.main()
