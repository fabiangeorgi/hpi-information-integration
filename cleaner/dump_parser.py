import logging
from google.protobuf.json_format import ParseDict

from build.gen.bakdata.corporate_updates.v1.corporate_updates_pb2 import CorporateUpdate


logger = logging.getLogger(__name__)


class DumpParser:
    def serialize(self, corporate_update_json) -> CorporateUpdate:
        try:
            patent = ParseDict(corporate_update_json, CorporateUpdate())

            return patent
        except Exception as ex:
            logger.error("Serializing failed", ex)
            return None
