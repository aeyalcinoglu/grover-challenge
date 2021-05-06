#!/bin/bash -e

cd ../

# clean-up
docker stop $(docker ps -a -q) && docker container prune
rm -rf kafka-docker src/grover-task-data data/results/*.csv

# create an env with miniconda
conda create -n grover-abalone python=3.8 -y
# ADJUST this according to your path
source /home/dahlersit/miniconda3/etc/profile.d/conda.sh
conda activate grover-abalone
# see requirements.txt
pip install confluent_kafka faust

git clone https://github.com/wurstmeister/kafka-docker.git
cp build/docker-compose.yml kafka-docker && cd kafka-docker && docker-compose up -d

sleep 15

echo 'Producing...'
cd ../src && python produce.py
faust -A process worker -l info