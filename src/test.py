from os import system
import subprocess
import time
import psutil
from fastapi import FastAPI, HTTPException
app = FastAPI()

proccess = None
proccess = 'telegram'#пишем сюда pid для проверки

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
        subprocess.call(['kill',str(pid)])
    else:
        print('Proccess not started')
# stop_proccess()

def start_proccess():
    global proccess
    pid = get_pid()
    if psutil.pid_exists(pid) == 0 :
        subprocess.run(["kill", "-CONT", pid])  # здесь можно заменить команду на запуск нужного процесса
        print(f"Процесс {proccess} запущен")
    else :
        print(f"Процесс {proccess} не найден")
start_proccess()