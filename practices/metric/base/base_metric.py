from .. import METRIC_BUILDER


__all__ = ["BaseMetric"]

def __dir__():
    return __all__


@METRIC_BUILDER.register("BaseMetric")
class BaseMetric:
    def __init__(self, **kwargs):
        pass

    def reset(self):
        raise NotImplementedError
    
    def update(self, pred, label):
        raise NotImplementedError
    
    def compute(self):
        raise NotImplementedError
