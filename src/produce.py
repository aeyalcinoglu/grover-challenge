# coding: utf8

from confluent_kafka import Producer
import csv
import json

file_name = "../data/abalone_full.csv"
topic_name = "abalone"

p = Producer({'bootstrap.servers': 'localhost:9092'})

with open(file_name) as file:
    reader = csv.DictReader(file, delimiter=",")
    for row in reader:
        data_set = {"Sex": str(row["Sex"]),
                    "Length": float(row["Length"]),
                    "Diameter": float(row["Diameter"]),
                    "Height": float(row["Height"]),
                    "Whole_weight": float(row["Whole_weight"]),
                    "Shucked_weight": float(row["Shucked_weight"]),
                    "Viscera_weight": float(row["Viscera_weight"]),
                    "Shell_weight": float(row["Shell_weight"]),
                    "Class_number_of_rings": int(row["Class_number_of_rings"])}

        p.produce(topic=topic_name, value=str(json.dumps(data_set)))
        p.flush()
    p.flush()
p.flush()
