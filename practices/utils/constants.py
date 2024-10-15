import os


__all__ = ["TOP_DIR"]

def __dir__():
    return __all__


TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
