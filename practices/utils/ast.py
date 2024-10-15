import os
import ast

from .constants import TOP_DIR


__all__ = ["get_register_info_from_file", "get_register_info_from_directory"]


def get_relative_import(path: str):
    if not path.startswith(TOP_DIR):
        raise ValueError("Path is not within the top directory")
    
    if not path.endswith(".py"):
        raise ValueError("Path is not a Python file")

    relative_path = os.path.relpath(path, TOP_DIR)
    base_name = os.path.basename(relative_path)
    if base_name == "__init__.py":
        relative_path = os.path.dirname(relative_path)
    else:
        relative_path = relative_path[:-3]
        
    return relative_path.replace(os.sep, ".")


def get_register_info_from_file(path: str):
    relative_path = get_relative_import(path)

    with open(path, "r") as f:
        content = f.read()

    register_info = {}

    tree = ast.parse(content)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
            cls_of_func_name = node.name
            decorator_info = None
            for decorator in node.decorator_list:
                info = get_decorator_info(decorator)
                if info is None:
                    continue

                decorator_info = info
                break

            if decorator_info is None:
                continue

            builder_name, register_name = decorator_info
            if builder_name not in register_info:
                register_info[builder_name] = []

            register_info[builder_name].append((
                register_name,
                relative_path,
                cls_of_func_name
            ))
        if isinstance(node, ast.Call):
            info = get_register_info(node)
            if info is None:
                continue

            builder_name, register_name, cls_of_func_name = info
            if builder_name not in register_info:
                register_info[builder_name] = []

            register_info[builder_name].append((
                register_name,
                relative_path,
                cls_of_func_name
            ))
    
    return register_info


def get_register_info_from_directory(directory: str):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        raise ValueError("Directory does not exist")

    register_infos = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                register_info = get_register_info_from_file(os.path.join(root, file))
                if register_info is None:
                    continue

                for builder_name, infos in register_info.items():
                    if builder_name not in register_infos:
                        register_infos[builder_name] = []

                    register_infos[builder_name].extend(infos)
        for directory in dirs:
            directory = os.path.join(root, directory)
            directory_register_infos = get_register_info_from_directory(directory)
            for builder_name, infos in directory_register_infos.items():
                if builder_name not in register_infos:
                    register_infos[builder_name] = []

                register_infos[builder_name].extend(infos)

    return register_infos


def get_decorator_info(decorator: ast.Call):
    if not isinstance(decorator, ast.Call):
        return None

    func = decorator.func
    if not isinstance(func, ast.Attribute):
        return None

    attr = func.attr
    if attr != "register":
        return None
    
    register_name = decorator.args[0].value
    builder_name = func.value.id

    return builder_name, register_name


def get_register_info(call: ast.Call):
    if not isinstance(call, ast.Call):
        return None

    func = call.func
    if not isinstance(func, ast.Attribute):
        return None
        
    attr = func.attr
    if attr != "register":
        return None

    if len(call.args) != 2:
        return None

    arg0 = call.args[0]
    if not isinstance(arg0, ast.Constant):
        return None
    
    arg1 = call.args[1]
    if not isinstance(arg1, ast.Name):
        return None

    register_name = arg0.value
    builder_name = func.value.id
    cls_of_func_name = arg1.id
    return builder_name, register_name, cls_of_func_name
    
