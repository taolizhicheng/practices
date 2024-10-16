from .. import METRIC_BUILDER


__all__ = ["BaseMetric"]

def __dir__():
    return __all__


@METRIC_BUILDER.register("BaseMetric")
class BaseMetric:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def reset(self):
        raise NotImplementedError
    
    def update(self, pred, label):
        raise NotImplementedError
    
    def compute(self):
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
