from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import StringSerializer

from build.gen.bakdata.corporate_updates.v1 import corporate_updates_pb2
from rb_cleaner.constant import BOOTSTRAP_SERVER, INPUT_TOPIC


class RbConsumer:
    def __init__(self):
        protobuf_deserializer = ProtobufDeserializer(
            corporate_updates_pb2.CorporateUpdate, {"use.deprecated.format": True}
        )

        consumer_conf = {
            "bootstrap.servers": BOOTSTRAP_SERVER,
            "group.id": "my-fdasfkldsafsdddddxfdsafdsafsdd",
            "key.deserializer": StringSerializer("utf_8"),
            "value.deserializer": protobuf_deserializer,
        }

        consumer = DeserializingConsumer(consumer_conf)
        consumer.subscribe([INPUT_TOPIC])
        self.consumer = consumer

        while True:
            try:
                # SIGINT can't be handled when polling, limit timeout to 1 second.
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue

                user = msg.value()
                if user is not None:
                    print("User record {}:\n"
                          "\tname: {}\n"
                          "\tfavorite_number: {}\n"
                          "\tfavorite_color: {}\n"
                          .format(msg.key(), user.name,
                                  user.favorite_number,
                                  user.favorite_color))
            except KeyboardInterrupt:
                break

    def consume_from_topic(self):
        while True:
            try:
                # SIGINT can't be handled when polling, limit timeout to 1 second.
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue

                corporate_update = msg.value()
                if corporate_update is not None:
                    print("User record {}:\n"
                          "\tname: {}\n"
                          "\tclean_name: {}\n"
                          .format(msg.key(), corporate_update.name,
                                  corporate_update.clean_name))
            except KeyboardInterrupt:
                break

        self.consumer.close()
