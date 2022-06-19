import json
import logging

import requests

from build.gen.bakdata.corporate_updates.v1.corporate_updates_pb2 import CorporateUpdate
from constant import INPUT_TOPIC
from rb_producer import RbProducer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

count = 0

def search(uri, search_after_id):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        # "from": 0,
        "size": 1,
        "search_after": [search_after_id],
        "query": {
            "match_all": {}
        },
        "sort": [{"_id": "asc"}]
    })
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    response = requests.get(uri, data=query, headers=headers)
    results = json.loads(response.text)
    # Last entry
    if len(results['hits']['hits']) == 0:
        raise Exception
    return results['hits']['hits'][0]['_source']


def mapEntry(result):
    corporate_update = CorporateUpdate()
    global count
    print(count)
    count+=1


class RbCleaner:
    def __init__(self):
        self.producer = RbProducer()


    def clean(self):
        first_document = "00001230-acba-48a8-9780-afdbb303af74"
        last_document = "ffffd88b-d241-4a6c-b2e3-bf1b6680e69a"
        previous_document_id = first_document

        while True:
            try:
                result = search(f'http://localhost:9200/{INPUT_TOPIC}/_search?pretty=true', previous_document_id)
                previous_document_id = result["id"]
                mapEntry(result)
            except Exception as ex:
                print('Reached end! Mapping is finished')
                break
        print("finish")
