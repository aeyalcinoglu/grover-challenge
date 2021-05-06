# Notes

[Farming of abalone began in the late 1950s and early 1960s in Japan and China](http://www.fishtech.com/abaloneinfo.html)!

# Pre-coding

- I tried to understand what streaming mentality is, and the landscape around it. One of the most important question that I tried to answer was: "Why is streaming better than triggering the database after each update".
- Then, I figured out the code stack in Java world and then found out the corresponding stack in Python world. I spend some time learning about the ELK/EKK stack. I decided to use Kafka in Docker, and Python with `faust` and `confluent_kafka`. [Here](https://www.youtube.com/watch?v=-DyWhcX3Dpc&list=PLa7VYi0yPIH2PelhRHoFR5iQgflg-y6JA) is a great introductory series on Kafka.
- I tried to figure out what part of the Kafka is opinionated, and what are the limits to it being configurable. I read some source code of Kafka, found out that Scala looks very nice. I realized that Kafka is very configurable, e.g. [Partitioner.java](https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/clients/producer/Partitioner.java) being very consice and the existence of [some low-level JVM settings](http://kafka.apache.org/documentation.html#java).


# Coding
At this point I go on with complete trust to the stack and my general approach.
- I first divided the task into 5 or so pieces, the first one being "produce and consume abalone_full csv file with just `confluent_kafka`". This was basically reading the [`confluent-kafka` documentation](https://docs.confluent.io/clients-confluent-kafka-python/current/overview.html), and connecting everything together.
- I also needed to setup an kafka environment, for which I decided to use Docker, however this was painful. [These notes](https://jaceklaskowski.gitbooks.io/apache-kafka/content/kafka-docker.html) were helpful.
- For processing, I first tried to have a trivial faust app, where it basically writes the stream to a csv file, hence generating an equivalent csv file to the input. Then I slowly found my way into the tasks.
- One of the first problems I faced was that `group_by` keyword in Faust seem to not work on `int` typed field descriptors. This made me use a hack instead of that keyword, which is probably not health due to that whole `async` world.
- Another problem was to decide when to close the csv files. Since it's in theory an infinite process, I thought a decent way is to just check if there's an update to the new csv files every some (let's say 10) seconds. I didn't want to make it depend on the input file, but this feels extremely hacky too. I couldn't get the data in the buffer without closing the file.


# Assumptions

- Concurrency concerns are mentioned in the [faust user guide](https://faust.readthedocs.io/en/latest/userguide/agents.html#concurrency). I decided to not change that variable, since it would affect only the individual agent, and also one cannot use the `group_by` keyword anymore. I realized that csv files for the different subtasks were getting created simultaneously, so I *assume* that Faust is giving some level of concurrency by default. There are some vague comments about this in [here](https://faust.readthedocs.io/en/latest/userguide/streams.html#message-life-cycle).


# Comments
- Even though it's very rigid and discrete, Kafka having concepts like [Stream Processing Topology](https://kafka.apache.org/0102/documentation/streams/core-concepts) is exciting, and I have the vague idea that it can be generalized (at least to the simplicial complexes).
- Faust was not well-documented and buggy. Sending kill signal and restarting the worker was a pain. I see that it has very [recent issues](https://github.com/robinhood/faust/issues/711) on these topics on github. However, I can't tell if these are just about [`asyncio`](https://stackoverflow.com/questions/48562893/how-to-gracefully-terminate-an-asyncio-script-with-ctrl-c).
- The fact that [Spotify's docker image](https://github.com/spotify/docker-kafka) for Kafka + Zookeeper is documented worse (and hence harder to use) than [wurstmeister's docker image](https://github.com/wurstmeister/kafka-docker) was surprising.
- I was looking for the low-level algorithms and efficiency hacks that Kafka uses. [Sendfile](https://www.oreilly.com/library/view/architecting-data-intensive-applications/9781786465092/9fc04120-fdda-4453-af7c-e89fd9f1dc31.xhtml) operation is one of them.

# Post-coding
- [Here](https://www.confluent.io/blog/distributed-consensus-reloaded-apache-zookeeper-and-replication-in-kafka/) is a great article about distributed consensus stuff.