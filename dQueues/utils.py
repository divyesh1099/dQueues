# dQueues/utils.py
import psutil
import datetime

def get_system_uptime():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.datetime.now()
    uptime = now - boot_time

    return {
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": str(uptime)
    }
