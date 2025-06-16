import json
import csv
import os

def read_json(path, roles):
    objs = []

    f = open(path, "r")

    js = json.load(f)["nodes"]
    for j in js:
        role = j["roles"]
        if role in roles:
            objs.append(j)

    f.close()
    return objs

def read_conf(path, key):
    f = open(path, "r")
    val = json.load(f)[key]
    f.close()
    return val

def aggregate_alias(path, variables, func):
    f = open(path, "r")
    reader = csv.DictReader(f)
    for row in reader:
        variables = func(row, variables)
    f.close()
    return variables

def aggregate_protocol(path, variables, f):
    aliases = [x for x in os.listdir(path) if os.path.isdir(f"{path}/{x}")]
    for alias in aliases:
        variables = aggregate_alias(f"{path}/{alias}/transactions.csv", variables, f)
    return variables

#Testing
if __name__ == "__main__":
    print(json.dumps(read_json("scripts/conf.json", ["replica"]), indent=4))