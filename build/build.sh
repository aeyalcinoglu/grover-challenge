#!/bin/bash -e

# create an env with miniconda
conda create -n grover-emre python=3.8
# change this according to your path
source /home/dahlersit/miniconda3/etc/profile.d/conda.sh
conda activate grover-emre
# see requirements.txt
pip install confluent_kafka faust

cd ../ && git clone https://github.com/wurstmeister/kafka-docker.git
cp build/docker-compose.yml kafka-docker && cd kafka-docker && docker-compose up -d

# REPLACE THIS WITH wait $!
sleep 15

cd ../src && python produce.py
faust -A main worker -l info
