import os

SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1

# 使用 os.path.expanduser('~') 获取当前操作系统平台的当前用户根目录
HISTORY_PATH = os.path.expanduser('~') + os.sep + '.shiyanlou_shell_history'