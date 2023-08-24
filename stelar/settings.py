import os
import uvloop
from ruamel.yaml import YAML
from typing import List
from monitor.process import ProcessData, Process


class Settings:
    def __init__(self, process: List[ProcessData]) -> None:
        self.process = process

    def read(loop: uvloop.Loop):
        try:
            with open(f"{os.getcwd()}/stelar.yaml", "r") as f:
                yaml = YAML()
                return yaml.load(f)
        except FileNotFoundError:
            print("No stelar.yaml file found!")
            loop.stop()
