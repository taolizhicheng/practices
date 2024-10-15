import yaml
import json


__all__ = ['load_config', 'save_config']

def __dir__():
    return __all__


def load_yaml(file_path):
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
