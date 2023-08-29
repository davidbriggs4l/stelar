import asyncio
import sys
import os
import signal


class Process:
    def __init__(self, pid, tty, time, cmd) -> None:
        self.pid = pid
        self.tty = tty
        self.time = time
        self.cmd = cmd


def kill(pid):
    try:
        os.kill(int(pid), signal.SIGTERM)
    except Exception as e:
        print(e)


async def ps(pid):
    command = ["ps", "-p", f"{pid}"]
    child = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=sys.stderr)
    stdout, stderr = await child.communicate()
    if stdout:
        lines = stdout.decode().split("\n")
        lines.remove('')
        lines.pop(0)
        procs = map(parse_ps_output, lines)
        procs = list(procs)
        if len(procs) > 0:
            return procs[0]
        return None


def parse_ps_output(p: str):
    fields = p.split(" ")
    return Process(pid=f"{fields[0]}", tty=f"{fields[1]}", time=f"{fields[2]}", cmd=f"{fields[3]}")
