import torch
from torch.utils.tensorboard import SummaryWriter

from ...utils.build import build_instance
from ...utils.load_config import save_config
from .. import TRAINER_BUILDER


__all__ = ["BaseTrainer"]

def __dir__():
    return __all__


@TRAINER_BUILDER.register("BaseTrainer")
class BaseTrainer:
    def __init__(
        self,
        **kwargs
    ):
        self.args = kwargs
        
        # 创建数据集
        self.train_dataset = None
        self.test_dataset = None
        self.build_dataset()

        # 创建模型
        self.model = None
        self.build_model()

        # 创建损失函数
        self.loss = None
        self.build_loss()

        # 创建优化器
        self.optimizer = None
        self.build_optimizer()

        # 创建学习率调度器
        self.scheduler = None
        self.build_scheduler()

        # 创建后处理函数
        self.postprocessor = None
        self.build_postprocessor()

        # 创建指标
        self.metric = None
        self.build_metric()

        # 创建数值记录器
        self.summary_writer = None
        self.build_summary_writer()

        # 其它
        self.global_step = 0

    def build_dataset(self):
        builder_name = "DATASET_BUILDER"

        dataset_args = self.args.get("DATASET")
        train_dataset_args = dataset_args.get("TRAIN")

        train_dataset_name = train_dataset_args.get("NAME")
        train_dataset_args = train_dataset_args.get("ARGS", {})
        self.train_dataset = build_instance(builder_name, name=train_dataset_name, args=train_dataset_args)

        test_dataset_args = dataset_args.get("TEST")
        test_dataset_name = test_dataset_args.get("NAME")
        test_dataset_args = test_dataset_args.get("ARGS", {})
        self.test_dataset = build_instance(builder_name, name=test_dataset_name, args=test_dataset_args)

    def build_model(self):
        builder_name = "MODEL_BUILDER"

        model_args = self.args.get("MODEL")
        model_name = model_args.get("NAME")
        model_args = model_args.get("ARGS", {})
        self.model = build_instance(builder_name, name=model_name, args=model_args)

    def build_loss(self):
        builder_name = "LOSS_BUILDER"

        loss_args = self.args.get("LOSS")
        loss_name = loss_args.get("NAME")
        loss_args = loss_args.get("ARGS", {})
        self.loss = build_instance(builder_name, name=loss_name, args=loss_args)

    def build_optimizer(self):
        builder_name = "OPTIMIZER_BUILDER"

        optimizer_args = self.args.get("OPTIMIZER")
        optimizer_name = optimizer_args.get("NAME")
        optimizer_args = optimizer_args.get("ARGS", {})

        if self.model is None:
            raise ValueError("Model is not built yet!")

        optimizer_args["params"] = self.model.parameters()

        self.optimizer = build_instance(builder_name, name=optimizer_name, args=optimizer_args)
    
    def build_scheduler(self):
        builder_name = "SCHEDULER_BUILDER"

        scheduler_args = self.args.get("SCHEDULER")
        scheduler_name = scheduler_args.get("NAME")
        scheduler_args = scheduler_args.get("ARGS", {})

        if self.optimizer is None:
            raise ValueError("Optimizer is not built yet!")
        
        scheduler_args["optimizer"] = self.optimizer

        self.scheduler = build_instance(builder_name, name=scheduler_name, args=scheduler_args)

    def build_postprocessor(self):
        builder_name = "POSTPROCESSOR_BUILDER"

        postprocessor_args = self.args.get("POSTPROCESSOR")
        postprocessor_name = postprocessor_args.get("NAME")
        postprocessor_args = postprocessor_args.get("ARGS", {})
        self.postprocessor = build_instance(builder_name, name=postprocessor_name, args=postprocessor_args)

    def build_metric(self):
        builder_name = "METRIC_BUILDER"

        metric_args = self.args.get("METRIC")
        metric_name = metric_args.get("NAME")
        metric_args = metric_args.get("ARGS", {})
        self.metric = build_instance(builder_name, name=metric_name, args=metric_args)

    def build_summary_writer(self):
        hyper_args = self.args.get("HYPER", {})
        others_args = hyper_args.get("OTHERS", {})
        summary_dir = others_args.get("summary_dir", None)

        if summary_dir is None:
            return None

        self.summary_writer = SummaryWriter(summary_dir)

    def checkpoint(self, epoch: int, meta: dict = None):
        hyper_args = self.args.get("HYPER", {})
        others_args = hyper_args.get("OTHERS", {})
        checkpoint_dir = others_args.get("checkpoint_dir", None)
        
        if checkpoint_dir is None:
            return

        checkpoint_name = others_args.get("checkpoint_name", "checkpoint")

        checkpoint_path = os.path.join(checkpoint_dir, f"{checkpoint_name}_{epoch}.pth")

        os.makedirs(checkpoint_dir, exist_ok=True)
        torch.save(self.model.state_dict(), checkpoint_path)

        if meta is not None:
            meta_path = os.path.join(checkpoint_dir, f"{checkpoint_name}_{epoch}.json")
            save_config(meta_path, meta)

    def train(self):
        hyper_args = self.args.get("HYPER", {})
        train_args = hyper_args.get("TRAIN", {})

        num_epochs = train_args.get("epochs")
        if num_epochs is None:
            raise ValueError("Epochs is not set!")

        for epoch in range(num_epochs):
            self.before_train_epoch()
            self.train_one_epoch()
            self.after_train_epoch()

            self.before_eval_epoch()
            self.eval_one_epoch()
            self.after_eval_epoch()

            self.checkpoint(epoch)

    def train_one_epoch(self):
        train_dataloader = self.get_train_dataloader()

        self.model.train()
        for data, label in train_dataloader:
            data = data.to(self.model.device)
            label = label.to(self.model.device)
            
            self.optimizer.zero_grad()

            output = self.model(data)
            loss = self.loss(output, label)

            loss.backward()
            self.optimizer.step()
            self.scheduler.step()

            if summary_writer is not None:
                summary_writer.add_scalar("loss", loss.item(), self.global_step)

            self.global_step += 1
    
    def get_train_dataloader(self):
        batch_size = self.train_hyper_args.get("batch_size", 16)
        shuffle = self.train_hyper_args.get("shuffle", True)
        num_workers = self.train_hyper_args.get("num_workers", 4)
        pin_memory = self.train_hyper_args.get("pin_memory", True)
        drop_last = self.train_hyper_args.get("drop_last", True)
        dataloader = torch.utils.data.DataLoader(
            self.train_dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            drop_last=drop_last,
            num_workers=num_workers,
            pin_memory=pin_memory,
        )

        return dataloader

    def eval_one_epoch(self):
        test_dataloader = self.get_test_dataloader()

        self.model.eval()
        self.metric.reset()

        with torch.no_grad():
            for data, label in test_dataloader:
                data = data.to(self.model.device)
                label = label.to(self.model.device)

                output = self.model(data)
                output = self.postprocessor(data, output)

                self.metric.update(output, label)
                metrics = self.metric.compute()

                if summary_writer is not None:
                    for metric_name, metric_value in metrics.items():
                        summary_writer.add_scalar(metric_name, metric_value, self.global_step)

    def get_test_dataloader(self):
        batch_size = self.test_hyper_args.get("batch_size", 1)
        shuffle = self.test_hyper_args.get("shuffle", False)
        num_workers = self.test_hyper_args.get("num_workers", 0)
        pin_memory = self.test_hyper_args.get("pin_memory", False)
        drop_last = self.test_hyper_args.get("drop_last", False)
        dataloader = torch.utils.data.DataLoader(
            self.test_dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            drop_last=drop_last,
            num_workers=num_workers,
            pin_memory=pin_memory,
        )

        return dataloader

    def before_train_epoch(self):
        pass

    def after_train_epoch(self):
        pass

    def before_eval_epoch(self):
        pass

    def after_eval_epoch(self):
        pass