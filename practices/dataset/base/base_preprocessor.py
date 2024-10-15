from .. import PREPROCESSOR_BUILDER


__all__ = ["BasePreprocessor"]


@PREPROCESSOR_BUILDER.register("BasePreprocessor")
class BasePreprocessor:
    def __init__(self, **kwargs):
        pass

    def __call__(self, data, label=None):
        raise NotImplementedError
