from typing import List

CmdArgs = List[List[str]]
CmdEnv = List[List[str]]


class ProcessData:
    def __init__(self, name=None, cmd=None, monitor_pid=None, child_pid=None, args: CmdArgs = None, env: CmdEnv = None, retries=None, max_retries=None) -> None:
        self.name = name
        self.cmd = cmd
        self.monitor_pid = monitor_pid
        self.child_pid = child_pid
        self.args = args
        self.env = env
        self.retries = retries
        self.max_retries = max_retries


class Process:
    def __init__(self, data: ProcessData) -> None:
        self.data = data

    def spawn(self):
        pass

    def kill(self):
        pass

    def increament_retires(self):
        pass

    def should_retry(self):
        pass

    def is_active(self):
        pass

    def save_state(self):
        pass
