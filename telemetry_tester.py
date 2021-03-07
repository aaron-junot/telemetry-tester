from datetime import datetime
import json
import os
import pwd
import socket
import subprocess
import sys

if (len(sys.argv) != 2):
    print(
"""Usage: python telemetry_tester.py [config.json]

Please specify a single configuration file.
""", file=sys.stderr)
    exit(1)

try:
    config = json.load(open(sys.argv[1]))
except FileNotFoundError:
    print("File Not Found: please specify a valid JSON configuration file", file=sys.stderr)
    exit(1)
except json.decoder.JSONDecodeError as j:
    print("Error loading json:", file=sys.stderr)
    print(str(j), file=sys.stderr)
    exit(1)
except Exception as e:
    print(f"Something went wrong: {e}", file=sys.stderr)
    exit(1)

command = config['command']
file_info = config['file']

if type(command) != list or not all(type(s) == str for s in command):
    print(f"""Invalid command:
    Expected: list of strings
    got: type: {type(config['command'])}, value: {config['command']}""", file=sys.stderr)
    exit(1)
if type(file_info) != dict:
    print(f"""Invalid file:
    Expected: dict
    got: {type(file_info)}""", file=sys.stderr)
    exit(1)

log = {
    "process":{},
    "file": {
        "create":{},
        "modify":{},
        "delete":{}
    },
    "network":{}
}

timestamp, sp = (datetime.now(), subprocess.Popen(command))
log['process']['time_stamp'] = str(timestamp)
log['process']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['process']['process_name'] = command[0]
log['process']['command_line'] = ' '.join(command)
log['process']['process_id'] = sp.pid

file_name = config['file'].get('name') or 'test'
file_type = config['file'].get('type') or 'csv'
file_location = config['file'].get('location') or os.getcwd()
file_location = f"{file_location}/{file_name}.{file_type}"

try:
    file_timestamp, f = (datetime.now(), open(file_location, "x"))
except FileExistsError:
    print(f"The file {file_location} already exists!", file=sys.stderr)
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

post_data = b'POST /post HTTP/1.1\nHost: httpbin.org\n\ntest'
dest_port = 80
source_port = 31415
source_address = socket.gethostbyname(socket.gethostname())
dest_address = socket.gethostbyname('httpbin.org')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', source_port))
s.connect((dest_address, dest_port))
network_timestamp, _ = (datetime.now(), s.sendall(post_data))
data = s.recv(1024)
s.close()

log['network']['time_stamp'] = str(network_timestamp)
log['network']['username'] = pwd.getpwuid(os.getuid()).pw_name
log['network']['destination_address'] = dest_address
log['network']['destination_port'] = dest_port
log['network']['source_address'] = source_address
log['network']['source_port'] = source_port
log['network']['data_size'] = len(post_data)
log['network']['data_protocol'] = "TCP" # socket.SOCK_STREAM is always TCP
log['network']['process_name'] = sys.argv[0]
log['network']['command_line'] = ' '.join(sys.argv)
log['network']['process_id'] = os.getpid()


print(json.dumps(log))
