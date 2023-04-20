from os import system
import subprocess
import time
import psutil
from fastapi import FastAPI, HTTPException
app = FastAPI()

proccess = None
proccess = '300000'#пишем сюда pid для проверки

# tmp = subprocess.Popen(['systemctl', 'status', proccess])
# print(tmp.args)

def start_process() :
    global proccess
    pid = int(proccess)
    tmp = subprocess.Popen(['systemctl', 'status', proccess])#смотрим статус данного процесса(время работы и т.д.)
    if tmp.returncode is None and psutil.pid_exists(pid):#если процесс существует и работает возвращает  true
        print("Process already running")
    else :                
        print('Proccess not started')
start_process()
#все значения сверяем с выводом команды ps aux

def stop_process() :
    global proccess
    pid = int(proccess)
    if psutil.pid_exists(pid):
        subprocess.call(['kill',str(pid)])
    else:
        print('Proccess not started')
stop_process()