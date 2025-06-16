from math import ceil
import os
import csv
from utils import aggregate_alias, aggregate_protocol

#Please procduce files with transactions for each alias before using this
#Produce a csv file for a protocol in an experiment.
#csv: protocol, latency, percentage

# ROOT_PATH = "/mnt/share/exp"
ROOT_PATH = "out"
SPLIT = 10


experiment_number = 1
folder_path = f"{ROOT_PATH}/exp{experiment_number}"
protocols = [x for x in os.listdir(folder_path) if os.path.isdir(f"{folder_path}/{x}")]
min_latency = float("inf")
max_latency = 0
for protocol in protocols:
    min_latency, = aggregate_protocol(f"{folder_path}/{protocol}", [min_latency], lambda row, variables: [float(row["latency"]) if float(row["latency"]) < variables[0] else variables[0]])
    max_latency, = aggregate_protocol(f"{folder_path}/{protocol}", [max_latency], lambda row, variables: [float(row["latency"]) if float(row["latency"]) > variables[0] else variables[0]])
inc = ceil((max_latency - min_latency)/SPLIT)


field_names = ["protocol", "latency", "percentage"]
protocol_f = open(f"{folder_path}/cdf.csv", "w")
writer = csv.DictWriter(protocol_f, fieldnames=field_names)
writer.writeheader()
for protocol in protocols:
    folder_path = f"{ROOT_PATH}/exp{experiment_number}/{protocol}"
    alias_folder = [x for x in os.listdir(folder_path) if os.path.isdir(f"{folder_path}/{x}")]
    files = [f"{folder_path}/{alias}/transactions.csv" for alias in alias_folder]

    for i in range(SPLIT):
        upper_bound_latency = min_latency + (i + 1)*inc
        p, t = 0, 0
        for f in files:
            count, total = aggregate_alias(f, [0,0], lambda row, variables: [variables[0] + (float(row["latency"]) <= upper_bound_latency), variables[1] + 1])
            p = ((p*t) + count)/(t + total)
        writer.writerow({"protocol": protocol, "latency": upper_bound_latency, "percentage":p})
protocol_f.close()

