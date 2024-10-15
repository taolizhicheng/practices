from .. import TRANSFORM_BUILDER


__all__ = ["BaseTransform"]


@TRANSFORM_BUILDER.register("BaseTransform")
class BaseTransform:
    def __init__(self, **kwargs):
        pass

    def __call__(self, data, label=None):
        raise NotImplementedError
