# coding: utf8

import faust
import os
import csv

app_name = "grover-task"
topic_name = "abalone"
buffer_flush_time_limit = 5

test_1_output_file_name = "test_1.csv"
test_2_output_file_name = "test_2.csv"
test_3_output_file_name = "test_3.csv"

subtask_1_file_name = "infants_with_more_than_14_rings.csv"
subtask_2_file_name = "males_heavy_and_short.csv"
subtask_3_file_name = "shell_humidity.csv"

output_1_file_name = subtask_1_file_name
output_2_file_name = subtask_2_file_name
output_3_file_name = subtask_3_file_name


class Abalone(faust.Record):
    Sex: str
    Length: float
    Diameter: float
    Height: float
    Whole_weight: float
    Shucked_weight: float
    Viscera_weight: float
    Shell_weight: float
    Class_number_of_rings: int


app = faust.App(app_name, topic_partitions=1, broker='kafka://127.0.0.1:9092',
                store="memory://")


abalone_topic = app.topic(topic_name, key_type=bytes,
                          value_type=Abalone, partitions=1)


csv_columns = ["id", "Sex", "Length", "Diameter", "Height", "Whole_weight",
               "Shucked_weight", "Viscera_weight", "Shell_weight", "Class_number_of_rings"]
csv_columns_with_humidity = csv_columns.copy()
csv_columns_with_humidity.append("shell_humidity_weight")

csv_file_1 = open(output_1_file_name, "w")
csv_file_2 = open(output_2_file_name, "w")
csv_file_3 = open(output_3_file_name, "w")

dict_writer_1 = csv.DictWriter(csv_file_1, fieldnames=csv_columns)
dict_writer_2 = csv.DictWriter(csv_file_2, fieldnames=csv_columns)
dict_writer_3 = csv.DictWriter(
    csv_file_3, fieldnames=csv_columns_with_humidity)

dict_writer_1.writeheader()
dict_writer_2.writeheader()
dict_writer_3.writeheader()


def csv_writer(dict_writer, enum, message):
    print(message)

    writable = dict(message)
    writable["id"] = enum
    del writable['__evaluated_fields__']

    dict_writer.writerow(writable)


def humidity_writer(humidity, key, value):
    print(value)

    writable = dict(value)
    writable["id"] = key
    writable["shell_humidity_weight"] = humidity
    del writable['__evaluated_fields__']

    dict_writer_3.writerow(writable)


@app.timer(interval=buffer_flush_time_limit)
async def buffer_cleaner():

    global last_mod_1, last_mod_2, last_mod_3

    try:
        if last_mod_1 == os.path.getmtime(output_1_file_name) and last_mod_2 == os.path.getmtime(output_2_file_name) and last_mod_3 == os.path.getmtime(output_3_file_name):
            print("ALL CLOSED")
            csv_file_1.close()
            csv_file_2.close()
            csv_file_3.close()
    except NameError:
        pass
    last_mod_1 = os.path.getmtime(output_1_file_name)
    last_mod_2 = os.path.getmtime(output_2_file_name)
    last_mod_3 = os.path.getmtime(output_3_file_name)


@app.agent(abalone_topic)
async def subtask_1(stream, sink=[csv_writer]):

    rings = {}

    async for value in stream.filter(lambda v: ((dict(vars(v).items())["Sex"] == 'I') and (dict(vars(v).items())["Class_number_of_rings"] >= 14))):

        key = str(value.Class_number_of_rings)

        try:
            rings[key] += 1
        except:
            rings[key] = 1

        csv_writer(dict_writer_1, rings[key], vars(value).items())


@app.agent(abalone_topic)
async def subtask_2(stream, sink=[humidity_writer]):

    async for i, value in stream.filter(lambda v: ((dict(vars(v).items())["Whole_weight"] > 0.4) and (dict(vars(v).items())["Length"] < 0.5))).enumerate():

        csv_writer(dict_writer_2, i, vars(value).items())


def shell_humidity(abalone):
    return round(abalone.Whole_weight - abalone.Shucked_weight-abalone.Shell_weight, 2)


@app.agent(abalone_topic)
async def subtask_3(stream, sink=[humidity_writer]):

    async for key, value in stream.enumerate():
        if shell_humidity(value) >= 0:
            humidity_writer(shell_humidity(value), key, vars(value).items())

if __name__ == "__main__":
    app.main()
