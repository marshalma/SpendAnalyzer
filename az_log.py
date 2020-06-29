#!/usr/local/bin/python3

from datetime import datetime
import time

def _log(log, level):
    print("[{}][{}] {}".format(datetime.fromtimestamp(time.time()), level, log))

def log_debug(log):
    _log(log, "DEBUG")

def log_info(log):
    _log(log, "INFO")

def log_warn(log):
    _log(log, "WARN")

def log_error(log):
    _log(log, "ERROR")
