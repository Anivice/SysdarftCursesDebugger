#!/usr/bin/env python

import curses
from time import sleep
import sys, os
component_dir = os.path.dirname(os.path.abspath(__file__)) + "/PySubComponents/"
sys.path.append(component_dir)
from PySubComponents.SysdarftDebugger import *


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <Target>")
        sys.exit(0)

    target = sys.argv[1]
    print(f"Connecting to {target}...")

    dbg = SysDbg(target)

    try:
        version = dbg.req_api_ver()
        print("Backend connected, Debugger Backend Version is ", version)
    except TargetUnreachable as e:
        print("Cannot connect to target: ", e.message)
        sys.exit(1)
    except BackendAPIIncorrectResponse as e:
        print("Wrong backend!", e.message)
        sys.exit(1)
