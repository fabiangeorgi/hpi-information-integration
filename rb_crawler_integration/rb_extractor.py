import logging
from time import sleep
import re
import requests
from parsel import Selector

from build.gen.bakdata.corporate_updates.v1.corporate_updates_pb2 import CorporateUpdate, EventType, Person
from rb_producer import RbProducer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BIRTHDAY_MATCHER = '\*\d{2}.\d{2}.\d{4}'
ADDRESS_MATCHER = '\(*[\w*\-*\s*\.*]*\s\d{1,3},\s\d{5}\s[A-Z][a-z]*\)*.'


class RbExtractor:
    def __init__(self, start_rb_id: int, state: str):
        self.rb_id = start_rb_id
        self.state = state
        self.producer = RbProducer()
        self.id = 1

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

                # TODO clean name of company and use as key -> or even use HRB number

                raw_text: str = selector.xpath("/html/body/font/table/tr[6]/td/text()").get()
                self.handle_events(selector, event_type, raw_text)
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

    def handle_events(self, selector, event_type, raw_text):
        if event_type == "Veränderungen":
            self.handle_changes(selector, raw_text)
        else:
            log.info(f"Skipping {self.id} as it's status is not change")
            self.id += 1
        # if event_type == "Neueintragungen":
        #     self.handle_new_entries(selector, raw_text)
        # elif event_type == "Veränderungen":
        #     self.handle_changes(selector, raw_text)
        # elif event_type == "Löschungen":
        #     self.handle_deletes(selector, raw_text)


    def extract_information_from_raw_text(self, selector, raw_text: str):
        # TODO check if we can clean the company name (match with our stock data name) cleanco!
        re_address = [x for x in re.finditer(pattern=ADDRESS_MATCHER, string=raw_text)]

        # print(raw_text)
        text = raw_text[re_address[0].span()[1]:].strip()
        text = [x for x in re.split(f'{BIRTHDAY_MATCHER}.|;', text) if x != '']
        # [print(x, '\n') for x in text]
        deletion = False
        corporates = []
        corporate_update = CorporateUpdate()
        for t in text:
            old_event_type = corporate_update.event_type
            if t.lower().find("prokura") != -1:
                if old_event_type != EventType.EVENT_PROKURA and old_event_type:
                    corporates.append(corporate_update)
                    corporate_update = CorporateUpdate()
                corporate_update.event_type = EventType.EVENT_PROKURA
            elif t.lower().find("hauptversammlung") != -1:
                if old_event_type != EventType.EVENT_HAUPTVERSAMMLUNG and old_event_type:
                    corporates.append(corporate_update)
                    corporate_update = CorporateUpdate()
                corporate_update.event_type = EventType.EVENT_HAUPTVERSAMMLUNG
            elif t.lower().find("vorstand") != -1 or t.lower().find("geschäftsführer") != -1:
                if old_event_type != EventType.EVENT_VORSTAND and old_event_type:
                    corporates.append(corporate_update)
                    corporate_update = CorporateUpdate()
                corporate_update.event_type = EventType.EVENT_VORSTAND
            elif t.lower().find("insolvenz") != -1:
                if old_event_type != EventType.EVENT_INSOLVENZ and old_event_type:
                    corporates.append(corporate_update)
                    corporate_update = CorporateUpdate()
                corporate_update.event_type = EventType.EVENT_INSOLVENZ
            else:
                if old_event_type != EventType.EVENT_UNKNOWN and old_event_type:
                    corporates.append(corporate_update)
                    corporate_update = CorporateUpdate()
                corporate_update.event_type = EventType.EVENT_UNKNOWN

            if corporate_update.id == 0:
                corporate_update.id = self.id
                self.id = self.id + 1
                corporate_update.event_date = selector.xpath("/html/body/font/table/tr[4]/td/text()").get()
                corporate_update.state = self.state
                corporate_update.name = raw_text.split(', ')[0].strip()
                corporate_update.address = re_address[0].group().replace('(', '').replace(')', "")[:-1].strip()

            if 'erloschen' in t.lower() or 'nicht mehr' in t.lower() or 'ausgeschieden' in t.lower():
                deletion = True
            elif 'gesamtprokura' in t.lower() or 'bestellt' in t.lower():
                deletion = False
            t = t.split(': ')[-1].strip(', ')
            if len(t.replace('.', ' ').split(', ')) == 3:
                surname, name, birth_location = t.replace('.', ' ').split(', ')
                surname = surname.split(': ')[-1]
                person = Person()
                person.name_addition = ' '.join(surname.split(' ')[:-1]).strip() if len(
                    ' '.join(surname.split(' ')[:-1]).strip()) < 10 else ''
                person.first_name = name.strip()
                person.last_name = surname.split(' ')[-1].strip()
                person.birth_location = birth_location.strip()
                if deletion:
                    corporate_update.personsDelete.append(person)
                else:
                    corporate_update.personsAdd.append(person)

            else:
                birthdays = re.finditer(pattern=BIRTHDAY_MATCHER, string=t)
                for match in birthdays:
                    birthday = match.group().replace("*", '')
                    personal_information = t[:match.span()[0]].strip().split(': ')
                    if 'erloschen' in ' '.join(personal_information).lower() or 'nicht mehr' in ' '.join(personal_information).lower() or 'ausgeschieden' in ' '.join(personal_information).lower():
                        deletion = True
                    elif 'gesamtprokura' in t.lower() or 'bestellt' in t.lower():
                        deletion = False
                    if len(personal_information) > 1:
                        personal_information = ' '.join(personal_information[1:]).split(',')
                    else:
                        personal_information = ' '.join(personal_information).split(',')
                    if 3 <= len(personal_information) <= 4:
                        # print(personal_information)
                        surname, name, birth_location = personal_information[0:3]
                        person = Person()
                        person.name_addition = ' '.join(surname.split(' ')[:-1]).strip()
                        person.birthday = birthday
                        person.first_name = name.strip()
                        person.last_name = surname.split(' ')[-1].strip()
                        person.birth_location = birth_location.strip()
                        if deletion:
                            corporate_update.personsDelete.append(person)
                        else:
                            corporate_update.personsAdd.append(person)
        corporates.append(corporate_update)
        return corporates

    def extract_change_information(self, selector: Selector, raw_text: str) -> CorporateUpdate:
        corporate_updates = self.extract_information_from_raw_text(selector, raw_text)
        return corporate_updates

    def handle_changes(self, selector, raw_text: str):
        corporate_updates = self.extract_change_information(selector, raw_text)
        print(corporate_updates)
        for corporate_update in corporate_updates:
            if corporate_update.id != 0:
                self.producer.produce_to_topic(corporate_update=corporate_update)
