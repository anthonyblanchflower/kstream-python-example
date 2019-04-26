from winton_kafka_streams.processor import BaseProcessor, TopologyBuilder
import winton_kafka_streams.kafka_config as kafka_config
import winton_kafka_streams.kafka_streams as kafka_streams
import time
import logging

log = logging.getLogger(__name__)


class MessageProcessor(BaseProcessor):

    def initialise(self, name, context):

        super().initialise(name, context)

    def process(self, _, value):

        log.debug(f'MessageProcessor::process({str(value)})')


def _debug_run(config_file):

    kafka_config.read_local_config(config_file)

    with TopologyBuilder() as topology_builder:
        topology_builder.source('input-value', ['example-topic']).processor('message', MessageProcessor, 'input-value').sink('output-value', 'example-topic-output', 'message')

    wks = kafka_streams.KafkaStreams(topology_builder, kafka_config)
    wks.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        wks.close()


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    import argparse

    parser = argparse.ArgumentParser(description="Debug runner for Python Kafka Streams")
    parser.add_argument('--config-file', '-c', help="Local configuration - will override internal defaults",
                        default='config.properties')
    args = parser.parse_args()

    _debug_run(args.config_file)
