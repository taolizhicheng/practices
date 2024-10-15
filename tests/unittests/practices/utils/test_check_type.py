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
from practices.utils.check_type import check_func_args, check_class_args, get_callable_type


class TestCheckFuncArgs(unittest.TestCase):
    def test_check_func_args(self):
        def my_func1(a: int, b: str):
            pass

        wrapper = check_func_args(my_func1)
        self.assertRaises(TypeError, wrapper, 1, 2)
        wrapper(1, '2')

        @check_func_args
        def my_func2(a: int, b: str):
            pass

        self.assertRaises(TypeError, my_func2, 1, 2)
        my_func2(1, '2')


class TestCheckClassArgs(unittest.TestCase):
    def test_check_class_args(self):
        class MyClass1:
            def __init__(self, a: int, b: str):
                pass

        wrapper = check_class_args(MyClass1)
        self.assertRaises(TypeError, wrapper, 1, 2)
        wrapper(1, '2')

        @check_class_args
        class MyClass2:
            def __init__(self, a: int, b: str):
                pass

        self.assertRaises(TypeError, MyClass2, 1, 2)
        MyClass2(1, '2')


class TestGetCallableType(unittest.TestCase):
    def test_get_callable_type(self):
        def my_func():
            pass

        class MyClass:
            pass

        self.assertEqual(get_callable_type(my_func), 'function')
        self.assertEqual(get_callable_type(MyClass), 'class')
        self.assertRaises(TypeError, get_callable_type, 1)


if __name__ == '__main__':
    unittest.main()

