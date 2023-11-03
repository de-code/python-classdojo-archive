import json
import logging
from pathlib import Path
from typing import Iterable

from dojo_archive.client import DojoFeedItem


LOGGER = logging.getLogger(__name__)


class FeedItemArchiver:
    def __init__(self, output_dir: str):
        self.output_dir_path = Path(output_dir)
        self.item_json_dir_path = self.output_dir_path.joinpath('item-json')
        self.item_json_dir_path.mkdir(parents=True, exist_ok=True)

    def get_item_json_path_by_id(self, item_id: str) -> Path:
        return self.item_json_dir_path.joinpath(f'{item_id}.json')

    def archive_feed_item(self, feed_item: DojoFeedItem):
        LOGGER.info('archiving: %r', feed_item)
        item_json_path = self.get_item_json_path_by_id(feed_item.item_id)
        item_json_path.write_text(
            json.dumps(feed_item.item_json, indent=2),
            encoding='utf-8'
        )

    def archive_feed_items(self, feed_item_iterable: Iterable[DojoFeedItem]):
        for feed_item in feed_item_iterable:
            self.archive_feed_item(feed_item)
