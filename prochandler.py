import psutil
import time
import os
import sys

process_signal_dict_linux = {
    "SIGTERM": 15,
    "SIGKILL": 9,
    "SIGSTOP": 17,
    "SIGCONT": 19,
    "SIGINT": 2,
    "SIGQUIT": 3,
    "SIGTSTP": 18,
    "SIGUSR1": 10,
    "SIGUSR2": 12,
}

def get_process_info(pid):
    try:
        p = psutil.Process(pid)
        return p.name(), p.username(), p.create_time(), p.status(), p.cpu_times(), p.memory_info(),p.cmdline()
    except psutil.AccessDenied:
        print('Access Denied')
        return None


def get_procs_dict():
    try:
        procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username',"status","cpu_percent","memory_percent","cmdline"])}
        return procs
    except psutil.AccessDenied:
        print('Access Denied')
        return None


def get_procs_dict_by_user(user):
    try:
        procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username',"status","cpu_percent","memory_percent","cmdline"]) if p.username()==user}
        return procs
    except psutil.AccessDenied:
        print('Access Denied')
        return None

def get_procs_dict_for_current_user():    
    return get_procs_dict_by_user(os.getlogin())
    


def send_signal_to_pid(pid,signal):
    try:
        p = psutil.Process(pid)
        p.send_signal(process_signal_dict_linux[signal])
        return True
    except psutil.AccessDenied:
        print('Access Denied')
        return False
    except KeyError:
        print('Invalid Signal')
        return False
    except psutil.NoSuchProcess:
        print('No such process')
        return False
    