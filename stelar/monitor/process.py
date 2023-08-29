import asyncio
from typing import List
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from .. import os
import sys
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
        self._data = data

    @property
    def data(self):
        return self._data

    async def spawn(self):
        args = self.data.args
        env = self.data.env
        try:
            child = await asyncio.create_subprocess_exec(self.data.cmd, *args, stdout=sys.stdout, stderr=sys.stderr)
            child_pid = child.pid
            import os as q
            current_pid = q.getpid()
            self.monitor_pid = current_pid
            self.child_pid = child_pid
            self.save_state()
            print(f"[debug]: Started child process with PID: {child_pid}")
            return child
        except Exception as e:
            print(e)

    def kill(self):
        os.kill(self.data.monitor_pid)

    @data.setter
    def monitor_pid(self, pid):
        self.data.monitor_pid = pid

    @data.setter
    def child_pid(self, pid):
        self.data.child_pid = pid

    def increament_retires(self):
        self.data.retries += 1

    def serialize(self):
        yaml = YAML()
        out = StringIO()
        yaml.compact(seq_seq=False, seq_map=False)
        yaml.indent(mapping=4, sequence=6, offset=3)
        yaml.register_class(ProcessData)
        yaml.dump(self.data, stream=out)
        return out.getvalue()

    def deserialize(data):
        yaml = YAML(pure=True, typ='rt')
        input = StringIO(data)
        p = yaml.load(input.read())
        if p is not None:
            return Process(data=ProcessData(**p))
        print("Nothing to deserialize!")
        exit(0)

    def should_retry(self):
        return self.data.retries <= self.data.max_retries

    async def is_active(self):
        ps = await os.ps()
        if ps is not None:
            return True
        return False

    def save_state(self):
        from . import file
        file.save(file.path_from_name(self.data.name), self)
