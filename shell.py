import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func import *

built_in_cmds = {}

def tokenize(string):
    return shlex.split(string)

def preprocess(tokens):
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token

def handler_kill(signum, frame):
    raise OSError("Killed!")

def execute(cmd_tokens):
    with open(HISTORY_PATH, 'a') as history_file:
        history_file.write(' '.join(cmd_tokens) + os.linesep)
    if cmd_tokens:
        cmd_name = cmd_tokens[0]
        cmd_args = cmd_tokens[1:]
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)
        signal.signal(signal.SIGINT, handler_kill)
        if platform.system() != "Windows":
            p = subprocess.Popen(cmd_tokens)
            p.communicate()
        else:
            command = ""
            command = ' '.join(cmd_tokens)
            os.system(command)
    return SHELL_STATUS_RUN

def display_cmd_prompt():
    user = getpass.getuser()
    hostname = socket.gethostname()
    cwd = os.getcwd()
    base_dir = os.path.basename(cwd)
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'
    if platform.system() != 'Windows':
        sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (user, hostname, base_dir))
    else:
        sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
    sys.stdout.flush()

def ignore_signals():
    if platform.system() != "Windows":
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def shell_loop():
    status = SHELL_STATUS_RUN
    while status == SHELL_STATUS_RUN:
        display_cmd_prompt()
        ignore_signals()
        try:
            cmd = sys.stdin.readline()
            cmd_tokens = tokenize(cmd)
            cmd_tokens = preprocess(cmd_tokens)
            status = execute(cmd_tokens)
        except:
            _, err, _ = sys.exc_info()
            print(err)

def register_command(name, func):
    built_in_cmds[name] = func

def init():
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("getenv", getenv)
    register_command("history", history)

def main():
    init()
    shell_loop()

if __name__ == "__main__":
    main()