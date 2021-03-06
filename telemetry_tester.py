from datetime import datetime
import json
import os
import pwd
import subprocess
import sys

args = sys.argv[1:]
log = {'process':{}, "file": {}, "network":{}}

timestamp, sp = (datetime.now(), subprocess.Popen(args))
log['process']['time_stamp'] = str(timestamp)
log['process']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['process']['process_name'] = args[0]
log['process']['command_line'] = ' '.join(args)
log['process']['process_id'] = sp.pid

print(json.dumps(log))