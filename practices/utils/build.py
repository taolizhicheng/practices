import os
import importlib
import warnings
from typing import Callable


from practices.utils.check_type import check_class_args, check_func_args, get_callable_type
from practices.utils.ast import get_register_info_from_directory, get_register_info_from_file


__all__ = ['Builder', 'build_indices', 'get_builder', 'build_instance']


@check_class_args
class Builder:
    """
    @brief: 用于注册和获取类或者函数

    @example:
    >>> builder = Builder()
    >>> builder.register('model', MyModel)
    >>> builder.build('model', args)
    MyModel()
    """
    def __init__(self, name: str):
        self._name = name
        self._caches = {}
        self._indices = {}
        

    def __contains__(self, name: str):
        return name in self._caches or name in self._indices

    def __getitem__(self, name: str):
        return self.get(name)

    def __iter__(self):
        return iter(self._caches)
    
    def __len__(self):
        return len(self._caches)

    def __str__(self):
        string = f"Builder({self._name})\n"
        string += f"  Registered:\n"
        for i, (name, func_or_class) in enumerate(self._caches.items()):
            string += f"    {i}: {name}\n"
        string += f"  Indices:\n"
        for i, (name, (module_path, module_name)) in enumerate(self._indices.items()):
            string += f"    {i}: {name} -> {module_path}.{module_name}\n"
        return string

    def __repr__(self):
        return self.__str__()

    def get(self, name: str):
        """
        @brief: 根据name从builder中获取对应的类或者函数

        @param name: 名称
        @return: 类或者函数
        """
        if name not in self._caches:
            if name not in self._indices:
                raise ValueError(f"{name} not registered in {self.name}")
            
            # try lazy import
            module_path, module_name = self._indices[name]
            # what if the module is not decorated?
            if module_name is None:
                module = importlib.import_module(module_path)
                if name not in self._caches:
                    raise ValueError(f"Module {module_path} not decorated")
            elif module_name is not None:
                module = importlib.import_module(module_path)
                module = getattr(module, module_name)
                if name not in self._caches:
                    warnings.warn(f"Module {module_path} not decorated, register {module_name} as {name}")
                    self._caches[name] = module

        return self._caches[name]

    def build(self, name: str, args: dict = None):
        """
        @brief: 根据name从builder中获取对应的类或者函数，并返回

        @param name: 名称
        @param args: 参数
        @return: 类或者函数

        @example:
        >>> builder = Builder()
        >>> builder.register('model', MyModel)
        >>> builder.build('model', args)
        MyModel()
        """
        if args is None:
            args = {}

        class_or_func = self.get(name)
        callable_type = get_callable_type(class_or_func)
        if callable_type == 'class':
            class_instance = check_class_args(class_or_func)
            return class_instance(**args)
        elif callable_type == 'function':
            func_instance = check_func_args(class_or_func)
            return func_instance(**args)
        else:
            raise ValueError(f"Unknown callable type: {callable_type}")

    def register(self, name: str, func_or_class: Callable = None, override: bool = False):
        """
        @brief: 将name对应的类或者函数注册到builder中

        @param name: 名称
        @param func_or_class: 类或者函数
        @param override: 是否覆盖已有的注册

        @example:
        >>> # 直接注册
        >>> builder = Builder()
        >>> builder.register('model', MyModel)
        >>> builder.build('model', **kwargs)
        >>> 
        >>> # 装饰器用法
        >>> @builder.register('model')
        >>> class MyModel:
        >>>     def __init__(self, **kwargs):
        >>>         pass
        >>> builder.build('model', **kwargs)
        """
        if name in self._caches and not override:
            raise ValueError(f"Model {name} already registered")

        if func_or_class is not None:
            self._caches[name] = func_or_class
        else:
            def decorator(func_or_class):
                self._caches[name] = func_or_class
                return func_or_class
            return decorator
    
    def register_index(self, name: str, path: str, module: str, override: bool=False):
        if name in self._indices and not override:
            raise ValueError(f"{name} already registered")
        
        if path is None:
            raise ValueError(f"Path is None")

        self._indices[name] = (path, module)

    @property
    def name(self):
        return self._name


DATASET_BUILDER = Builder("DATASET")
PREPROCESSOR_BUILDER = Builder("PREPROCESSOR")
TRANSFORM_BUILDER = Builder("TRANSFORM")
MODEL_BUILDER = Builder("MODEL")
LOSS_BUILDER = Builder("LOSS")
OPTIMIZER_BUILDER = Builder("OPTIMIZER")
SCHEDULER_BUILDER = Builder("SCHEDULER")
POSTPROCESSOR_BUILDER = Builder("POSTPROCESSOR")
METRIC_BUILDER = Builder("METRIC")

TRAINER_BUILDER = Builder("TRAINER")


def get_builder(name: str):
    if name == "DATASET_BUILDER":
        return DATASET_BUILDER
    elif name == "PREPROCESSOR_BUILDER":
        return PREPROCESSOR_BUILDER
    elif name == "TRANSFORM_BUILDER":
        return TRANSFORM_BUILDER
    elif name == "MODEL_BUILDER":
        return MODEL_BUILDER
    elif name == "LOSS_BUILDER":
        return LOSS_BUILDER
    elif name == "OPTIMIZER_BUILDER":
        return OPTIMIZER_BUILDER
    elif name == "SCHEDULER_BUILDER":
        return SCHEDULER_BUILDER
    elif name == "POSTPROCESSOR_BUILDER":
        return POSTPROCESSOR_BUILDER
    elif name == "METRIC_BUILDER":
        return METRIC_BUILDER
    elif name == "TRAINER_BUILDER":
        return TRAINER_BUILDER
    else:
        raise ValueError(f"Unknown builder name: {name}")


def build_indices(path: str):
    if os.path.isdir(path):
        register_infos = get_register_info_from_directory(path)
    elif os.path.isfile(path):
        register_infos = get_register_info_from_file(path)
    else:
        raise ValueError(f"Unknown path type: {path}")

    for builder_name, infos in register_infos.items():
        builder = get_builder(builder_name)

        for info in infos:
            name, module_path, module_name = info
            builder.register_index(name, module_path, module_name)


def build_instance(builder_name: str, name: str, args: dict):
    builder = get_builder(builder_name)
    return builder.build(name, args)
