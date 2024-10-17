import os
import re
import yaml
import json


__all__ = ['load_config', 'save_config']

def __dir__():
    return __all__


ARG_REGEX = r"\$\{\w+:[\s]*[\a-zA-Z0-9\_\-\.]+\}|\$\{\w+\}"

def scan_args_for_string(string: str):
    """
    @brief  扫描字符串中的参数
    @detail 扫描字符串中满足 #{name:default_value} 模式的参数，并返回对应的参数列表

    @param  string 要扫描的字符串
    @return 包含参数名称和默认值的列表
    """
    matches = re.finditer(ARG_REGEX, string)
    args = []

    for match_ in matches:
        start, end = match_.span()
        arg_name = match_.group()[2:-1]
        if ":" in arg_name:
            arg_name, default_value = arg_name.split(":")
        else:
            default_value = None
        
        args.append({
            "name": arg_name,
            "default_value": default_value,
        })
    return args


def format_string(string: str, args: dict):
    """
    @brief  格式化字符串
    @detail 将字符串中的参数替换为对应的值

    @param  string 要格式化的字符串
    @param  args 参数列表
    @return 格式化后的字符串
    """
    replace_intervals = []
    matches = re.finditer(ARG_REGEX, string)
    for match_ in matches:
        start, end = match_.span()
        arg_name = match_.group()[2:-1]
        if ":" in arg_name:
            arg_name, _ = arg_name.split(":")

        value = args[arg_name]
        value = str(value)

        replace_intervals.append((start, end, value))
    
    if len(replace_intervals) == 0:
        return string
    
    start = 0
    end = replace_intervals[0][0]
    final_string = string[start:end]

    for i in range(len(replace_intervals) - 1):
        start, end, value = replace_intervals[i]
        final_string += value

        start = end
        end = replace_intervals[i+1][0]
        final_string += string[start:end]

    start, end, value = replace_intervals[-1]
    final_string += value
    final_string += string[end:]

    return final_string


def load_yaml(file_path):
    def env_var_constructor(loader, node):
        string = loader.construct_scalar(node)
        args = scan_args_for_string(string)
        formatted_args = {}
        for arg in args:
            name = arg["name"]
            value = arg["default_value"]
            env_value = os.getenv(name, value)
            
            if env_value is None:
                raise ValueError(f"Environment variable {name} is not set")
            
            formatted_args[name] = env_value
            
        string = format_string(string, formatted_args)
        return string
            
    yaml.SafeLoader.add_constructor('!env', env_var_constructor)

    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def save_yaml(file_path, data):
    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f)


def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_config(file_path):
    if file_path.endswith('.yaml'):
        return load_yaml(file_path)
    elif file_path.endswith('.json'):
        return load_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")


def save_config(file_path, data):
    if file_path.endswith('.yaml'):
        save_yaml(file_path, data)
    elif file_path.endswith('.json'):
        save_json(file_path, data)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
