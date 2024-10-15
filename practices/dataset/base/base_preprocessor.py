from practices.utils.build import get_builder


PREPROCESSOR_BUILDER = get_builder("PREPROCESSOR_BUILDER")


@PREPROCESSOR_BUILDER.register("BasePreprocessor")
class BasePreprocessor:
    def __init__(self, **kwargs):
        pass

    def __call__(self, data, label=None):
        raise NotImplementedError
