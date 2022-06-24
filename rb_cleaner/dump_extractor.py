import json


class DumpExtractor:

    def extract(self, line: str):
        # Parsing
        parsed_line = json.loads(line)
        result = parsed_line["_source"]

        return result
