from practices.utils.build import get_builder


POSTPROCESSOR_BUILDER = get_builder("POSTPROCESSOR_BUILDER")


@POSTPROCESSOR_BUILDER.register("BasePostprocessor")
class BasePostprocessor:
    def __init__(self, **kwargs):
        pass

    def __call__(self, output):
        raise NotImplementedError

