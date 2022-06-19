import json


class DumpExtractor:
    # {"_index": "corporate-events-integration", "_type": "_doc", "_id": "f3f85e2e-44de-492c-90f0-97b3545bfbf7", "_score": 1,
    #  "_source": {"id": "f3f85e2e-44de-492c-90f0-97b3545bfbf7", "name": "HANNI BANI GmbH", "clean_name": "HANNI BANI",
    #              "state": "th", "address": "Mehla Nässa 1, 07950 Zeulenroda", "event_date": "07.09.2006",
    #              "event_type": "EVENT_INSOLVENZ", "personsAdd": [
    #          {"id": "925637420ecd22b6433c457037b64b714bbf7665", "first_name": "Candy", "last_name": "Daßler",
    #           "birthday": "", "birth_location": "Triebes", "name_addition": ""}], "personsDelete": []}}

    def extract(self, line: str):
        # Parsing
        parsed_line = json.loads(line)
        result = parsed_line["_source"]

        return result
