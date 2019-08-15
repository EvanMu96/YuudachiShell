from .constants import *
import subprocess

def man(args):
    cmd = args[0]
    subprocess.call(["man", cmd])
    return SHELL_STATUS_RUN