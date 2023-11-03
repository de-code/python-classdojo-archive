import dataclasses
from datetime import datetime

from dojo_archive.dojo_api_typing import DojoFeedItemJson
from dojo_archive.utils.datetime import parse_timestamp


@dataclasses.dataclass(frozen=True)
class DojoFeedItem:
    item_json: DojoFeedItemJson
    item_id: str
    time: datetime

    @staticmethod
    def from_item_json(item_json: DojoFeedItemJson):
        return DojoFeedItem(
            item_json=item_json,
            item_id=item_json['_id'],
            time=parse_timestamp(item_json['time'])
        )
