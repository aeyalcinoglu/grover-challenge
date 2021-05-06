#!/bin/bash -e

cd ../

# clean-up
docker stop $(docker ps -a -q) && docker container prune
rm -rf kafka-docker src/grover-task-data data/results/*.csv
