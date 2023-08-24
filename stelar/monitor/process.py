from typing import List

CmdArgs = List[List[str]]
CmdEnv = List[List[str]]

class ProcessData:
    def __init__(self, name, cmd, monitor_pid, child_pid, args:CmdArgs, env:CmdEnv, retries, max_retries) -> None:
        self.name = name
        self.cmd = cmd
        self.monitor_pid = monitor_pid
        self.child_pid = child_pid
        self.args = args
        self.env = env
        self.retries = retries
        self.mac_retries = max_retries

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