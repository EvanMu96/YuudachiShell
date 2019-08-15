from .constants import *

def echo(args):
    result_str = ' '.join(args)
    print(result_str)
    return SHELL_STATUS_RUN