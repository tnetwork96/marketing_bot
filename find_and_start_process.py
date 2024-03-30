import subprocess
import os

process_name = "bot_wake_up"
p = subprocess.Popen(f'ps aux | grep -i {process_name}', stdout=subprocess.PIPE, shell=True)
console_text = list(p.communicate())[0].decode("utf-8")
processes = [x for x in console_text.split("\n") if x.strip()]
correct_process = [p for p in processes if process_name in p and "nohup" in p]
correct_process = correct_process[0] if len(correct_process) != 0 else None
if not correct_process:
    os.system('sudo nohup python3 bot_wake_up.py &')

