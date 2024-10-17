from rich.progress import Progress


__all__ = ["ProgressBar"]
def __dir__():
    return __all__


class ProgressBar:
    def __init__(self, show_progress: bool = True):
        self.show_progress = show_progress

    def __enter__(self):
        self.build_progress_bar()
        self.build_tasks()
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        if self.progress_bar is None:
            return

        self.progress_bar.start()

    def stop(self):
        if self.progress_bar is None:
            return

        self.progress_bar.stop()

    def refresh(self):
        if self.progress_bar is None:
            return

        self.progress_bar.refresh()

    def build_progress_bar(self):
        if not self.show_progress:
            self.progress_bar = None
            return

        self.progress_bar = Progress()
    
    def build_tasks(self):
        if self.progress_bar is None:
            self.epoch_task = None
            self.train_step_task = None
            self.eval_step_task = None
            return

        self.epoch_task = self.progress_bar.add_task("[red]Epochs")
        self.train_step_task = self.progress_bar.add_task("[green]Training Steps")
        self.eval_step_task = self.progress_bar.add_task("[green]Validation Steps")
        self.epoch = 0
        self.num_epochs = 0
        self.train_step = 0
        self.num_train_steps = 0
        self.eval_step = 0
        self.num_eval_steps = 0

    def reset_epoch_task(self, num_epochs: int):
        if self.progress_bar is None:
            return

        self.progress_bar.reset(
            self.epoch_task, 
            description=f"[red]Epochs 0/{num_epochs}", 
            total=num_epochs, 
            refresh=True
        )
        self.epoch = 0
        self.num_epochs = num_epochs

    def reset_train_step_task(self, num_train_steps: int):
        if self.progress_bar is None:
            return

        self.progress_bar.reset(
            self.train_step_task, 
            description=f"[green]Training Steps 0/{num_train_steps}", 
            total=num_train_steps, 
            refresh=True
        )
        self.train_step = 0
        self.num_train_steps = num_train_steps

    def reset_eval_step_task(self, num_eval_steps: int):
        if self.progress_bar is None:
            return

        self.progress_bar.reset(
            self.eval_step_task, 
            description=f"[green]Validation Steps 0/{num_eval_steps}", 
            total=num_eval_steps, 
            refresh=True
        )
        self.eval_step = 0
        self.num_eval_steps = num_eval_steps

    def update_epoch_task(self):
        if self.progress_bar is None:
            return

        self.epoch += 1
        self.progress_bar.update(
            self.epoch_task, 
            advance=1, 
            description=f"[red]Epochs {self.epoch}/{self.num_epochs}"
        )

    def update_train_step_task(self):
        if self.progress_bar is None:
            return

        self.train_step += 1
        self.progress_bar.update(
            self.train_step_task, 
            advance=1, 
            description=f"[green]Training Steps {self.train_step}/{self.num_train_steps}"
        )

    def update_eval_step_task(self):
        if self.progress_bar is None:
            return

        self.eval_step += 1
        self.progress_bar.update(
            self.eval_step_task, 
            advance=1, 
            description=f"[green]Validation Steps {self.eval_step}/{self.num_eval_steps}"
        )

