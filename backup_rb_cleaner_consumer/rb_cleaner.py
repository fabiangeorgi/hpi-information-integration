import logging

from rb_consumer import RbConsumer
from rb_producer import RbProducer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class RbCleaner:
    def __init__(self):
        self.consumer = RbConsumer()
        self.producer = RbProducer()

    def clean(self):
        while True:
            try:
                # # Response format is {TopicPartiton('topic1', 1): [msg1, msg2]}
                # msg_pack = self.consumer.consume_from_topic()
                #
                # for tp, messages in msg_pack.items():
                #     for message in messages:
                #         log.error("%s:%d:%d: key=%s value=%s" % (tp.topic, tp.partition,
                #                                               message.offset, message.key,
                #                                               message.value))
                msg = self.consumer.consumer.poll(1.0)
                if msg is None:
                    continue

                corporate_update = msg.value()
                if corporate_update is not None:
                    print("User record {}:\n"
                          "\tname: {}\n"
                          "\tclean_name: {}\n"
                          .format(msg.key(), corporate_update.name,
                                  corporate_update.clean_name))
            except Exception as ex:
                log.error(f"Cause: {ex}")
                continue
