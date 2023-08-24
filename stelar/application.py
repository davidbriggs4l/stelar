import asyncio
import uvloop
import os
import argparse
from settings import Settings


async def start_process(loop: uvloop.Loop):
    settings = Settings.read(loop=loop)
    print(settings)
    print("Staring process found in stelar.yaml")


def monitor(loop: uvloop.Loop, data):
    print(f"monitor {data}")


def list(loop: uvloop.Loop, all):
    print(f"listing with all as {all}")


def stop(loop: uvloop.Loop, id):
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

        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop=loop)
        subcommand = args.subcommand
        if subcommand == "monitor":
            loop.create_task(args.func(args.data))
        elif subcommand == "list":
            args.func(args.all)
        elif subcommand == "stop":
            args.func(args.process)
        elif subcommand == None:
            loop.create_task(start_process(loop=loop))
        else:
            NotImplemented
        loop.run_forever()
    except KeyboardInterrupt:
        exit(0)
    except SystemExit:
        exit(0)
    finally:
        loop.close()


if __name__ == "__main__":
    main()
