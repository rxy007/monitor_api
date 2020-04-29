from task import _Task
from email_util import send_eamil
from logger_util import write_log


class Task(_Task):
    def on_failed_call(self):
        write_log(self.task_name, 'task failed, start send email...')
        to = []
        cc = []
        subject = '任务失败'
        html_content = 'example任务失败，请检查'
        mime_charset = 'utf8'
        send_eamil(to, subject, html_content, retry=3, cc=cc, mime_charset=mime_charset)
        write_log(self.task_name, 'done send email.')

    def on_success_call(self):
        write_log(self.task_name, 'task successful, start send email...')
        to = []
        cc = []
        subject = '任务成功'
        html_content = 'example任务执行成功'
        mime_charset = 'utf8'
        send_eamil(to, subject, html_content, retry=3, cc=cc, mime_charset=mime_charset)
        write_log(self.task_name, 'done send email.')

    def run(self):
        try:
            assert 1+1 == 2
        except AssertionError:
            return False
        return True

task = Task(cron='* * * * *', task_name='example')
