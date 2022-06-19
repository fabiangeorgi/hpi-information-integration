import click
import logging
import os
import io

from av_crawler.mapper import COMPANY_SYMBOLS
from cleaner.dump_extractor import DumpExtractor
from cleaner.dump_parser import DumpParser
from cleaner.rb_producer import RbProducer
from cleanco import basename
from fuzzywuzzy import process

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
        cleaned_name = basename(corporate_update.name.replace('Aktiengesellschaft', '')).strip()
        index = -1
        try:
            index = COMPANY_NAMES.index(cleaned_name)
        except ValueError:
            pass

        if index == -1:
            # use fuzzy search
            # TODO set the threshold better
            result = process.extractOne(cleaned_name, COMPANY_NAMES)
            if result[1] > SCORE_THRESHOLD:
                index = COMPANY_NAMES.index(result[0])

        corporate_update.reference_company_id = index
        corporate_update.clean_name = cleaned_name

        producer.produce_to_topic(corporate_update)

    input_file.close()


if __name__ == "__main__":
    file = "/Users/georgi/Desktop/integration.json"
    run(file)
