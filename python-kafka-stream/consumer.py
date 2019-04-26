#!/usr/bin/env python
from confluent_kafka import Consumer, KafkaException
from configparser import ConfigParser
import sys
import os


def get_section_config(section):

    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(root_dir, 'config.ini')
    parser = ConfigParser()
    parser.read(config_path)
    config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
    section_config = config_dict[section]

    return section_config


def print_assignment(consumer, partitions):
    print('Assignment:', partitions)


if __name__ == '__main__':

    consumer_conf = get_section_config('consumer')
    consume = Consumer(**consumer_conf)
    consume.subscribe(['example-topic-output'], on_assign=print_assignment)

    try:
        while True:
            msg = consume.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                print(msg.value())

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        # Close down consumer to commit final offsets.
        consume.close()
