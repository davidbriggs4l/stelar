from stelar.monitor.process import Process
import os

def save(path, process: Process):
    pass

def read(path):
    pass

def path_from_pid(pid):
    base_path = procs_path()
    return f"{base_path}/{pid}.json"

def path_from_name(proc_name):
    base_path = procs_path()
    return f"{base_path}/{proc_name}.json"

def procs_path():
    home_dir = os.path.expanduser("~")
    return f"{home_dir}/.stelar/procs"