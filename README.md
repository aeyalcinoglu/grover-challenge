# Grover Take-Home Test

I was asked to solve [an assignment](https://github.com/devsbb/grover-engineering-recruitment/tree/master/challenges/abalone-data-processing) for the [SWE - Risk & Data](https://web.archive.org/web/20211122174537/https://boards.greenhouse.io/grover/jobs/4470003003) position. For some notes see `thought-process.md`. You can find the resulting csv files in `data/final-results`.

## How to build

I am using the `build.sh` script in the `build` directory, but it needs to be slightly adjusted, since it's using miniconda as the environment management system. Look at this script to see what's going on.

How to build without it:

- We will use the [kafka-docker](https://hub.docker.com/r/wurstmeister/kafka/) image as the docker image for Apache Kafka. Clone the [source repository](https://github.com/wurstmeister/kafka-docker) and replace the `docker-compose.yml` with the one in the `build` directory. Then run  `docker-compose up `.
- Python version is 3.8, need to have `faust` and `confluent-kafka` modules. See the `requirements.txt` in the `build` directory.
- Go into the `src` directory and put the data into the broker by running `python produce.py`. After it's done, run the program by `faust -A process worker -l info`. Results can be found in `data/results`.
