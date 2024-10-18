# 深度学习组件框架

继承基础组件，实现自定义组件，并通过配置完成模型的训练和测试。

基础组件内容：
- BaseDataset
- BasePreprocessor
- BaseTransform
- BaseModel
- BaseLoss
- BaseOptimizer
- BaseScheduler
- BasePreprocessor
- BaseMetric
- BaseTrainer

## 下载安装

下载：
```shell
git clone https://github.com/taolizhicheng/practices.git
```

安装：
```shell
cd practices/
conda create -n [env_name] python=3.10
conda activate [env_name]
pip install .
```

## 使用


假设有另外的深度学习项目，以图像分类为例，目录结构如下：

```
├── project/
    ├── data/
        ├── train/
            ├── images/
                ├── image1.jpg
                ├── image2.jpg
                ├── ...
            ├── labels/
                ├── image1.json
                ├── image2.json
                ├── ...
        ├── val/
            ├── images/
                ├── image1.jpg
                ├── image2.jpg
                ├── ...
            ├── labels/
                ├── image1.json
                ├── image2.json
                ├── ...
    ├── configs/
        ├── baseline.yaml
    ├── project/
        ├── __init__.py
        ├── dataset/
            ├── __init__.py 
            ├── dataset.py
            ├── preprocessor.py
            ├── transforms.py
        ├── model/
            ├── __init__.py
            ├── model.py
        ├── loss/
            ├── __init__.py
            ├── loss.py
        ├── postprocessor/
            ├── __init__.py
            ├── postprocessor.py
        ├── metric/
            ├── __init__.py
            ├── metric.py
        ├── trainer/
            ├── __init__.py
            ├── trainer.py
```

### 使用方法（以`dataset/`目录为例）

在`project/__init__.py`中添加以下内容：
```python
import project.dataset
# 其它模块类似
```

在`project/dataset/__init__.py`中添加以下内容：
```python
import os
from practices.dataset import DATASET_BUILDER, PREPROCESSOR_BUILDER, TRANSFORM_BUILDER
from practices.utils.builder import build_index

__all__ = ['DATASET_BUILDER', 'PREPROCESSOR_BUILDER', 'TRANSFORM_BUILDER']
def __dir__():
    return __all__

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

build_index(THIS_DIR)
```


`dataset/dataset.py`用于实现`Dataset`类，继承自`BaseDataset`，需要完成`build_data`方法和`get_data`方法。


```python
import os
from . import DATASET_BUILDER
from practices.dataset.base.base_dataset import BaseDataset


@DATASET_BUILDER.build("ImageClassificationDataset")
class ImageClassificationDataset(BaseDataset):
    def __init__(self, data_dir, **kwargs):
        self.data_dir = data_dir
        super().__init__(
            **kwargs
        )
    
    def build_data(self):
        self.data = []
        for image_path in glob.glob(os.path.join(self.data_dir, 'images/*.jpg')):
            self.data.append({
                'image': image_path,
                'label': os.path.join(self.data_dir, 'labels/', os.path.basename(image_path).replace('.jpg', '.json'))
            })
    
    def get_data(self, index):
        single_data = self.data[index]
        image = cv2.imread(single_data['image'])
        label = json.load(open(single_data['label']))
        return image, label

```

`dataset/preprocessor.py`用于实现`Preprocessor`类，继承自`BasePreprocessor`，需要完成`__init__`方法和`__call__`方法。

```python
from . import PREPROCESSOR_BUILDER
from practices.dataset.base.base_preprocessor import BasePreprocessor

@PREPROCESSOR_BUILDER.build("ImageClassificationPreprocessor")
class ImageClassificationPreprocessor(BasePreprocessor):
    def __init__(self, image_size):
        self.image_size = image_size
    
    def __call__(self, image, label):
        image = cv2.resize(image, self.image_size)
        return image, label
```

`dataset/transforms.py`用于实现`Transform`类，继承自`BaseTransform`，需要完成`__init__`方法和`__call__`方法。

```python
from . import TRANSFORM_BUILDER
from practices.dataset.base.base_transform import BaseTransform

@TRANSFORM_BUILDER.build("RandomFlip")
class RandomFlip(BaseTransform):
    def __init__(self, prob=0.5):
        self.prob = prob
    
    def __call__(self, image, label):
        if random.random() < self.prob:
            image = cv2.flip(image, 1)
        return image, label

# 其它transforms...
```

这样一来，就可以通过配置进行实例化，如下：
```python
import project

config = {
    "DATASET": {
        "NAME": "ImageClassificationDataset",
        "ARGS": {
            "data_dir": "data/train",
            "PREPROCESSOR": {
                "NAME": "ImageClassificationPreprocessor",
                "ARGS": {
                    "image_size": (224, 224)
                }
            },
            "TRANSFORMS": [
                {"NAME": "RandomFlip", "PROB": 0.5},
                {"NAME": "RandomRotate", "ANGLE": 10},
            ]
        }
    }
}

name = config["DATASET"]["NAME"]
args = config["DATASET"]["ARGS"]
dataset = project.dataset.DATASET_BUILDER.build(name, args)

data, label = dataset[0]
```
