from .. import DATASET_BUILDER, PREPROCESSOR_BUILDER, TRANSFORM_BUILDER


__all__ = ["BaseDataset"]


@DATASET_BUILDER.register('BaseDataset')
class BaseDataset:
    def __init__(self, **kwargs):
        preprocessor_args = kwargs.pop("PREPROCESSOR", None)
        transforms_args = kwargs.pop("TRANSFORMS", None)
        self.preprocessor = self.build_preprocessor(preprocessor_args)
        self.transforms = self.build_transforms(transforms_args)

        self.build_data(**kwargs)

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index):
        data = self.get_data(index)
        if not isinstance(data, tuple):
            raise ValueError("Data must be a tuple of (data, label) or (data,)")
        # may have label
        if len(data) == 2:
            data, label = data
        else:
            label = None
        if self.preprocessor is not None:
            data, label = self.preprocessor(data, label)
        if self.transforms is not None:
            for transform in self.transforms:
                data, label = transform(data, label)
        
        if label is not None:
            return data, label
        else:
            return data

    def build_preprocessor(self, preprocessor_args: dict = None):
        if preprocessor_args is None:
            return None

        name = preprocessor_args.get("NAME")
        args = preprocessor_args.get("ARGS", {})
        return PREPROCESSOR_BUILDER.build(name, args)

    def build_transforms(self, transforms_args: list = None):
        if transforms_args is None:
            return []

        transform_list = []
        for transform_arg in transforms_args:
            name = transform_arg.get("NAME")
            args = transform_arg.get("ARGS", {})
            transform_list.append(TRANSFORM_BUILDER.build(name, args))
        return transform_list

    def build_data(self, **kwargs):
        raise NotImplementedError

    def get_data(self, index):
        raise NotImplementedError
