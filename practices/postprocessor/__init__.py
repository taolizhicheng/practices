import os

from ..utils.build import build_indices, get_builder


__all__ = ["POSTPROCESSOR_BUILDER"]

def __dir__():
    return __all__


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
POSTPROCESSOR_BUILDER = get_builder("POSTPROCESSOR_BUILDER")


# 预注册base目录下的所有模块
build_indices(os.path.join(THIS_DIR, "base"))