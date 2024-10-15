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
from practices.utils.build import Builder


class TestBuildFuncArgs(unittest.TestCase):
    def test_build_func(self):
        builder = Builder('callable')
        self.assertEqual(builder.name, 'callable')

        def my_func1(a: int, b: str):
            return 1

        builder.register('my_func1', my_func1)
        self.assertRaises(TypeError, builder.build, 'my_func1', {"a": 1, "b": 2})
        self.assertEqual(builder.build('my_func1', {"a": 1, "b": "2"}), 1)

        @builder.register('my_func2')
        def my_func2(a: int, b: str):
            return 2

        self.assertEqual(builder.build('my_func2', {"a": 1, "b": "2"}), 2)

        @builder.register('my_func2', override=True)
        def my_func2(a: int, b: str):
            return 3

        self.assertEqual(builder.build('my_func2', {"a": 1, "b": "2"}), 3)

        self.assertEquals(len(builder), 2)
        self.assertTrue('my_func1' in builder)
    
    def test_build_class(self):
        builder = Builder('callable')

        class MyClass:
            def __init__(self, a: int, b: str):
                self.a = a
                self.b = b

        builder.register('my_class', MyClass)
        self.assertRaises(TypeError, builder.build, 'my_class', {"a": 1, "b": 2})
        class_instance = builder.build('my_class', {"a": 1, "b": "2"})
        self.assertIsInstance(class_instance, MyClass)
        self.assertEqual(class_instance.a, 1)
        self.assertEqual(class_instance.b, "2")


if __name__ == '__main__':
    unittest.main()
