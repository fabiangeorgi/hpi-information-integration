from cleanco import basename
from fuzzywuzzy import process, fuzz
from av_crawler.mapper import COMPANY_SYMBOLS
import logging
import os
import abydos.distance as abd
import re

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


COMPANY_NAMES = list(map(lambda x:  basename(x[1].strip()), COMPANY_SYMBOLS))


if __name__ == "__main__":
    saps = ['SAP AG', 'SAP Systems Integration', 'SAP Beteiligungs GmbH', 'SAP Deutschland AG & Co. KG', 'SAP Hosting AG & Co. KG']
    german_posts = ['Deutsche Post AG', 'Deutsche Post Bauen GmbH', 'Deutsche Post Dokumentenservices GmbH', 'Deutsche Post Delta GmbH']
    lufthansas = ['Lufthansa Technik Aktiengesellschaft', 'Deutsche Lufthansa Aktiengesellschaft', 'Lufthansa Systems AKTIENGESELLSCHAFT', 'Lufthansa Cargo AKTIENGESELLSCHAFT', 'Deutsche Schiffsbank AKTIENGESELLSCHAFT']
    eons = ['E.ON AG', 'E.ON Finanzanlagen GmbH']


    threshold = 90
    max_score = 0
    best_result = ''
    comp_name = ''
    for sap in lufthansas:
        cleaned = basename(re.sub(r'aktiengesellschaft', '', sap, flags=re.IGNORECASE)).strip().replace(' ', '')
        result_cleaned = process.extractOne(cleaned, COMPANY_NAMES)
        # logger.info(f"{result_cleaned} {cleaned}")
        # logger.info(f"{len(result_cleaned[0])}, {len(cleaned)}")
        # logger.info(result_cleaned[0].lower().replace(' ', '') in cleaned.lower())
        if result_cleaned[0].lower().replace(' ', '') in cleaned.lower() and (result_cleaned[1] > threshold or re.search('aktiengesellschaft', sap)):
            logger.info(f"{result_cleaned}, score: {result_cleaned[1]}")


        # max = 0
        # best_match = ''
        # for company_name in COMPANY_NAMES:
        #     resul = abd.DiscountedLevenshtein().sim(company_name, cleaned)
        #     if resul > max:
        #         max = resul
        #         best_match = company_name


        # logger.info(f"RESULTS DISCOUNTED \ncompany name: {sap}\nCleaned: {best_match}\nscore: {max}\n")
        # logger.info(f"RESULTS\ncompany name: {sap}\nCleaned: {result_cleaned}\nnot cleaned: {result}\n\n")
    logger.info(f"BEST RESULTS WITH INCLUDE: \ncompany name: {best_result}\nCleaned: {comp_name}\nscore: {max_score}\n")
