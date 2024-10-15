from .. import POSTPROCESSOR_BUILDER


__all__ = ["BasePostprocessor"]

def __dir__():
    return __all__


@POSTPROCESSOR_BUILDER.register("BasePostprocessor")
class BasePostprocessor:
    def __init__(self, **kwargs):
        pass

    def __call__(self, output):
        raise NotImplementedError

