import os
from ruamel.yaml import YAML
from typing import List
from .monitor.process import ProcessData, Process
import logging


class Settings:
    def __init__(self, process: List[ProcessData] = None) -> None:
        self.process = process

    def read():
        try:
            with open(f"{os.getcwd()}/stelar.yaml", "r") as f:
                yaml = YAML(pure=True, typ='rt')
                config = yaml.load(f)
                hasprocess = config is not None and 'process' in config
                if hasprocess:
                    return Settings(process=[ProcessData(**data) for data in config['process']])
                print("No process to run!")
                exit(0)
        except FileNotFoundError:
            print("No stelar.yaml file found!")

    def list_procs(self) -> List[Process]:
        procs = self.process.copy()
        return [Process(data=data) for data in procs]


async def start(process: Process):
    child = await process.spawn()
    # status = await chid.wait()
    if child is not None:
        status = await child.wait()
        if status > 0:
            logging.debug("Child process ended with errors, retry!")
            process.increament_retires()
            if process.should_retry():
                start(process=process)
            else:
                logging.warning("Too many retries, stopping!")
        else:
            logging.debug("Child process ended with no errors.")


async def async_filter(x, y):
    list(filter(await async_filter, entry))
    return


async def list_processes(all):
    from .monitor import file
    base_path = file.procs_path()
    try:
        entry = []
        items = os.listdir(base_path)
        for item in items:
            entry.append(file.read(path=item))
        return
    except Exception as e:
        print(e)
        exit(0)
