from dojo_archive.dojo_api_typing import DojoFeedItemJson
from dojo_archive.model import DojoFeedItem
from dojo_archive.utils.datetime import parse_timestamp


FEED_ITEM_JSON_1: DojoFeedItemJson = {
    '_id': 'id1',
    'time': '2023-01-02T03:04:05.678Z'
}


class TestDojoFeedItem:
    def test_should_return_parsed_item_json(self):
        feed_item = DojoFeedItem.from_item_json(FEED_ITEM_JSON_1)
        assert feed_item.item_json == FEED_ITEM_JSON_1
        assert feed_item.item_id == FEED_ITEM_JSON_1['_id']
        assert feed_item.time == parse_timestamp(FEED_ITEM_JSON_1['time'])
