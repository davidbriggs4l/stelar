import os
from ruamel.yaml import YAML
from typing import List
from .monitor.process import ProcessData, Process


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
                return None
        except FileNotFoundError:
            print("No stelar.yaml file found!")

    def list_procs(self) -> List[Process]:
        procs = self.process.copy()
        return [Process(data=data) for data in procs]
