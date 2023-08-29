from .process import Process, ProcessData
import logging
import os


def save(path, process: Process):
    data = process.serialize()
    os.makedirs(procs_path())
    logging.debug(f"Saving file {path}")
    try:
        with open(path, "w") as file:
            file.write(data)
    except (PermissionError, FileNotFoundError, OSError, IOError, Exception) as e:
        print(e)


def read(path):
    try:
        with open(path, "r") as f:
            content = f.read()
            from ruamel.yaml import YAML
            yaml = YAML(typ='rt', pure=True)
            config = yaml.load(content)
            return Process(data=config)
    except FileNotFoundError as e:
        print(e)
    # except Exception as e:
    #     print(e)


def delete(path):
    pass


def path_from_pid(pid):
    base_path = procs_path()
    return f"{base_path}/{pid}.yaml"


def path_from_name(proc_name):
    base_path = procs_path()
    return f"{base_path}/{proc_name}.yaml"


def procs_path():
    home_dir = os.path.expanduser("~")
    return f"{home_dir}/.stelar/procs"
