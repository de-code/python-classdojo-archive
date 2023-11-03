import json
from pathlib import Path

from dojo_archive.archiver import FeedItemArchiver
from dojo_archive.dojo_api_typing import DojoFeedItemJson
from dojo_archive.model import DojoFeedItem


FEED_ITEM_JSON_1: DojoFeedItemJson = {
    '_id': 'id1',
    'time': '2023-01-02T03:04:05.678Z'
}


class TestFeedItemArchiver:
    def test_should_write_item_json(self, tmp_path: Path):
        archiver = FeedItemArchiver(str(tmp_path.joinpath('output')))
        archiver.archive_feed_items([
            DojoFeedItem.from_item_json(FEED_ITEM_JSON_1)
        ])
        item_json_path = archiver.get_item_json_path_by_id(FEED_ITEM_JSON_1['_id'])
        assert item_json_path.exists()
        assert json.loads(item_json_path.read_text('utf-8')) == FEED_ITEM_JSON_1
