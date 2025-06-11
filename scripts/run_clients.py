import subprocess
from threading import Thread
from utils import read_json, read_conf
from kill_all import kill_proc

clients = read_json("scripts/conf.json", ["client"])

node_addresses = []
users = []
key_paths = []
aliases=[]
for client in clients:
    node_addresses.append(client["node_address"])
    users.append(client["user"])
    key_paths.append(client["key_path"])
    aliases.append(client["alias"])
protocol = read_conf("scripts/conf.json", "protocol")
config_file = read_conf("scripts/conf.json", "config_file")
experiment_number = read_conf("scripts/conf.json", "exp")
n = len(node_addresses)

def run(id):
    key_path = key_paths[id]
    user = users[id]
    node_address = node_addresses[id]
    alias = aliases[id]

    address = f"{user}@{node_address}"

    kill_proc(key_path, address)
    subprocess.run(["ssh", "-i", key_path, address, f"sudo mkdir -p /mnt/share/exp/exp{experiment_number}/{protocol}/{alias}"], check=True)
    subprocess.run(["ssh", "-i", key_path, address, f"cd /mnt/share/src/swiftpaxos_copy && swiftpaxos -run client -config aws.conf -protocol {protocol} -alias {alias} -log /mnt/share/exp/exp{experiment_number}/{protocol}/{alias}/{alias}_"], check=True)

threads = []
for i in range(n):
    thread = Thread(target = run, args=(i,))
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()


