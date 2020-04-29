class _Task(object):
    def __init__(self, cron='', task_name=''):
        self.cron = cron
        self.task_name = task_name

    def on_success_call(self):
        raise NotImplementedError()

    def on_failed_call(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        if self.run():
            self.on_success_call()
        else:
            self.on_failed_call()
