import click
import logging
import os
import io

from av_crawler.mapper import COMPANY_SYMBOLS
from rb_cleaner.dump_extractor import DumpExtractor
from rb_cleaner.dump_parser import DumpParser
from rb_cleaner.rb_producer import RbProducer
from cleanco import basename
from fuzzywuzzy import process
import re

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

COMPANY_NAMES = list(map(lambda x: x[1].strip(), COMPANY_SYMBOLS))
SCORE_THRESHOLD = 80

def run(file: str):
    input_file = io.open(file, "r", buffering=1, encoding="utf-8")
    extractor = DumpExtractor()
    parser = DumpParser()
    producer = RbProducer()

    while input_file.readable():
        line = input_file.readline()

        if not line:
            break

        corporate_update_json = extractor.extract(line)

        corporate_update = parser.serialize(corporate_update_json)

        if not corporate_update:
            break

        # cleaning and transformation
        cleaned_name = basename(re.sub(r'aktiengesellschaft', '', corporate_update.name, flags=re.IGNORECASE)).strip().replace(' ', '')
        index = -1
        match_score = 0
        try:
            index = COMPANY_NAMES.index(cleaned_name)
            match_score = 100
        except ValueError:
            pass

        if index == -1:
            threshold = 90
            result = process.extractOne(cleaned_name, COMPANY_NAMES)
            if result[0].lower().replace(' ', '') in cleaned_name.lower() and (result[1] > threshold or (result[1] >= threshold and re.search(r'(aktiengesellschaft$|\sag$|\sse$)', corporate_update.name, flags=re.IGNORECASE))):
                index = COMPANY_NAMES.index(result[0])
                match_score = result[1]

        corporate_update.reference_company_id = index
        corporate_update.clean_name = cleaned_name
        corporate_update.match_score = match_score

        producer.produce_to_topic(corporate_update)

    input_file.close()


if __name__ == "__main__":
    file = "/Users/georgi/Desktop/integration.json"
    run(file)
