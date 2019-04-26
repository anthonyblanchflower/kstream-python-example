#!/usr/bin/env python
from confluent_kafka import Producer
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


def delivery_callback(err, msg):

    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                         (msg.topic(), msg.partition(), msg.offset()))


if __name__ == '__main__':

    producer_conf = get_section_config('producer')
    producer = Producer(**producer_conf)
    producer.produce('example-topic', 'example-message', callback=delivery_callback)
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(producer))
    producer.flush()

