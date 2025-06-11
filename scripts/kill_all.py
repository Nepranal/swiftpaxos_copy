import subprocess
from utils import read_json

def kill_proc(key_path, address):
    commands = subprocess.run(["ssh", "-i", key_path, address, "ps -ef | grep swiftpaxos"], check=True, capture_output=True).split("\n")
    for command in commands:
        cmds = command.split()
        if len(cmds) >= 2:
            pid = cmds[1]
            subprocess.run(["ssh", "-i", key_path, address, "kill " + pid])

nodes = read_json("scripts/conf.json", ["client", "replica", "master"])
for node in nodes:
    kill_proc(node["key_path"], node["node_address"])