from practices.utils.build import get_builder


METRIC_BUILDER = get_builder("METRIC_BUILDER")


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
