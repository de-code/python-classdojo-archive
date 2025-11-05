import json
import logging
import os
from pathlib import Path
from typing import Iterable, Optional, Sequence

import requests

from dojo_archive.client import DojoFeedItem
from dojo_archive.dojo_api_typing import DojoFeedItemAttachmentJson


LOGGER = logging.getLogger(__name__)


class FeedItemArchiver:
    def __init__(self, output_dir: str, requests_session: requests.Session):
        self.output_dir_path = Path(output_dir)
        self.requests_session = requests_session
        self.item_json_dir_path = self.output_dir_path.joinpath('item-json')
        self.item_json_dir_path.mkdir(parents=True, exist_ok=True)
        self.item_attachments_dir_path = self.output_dir_path.joinpath('attachments')
        self.item_attachments_dir_path.mkdir(parents=True, exist_ok=True)

    def get_item_json_path_by_id(self, item_id: str) -> Path:
        return self.item_json_dir_path.joinpath(f'{item_id}.json')

    def get_item_attachment_path(
        self,
        feed_item: DojoFeedItem,
        attachment_json: DojoFeedItemAttachmentJson
    ) -> Path:
        metadata_json = attachment_json.get('metadata')
        filename = metadata_json and metadata_json.get('filename')
        if not filename:
            filename = os.path.basename(attachment_json['path'])
        filename = filename.split('?', maxsplit=1)[0]
        return self.item_attachments_dir_path.joinpath(
            f'{feed_item.time.date().isoformat()}-{feed_item.item_id}-{filename}'
        )

    def archive_feed_item_attachment(
        self,
        feed_item: DojoFeedItem,
        attachment_json: DojoFeedItemAttachmentJson
    ):
        attachment_path = self.get_item_attachment_path(
            feed_item=feed_item,
            attachment_json=attachment_json
        )
        if attachment_path.exists():
            LOGGER.debug('attachment already downloaded: %r', attachment_path)
            return
        attachment_url = attachment_json['path']
        response = self.requests_session.get(attachment_url)
        attachment_path.write_bytes(response.content)

    def archive_feed_item_attachments(
        self,
        feed_item: DojoFeedItem,
        attachment_json_list: Optional[Sequence[DojoFeedItemAttachmentJson]]
    ):
        if attachment_json_list:
            for attachment_json in attachment_json_list:
                self.archive_feed_item_attachment(
                    feed_item=feed_item,
                    attachment_json=attachment_json
                )

    def archive_feed_item(self, feed_item: DojoFeedItem):
        LOGGER.info('archiving: %r', feed_item)
        item_json_path = self.get_item_json_path_by_id(feed_item.item_id)
        item_json_path.write_text(
            json.dumps(feed_item.item_json, indent=2),
            encoding='utf-8'
        )
        feed_content_json = feed_item.item_json.get('contents')
        if feed_content_json:
            self.archive_feed_item_attachments(
                feed_item=feed_item,
                attachment_json_list=feed_content_json.get('attachments')
            )

    def iter_archive_feed_items(self, feed_item_iterable: Iterable[DojoFeedItem]):
        for feed_item in feed_item_iterable:
            self.archive_feed_item(feed_item)
            yield feed_item

    def archive_feed_items(self, feed_item_iterable: Iterable[DojoFeedItem]):
        for _ in self.iter_archive_feed_items(feed_item_iterable):
            pass
