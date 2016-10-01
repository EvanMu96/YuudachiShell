import os
import signal
import shlex
import getpass
import socket
import subprocess
import platform
from func import *

# 一张字典标，用来存储命令与函数的映射
built_in_cmds = {}

def register_command(name, func):
    """
    注册命令
    :param name:命令名
    :param func: 函数名
    """
    built_in_cmds[name] = func

def init():
    """
    注册所有命令
    """
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("getenv", getenv)
    register_command("history", history)

def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN
        # 当shell运行信号为正在运行
        display_cmd_prompt()

        # 忽略 ctrl+c ctrl+z
        ignore_signals()

        try:
            # 读取命令
            cmd = sys.stdin.readline()

            # 解析命令，将命令拆分返回一个列表
            cmd_token = tokenize(cmd)

            # 预处理函数
            # 将命令中的环境变量使用真实值进行替换
            cmd_token = preprocess(cmd_token)

            # 执行命令并返回shell的状态
            status = excute(cmd_token)

        except:
            # sys.exc_info 函数包含三个值的tuple
            _, err, _ = sys.exc_info()
            print(err)
            # 我们只需获得中间的错误信息

def display_cmd_prompt():
    # getpass.getuser获取当前用户名
    user = getpass.getuser()

    # 获取hostname
    hostname = socket.gethostname()

    # 获取当前工作路径
    cwd = os.getcwd()

    # 获取路径的 cwd的最低一级的目录
    base_dir = os.path.basename(cwd)

    # 如果当前目录在用户的根目录中则用~代替
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'

    # 输出命令提示符
    if platform.system() != 'windows':
        sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (user, hostname, base_dir))
    else:
    sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " % (user, hostname, base_dir))

def ignore_signals():
    if platform.system() != 'windows':
        # 不是windows时忽略ctrl + z
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    # 忽略 ctrl + c
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def tokenize(string):
    # 将string按shell的语法规则进行分割
    # 返回string的分割列表
    return shlex.split(string)

def preprocess(tokens):
    # 用于存储处理之后的token
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
            # os.getenv用于获取环境变量的值
            # 变量不存在是返回而为空
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token

def handler_kill(signum, frame):
    raise OSError('Killed')

def execute(cmd_tokens):
    # open() 'a'模式表示以添加的方式打开制定文件
    # 这个模式下write操作不会覆盖文件原有信息，而是添加到文件原有信息之后
    with open(HISTORY_PATH, 'a') as history_file:
        history_file.write(' '.join(cmd_tokens) + os.linesep)

    if cmd_tokens:
        # 获取命令
        cmd_name = cmd_token[0]
        # 获取参数
        cmd_arg = cmd_token[1]

        # 如果当前命令在命令中
        # 则传入参数，调用响应相应函数执行

        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_arg)

        # 监听ctrl + c信号

        signal.signal(signal.SIGINT, handler_kill)

        # 如果当前系统不是windows
        # 则创建子进程

        if platform != 'windows':
            p = subprocess.Popen(cmd_tokens)

            # 父进程从子进程读取数据，直到读取到EOF
            # 这里主要用来等待子进程终止运行
            p.communicate()
        else:
            # windows平台
            command = ""
            command = "".join(cmd_tokens)
            # 执行command
            os.system(command)
    return SHELL_STATUS_RUN

# shell.py程序入口
def main():
    # 执行shell_loop之前先进行出事换
     init()

    # 处理命令的主程序
    shell_loop()

if __name__ == '__main__':
    main()