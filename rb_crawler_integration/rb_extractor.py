import logging
from time import sleep

import requests
from parsel import Selector

from build.gen.bakdata.corporate_updates.v1.corporate_updates_pb2 import Corporate, Status, CorporateUpdate, EventType
from rb_producer import RbProducer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class RbExtractor:
    def __init__(self, start_rb_id: int, state: str):
        self.rb_id = start_rb_id
        self.state = state
        self.producer = RbProducer()

    def extract(self):
        while True:
            try:
                log.info(f"Sending Request for: {self.rb_id} and state: {self.state}")
                text = self.send_request()
                if "Falsche Parameter" in text:
                    log.info("The end has reached")
                    break
                selector = Selector(text=text)

                event_type = selector.xpath("/html/body/font/table/tr[3]/td/text()").get()

                id = f"{self.state}_{self.rb_id}"

                # TODO clean name of company and use as key -> or even use HRB number

                raw_text: str = selector.xpath("/html/body/font/table/tr[6]/td/text()").get()
                self.handle_events(id, selector, event_type, raw_text)
                self.rb_id = self.rb_id + 1
            except Exception as ex:
                log.error(f"Skipping {self.rb_id} in state {self.state}")
                log.error(f"Cause: {ex}")
                self.rb_id = self.rb_id + 1
                continue
        exit(0)

    def send_request(self) -> str:
        url = f"https://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?rb_id={self.rb_id}&land_abk={self.state}"
        # For graceful crawling! Remove this at your own risk!
        # sleep(0.01)
        return requests.get(url=url).text

    @staticmethod
    def extract_company_reference_number(selector: Selector) -> str:
        return ((selector.xpath("/html/body/font/table/tr[1]/td/nobr/u/text()").get()).split(": ")[1]).strip()

    def handle_events(self, id, selector, event_type, raw_text):
        if event_type == "Neueintragungen":
            self.handle_new_entries(id, selector, raw_text)
        elif event_type == "Veränderungen":
            self.handle_changes(id, selector, raw_text)
        elif event_type == "Löschungen":
            self.handle_deletes(id, selector)

    def handle_new_entries(self, id, selector, raw_text: str) -> Corporate:
        log.debug(f"New company found: {selector.id}")
        selector.event_type = "create"
        selector.information = raw_text
        selector.status = Status.STATUS_ACTIVE
        # self.producer.produce_to_topic(corporate=corporate)

    @staticmethod
    def extract_change_information(corporate_update: CorporateUpdate, raw_text: str) -> CorporateUpdate:
        if raw_text.lower().find("prokura") != -1:
            corporate_update.event_type = EventType.PROKURA
        elif raw_text.lower().find("hauptversammlung") != -1:
            corporate_update.event_type = EventType.HAUPTVERSAMMLUNG
        else:
            corporate_update.event_type = EventType.UNKNOWN
        return corporate_update

    def handle_changes(self, id, selector, raw_text: str):
        # uint32 id = 1;
        # string event_date = 2;
        # EventType event_type = 3;
        # repeated Person personsAdd = 4;
        # repeated Person personsDelete = 5;
        corporate = Corporate()
        corporate_update = CorporateUpdate()
        corporate_update.id = 1
        corporate_update.event_date = selector.xpath("/html/body/font/table/tr[4]/td/text()").get()

        corporate_update = self.extract_change_information(corporate_update, raw_text)

        corporate.update.append(corporate_update)
        log.error("test")

        self.producer.produce_to_topic(corporate=corporate)

    def handle_deletes(self, selector):
        log.debug(f"Company {selector.id} is inactive")
        selector.event_type = "delete"
        selector.status = Status.STATUS_INACTIVE
        # self.producer.produce_to_topic(corporate=corporate)
