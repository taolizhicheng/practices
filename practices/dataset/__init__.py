import os

from ..utils.build import build_indices, get_builder


__all__ = ["DATASET_BUILDER", "PREPROCESSOR_BUILDER", "TRANSFORM_BUILDER"]

def __dir__():
    return __all__


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_BUILDER = get_builder("DATASET_BUILDER")
PREPROCESSOR_BUILDER = get_builder("PREPROCESSOR_BUILDER")
TRANSFORM_BUILDER = get_builder("TRANSFORM_BUILDER")

# 预注册base目录下的所有模块
build_indices(os.path.join(THIS_DIR, "base"))
