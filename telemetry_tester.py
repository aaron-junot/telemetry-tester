from datetime import datetime
import json
import os
import pwd
import subprocess
import sys

args = sys.argv[1:]
log = {
    "process":{},
    "file": {
        "create":{},
        "modify":{},
        "delete":{}
    },
    "network":{}
}

timestamp, sp = (datetime.now(), subprocess.Popen(args))
log['process']['time_stamp'] = str(timestamp)
log['process']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['process']['process_name'] = args[0]
log['process']['command_line'] = ' '.join(args)
log['process']['process_id'] = sp.pid

file_name = "test"
file_type = "csv"
file_location = f"{os.getcwd()}/{file_name}.{file_type}"

try:
    file_timestamp, f = (datetime.now(), open(file_location, "x"))
except FileExistsError:
    print(f"The file {file_location} already exists!")
    exit()

log['file']['create']['time_stamp'] = str(file_timestamp)
log['file']['create']['path'] = file_location
log['file']['create']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['file']['create']['process_name'] = sys.argv[0]
log['file']['create']['command_line'] = ' '.join(sys.argv)
log['file']['create']['process_id'] = os.getpid()

f.close()

f = open(file_location, "a")
modify_timestamp, _ = (datetime.now(), f.write("test1,test2,test3"))

log['file']['modify']['time_stamp'] = str(modify_timestamp)
log['file']['modify']['path'] = file_location
log['file']['modify']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['file']['modify']['process_name'] = sys.argv[0]
log['file']['modify']['command_line'] = ' '.join(sys.argv)
log['file']['modify']['process_id'] = os.getpid()

f.close()

delete_timestamp, _ = (datetime.now(), os.remove(file_location))

log['file']['delete']['time_stamp'] = str(delete_timestamp)
log['file']['delete']['path'] = file_location
log['file']['delete']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['file']['delete']['process_name'] = sys.argv[0]
log['file']['delete']['command_line'] = ' '.join(sys.argv)
log['file']['delete']['process_id'] = os.getpid()

print(json.dumps(log))
