from .. import POSTPROCESSOR_BUILDER


__all__ = ["BasePostprocessor"]

def __dir__():
    return __all__


@POSTPROCESSOR_BUILDER.register("BasePostprocessor")
class BasePostprocessor:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, output):
        raise NotImplementedError

    def __str__(self):
        string = f"{self.__class__.__name__}("
        for key, value in self.kwargs.items():
            string += f"\n  {key}={value},"
        if len(self.kwargs) > 0:
            string = string[:-1]
            string += "\n)" 
        else:
            string += ")"
        return string

    def __repr__(self):
        return self.__str__()
