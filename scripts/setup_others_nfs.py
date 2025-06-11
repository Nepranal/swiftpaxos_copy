import subprocess
from utils import read_json

#Set up nfs for everyone else
#This is supposed to only be done once

replicas = read_json("scripts/conf.json", ["replica"])
mstr = read_json("scripts/conf.json", ["master"])

node_addresses = []
users = []
key_paths = []
server_ip = mstr["server_ip"]
for replica in replicas:
    node_addresses.append(replica["node_address"])
    users.append(replica["user"])
    key_paths.append(replica["key_path"])

n = len(node_addresses)
commands = [
    "sudo mkdir -p /mnt/share", #Root directory
    "sudo mkdir -p /mnt/share/src", #Code folder
    "sudo mkdir -p /mnt/share/exp", #Experiment results folder
    "sudo apt install nfs-common", #nfs client
    f"sudo mount {server_ip}:/mnt/share/src /mnt/share/src",
    f"sudo mount {server_ip}:/mnt/share/exp /mnt/share/exp"
]

for i in range(n):
    address = f"{users[i]}@{node_addresses[i]}"
    key_path = key_paths[i]
    for cmd in commands:
        try:
            subprocess.run(["ssh", "-i", key_path, address, cmd], check=True)
        except Exception as e:
            print(repr(e))
            break
