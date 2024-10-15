import os

from practices.utils.build import build_indices


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


# 预注册base目录下的所有模块
build_indices(os.path.join(THIS_DIR, "base"))
