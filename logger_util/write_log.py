import os
import datetime

_log_conf = {}


def conf_log(name, size=20*1024*1024):
    _log_conf[name] = size


def check_log_file(name):
    log_file = os.path.join('logs', name, 'out')
    if os.path.exists(log_file):
        size = os.stat(log_file).st_size
        return size < _log_conf[name]
    return True


def rename_log_file(name):
    log_file = os.path.join('logs', name, 'out')
    dest_log_file = os.path.join('logs', name, 'out') + str(len(os.listdir(os.path.join('logs', name))))
    os.rename(log_file, dest_log_file)


def write_log(name, message):
    if name not in _log_conf:
        conf_log(name)
    log_dir = os.path.join('logs', name)
    os.makedirs(log_dir, exist_ok=True)
    if not check_log_file(name):
        rename_log_file(name)
    with open(os.path.join('logs', name, 'out'), 'a+', encoding='utf8') as f:
        log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(log_time + ' ' + message + '\n')

