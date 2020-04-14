import importlib
import os
import tornado
from logger_util import write_log

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.triggers.cron import CronTrigger

with open('_pid', 'w') as f:
    f.write(str(os.getpid()) + '\n')


scheduler_dict = {}
tasks = []


def get_task(path='tasks'):
    write_log('main', 'start get task...')
    tmp_files = [file for file in os.listdir('tasks') if file.endswith('py')]
    for file in tmp_files:
        file_path = os.path.join(path, file)
        last_change_time = os.stat(file_path).st_mtime
        task = path+'.'+file[:-3]
        if task not in tasks:
            module = importlib.import_module(task)
            scheduler_dict[task] = [module, 'new', last_change_time]
            tasks.append(task)
        elif scheduler_dict[task][2] < last_change_time:
            module = importlib.reload(task)
            scheduler_dict[task][0] = module
            scheduler_dict[task][1] = 'update'
            scheduler_dict[task][2] = last_change_time

    tmp_tasks = [path+'.'+file[:-3] for file in tmp_files]
    stop_tasks = set(tasks)-set(tmp_tasks)

    for task in stop_tasks:
        tasks.remove(task)
        scheduler_dict[task][1] = 'stop'

    scheduler_task()
    write_log('main', 'get task done!')


def scheduler_task():
    write_log('main', 'start scheduler task...')
    stop_tasks = []
    for k, v in scheduler_dict.items():
        if v[1] == 'new':
            cron = getattr(v[0], 'cron')
            job = scheduler.add_job(run_task, CronTrigger.from_crontab(cron), kwargs={'name': k, 'module': v[0]})
            v[1] = 'schedule'
            v.append(job.id)
            write_log('main', 'creat new job ===> name: ' + k + '===> cron: ' + cron)
        elif v[1] == 'update':
            scheduler.remove_job(v[3])
            cron = getattr(v[0], 'cron')
            job = scheduler.add_job(run_task, CronTrigger.from_crontab(cron), kwargs={'name': k, 'module': v[0]})
            v[1] = 'schedule'
            v[3] = job.id
            write_log('main', 'update job ===> name: ' + k + '===> cron: ' + cron)
        elif v[1] == 'stop':
            scheduler.remove_job(v[3])
            stop_tasks.append(k)
    for stop_task in stop_tasks:
        scheduler_dict.pop(stop_task)
        write_log('main', 'stop job ===> name: ' + stop_task)
    write_log('main', 'scheduler task done!')


def run_task(name, module):
    run_function = getattr(module, 'run')
    write_log('main', 'start run task===> ' + name)
    run_function()
    write_log('main', 'task done ===> ' + name)


scheduler = TornadoScheduler()
scheduler.add_job(get_task, 'interval', seconds=20)
scheduler.start()

tornado.ioloop.IOLoop.instance().start()
