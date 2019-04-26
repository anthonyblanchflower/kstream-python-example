# Python KStream Example

## Creating local Kafka environment

To create a docker network, kafka and zookeeper service:

`docker network create kafka`

`docker run --net=kafka -d --name=zookeeper -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:4.1.0`

`docker run --net=kafka -d -p 9092:9092 --name=kafka -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:4.1.0`

then point kafka:9092 to the local host IP (127.0.0.1):

`sudo vi /etc/hosts` and add `127.0.0.1    kafka` to this file.

## Install dependencies

You will require the Apache Kafka C/C++ library librdkafka. 
For OSX this can be installed through Homebrew using `brew install librdkafka` then
export these environmental variables `CFLAGS=-I/usr/local/include and LDFLAGS=-L/usr/local/lib`.
Python dependencies can be installed using `pip install -r requirements.txt`. 

## Populate Kafka Messages
* Run `python3 ./python-kafka-stream/producer.py` to deliver messages to Kafka.
* Run `python3 ./python-kafka-stream/consumer.py` to verify that the delivered messages can be consumed.

## Running KStream
* Run `python3 ./python-kstream/kstream.py` to process messages from Kafka. At the moment
no transformation of the message occurs, it is just logged to the console.
