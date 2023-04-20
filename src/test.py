from os import system
import subprocess
import time
import psutil
from fastapi import FastAPI, HTTPException
app = FastAPI()

proccess = None
proccess = 'zsh'#пишем сюда pid для проверки

# tmp = subprocess.Popen(['systemctl', 'status', proccess])
# print(tmp.args)

def get_pid():
    global proccess
    pid = subprocess.check_output(['pgrep',proccess])
    print(pid)
    return int(pid)
# get_pid()

def status_proccess() :
    global proccess
    pid = get_pid()
    tmp = subprocess.Popen(['systemctl', 'status', proccess])#смотрим статус данного процесса(время работы и т.д.)
    if tmp.returncode is None and psutil.pid_exists(pid):#если процесс существует и работает возвращает  true
        print("Process already running")
    else :                
        print('Proccess not started')
# status_proccess()
#все значения сверяем с выводом команды ps aux

def stop_proccess() :
    global proccess
    pid = get_pid()
    if psutil.pid_exists(pid):
        subprocess.run(['sudo', 'systemctl', 'stop', proccess])
        print(f"{proccess} stopted")
    else:
        print('Proccess not started')
stop_proccess()

def start_proccess():
    global proccess
    pid = get_pid()
    if pid is not None:
        subprocess.call(['systemd-run', '--unit='+proccess, '--scope', 'myprocess'])
        status_proccess()
        print(f'{proccess} started')
    else :
        print(f'{proccess} running')

# start_proccess()
#надо понять, если у меня под одни процессом множество pid, нужно ли валидировать это, или выбирать процесс который имеет один пид