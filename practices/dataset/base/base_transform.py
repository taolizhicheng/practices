from practices.utils.build import get_builder


TRANSFORM_BUILDER = get_builder("TRANSFORM_BUILDER")


@TRANSFORM_BUILDER.register("BaseTransform")
class BaseTransform:
    def __init__(self, **kwargs):
        pass

    def __call__(self, data, label=None):
        raise NotImplementedError
