import logging
import atexit
import asyncio
from . import os
import argparse
import sys
from .settings import Settings, start
from .monitor.process import Process
from .monitor import file
import json


async def start_process():
    settings = Settings.read()
    processes = settings.list_procs()
    print("Staring process found in stelar.yaml")
    for p in processes:
        data = p.serialize()
        print(f"Name: {p.data.name}")
        print(f"Command: {p.data.cmd}")
        command = [*sys.orig_argv, "monitor", "--data", data]
        child = await asyncio.create_subprocess_exec(
            *command, stdout=sys.stdout, stderr=sys.stderr)
        print(f"Manager process started with PID: {child.pid}")
        # stdout, stderr = await child.communicate()
        rcode = await child.wait()
        print(f"[{p.data.name!r}] exited with {rcode}")


def sigterm_handler(name):
    print("[debug]: SIGTERM arrived!")
    process = file.read(file.path_from_name(name))
    os.kill(process.data.child_pid)


async def monitor(data):
    process = Process.deserialize(data)
    atexit.register(sigterm_handler, process.data.name)
    await start(process=process)


def list(all):
    print(f"listing with all as {all}")


def stop(id):
    print(f"stopping {id}")


def main():
    parser = argparse.ArgumentParser(
        description="A simple process manager")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    ###
    monitorProc = subparsers.add_parser(
        "monitor",  help="[INTERNAL] Monitors the provided command data as JSON")
    monitorProc.add_argument(
        "--data", metavar="<data>", help="Data needed to start the monitoring process", type=str, required=True)
    monitorProc.set_defaults(func=monitor)
    listProc = subparsers.add_parser("list", help="List active processes")
    listProc.add_argument(
        "--all", "-a", help="Show all processes", action="store_true")
    listProc.set_defaults(func=list)
    stopProc = subparsers.add_parser(
        "stop", help="Stops an already running process giver its id")
    stopProc.add_argument(
        "--process", metavar="<process>", help="The process to store", type=str, required=True)
    stopProc.set_defaults(func=stop)

    ###
    try:
        args = parser.parse_args()

        subcommand = args.subcommand
        if subcommand == "monitor":
            asyncio.run(args.func(args.data))
        elif subcommand == "list":
            args.func(args.all)
        elif subcommand == "stop":
            args.func(args.process)
        elif subcommand == None:
            asyncio.run(start_process())
        else:
            NotImplemented
    # except KeyboardInterrupt:
    #     exit()
    # except SystemExit:
    #     exit(0)
    except Exception as e:
        logging.error(e)
    finally:
        exit()


if __name__ == "__main__":
    main()
