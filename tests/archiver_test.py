import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from dojo_archive.archiver import FeedItemArchiver
from dojo_archive.dojo_api_typing import (
    DojoFeedItemAttachmentJson,
    DojoFeedItemAttachmentMetadataJson,
    DojoFeedItemJson
)
from dojo_archive.model import DojoFeedItem


PDF_BYTES_1 = b'PDF 1'

PDF_ATTACHMENT_METADATA_JSON_1: DojoFeedItemAttachmentMetadataJson = {
    'mimetype': 'application/pdf',
    'filename': 'File 1.pdf'
}

PDF_ATTACHMENT_JSON_1: DojoFeedItemAttachmentJson = {
    'path': 'https://example.com/file1.pdf',
    'metadata': PDF_ATTACHMENT_METADATA_JSON_1
}

IMAGE_ATTACHMENT_METADATA_WITHOUT_FILENAME_JSON_1: DojoFeedItemAttachmentMetadataJson = {
    'mimetype': 'image/jpeg'
}

IMAGE_ATTACHMENT_WITHOUT_FILENAME_JSON_1: DojoFeedItemAttachmentJson = {
    'path': 'https://example.com/file1.jpg',
    'metadata': IMAGE_ATTACHMENT_METADATA_WITHOUT_FILENAME_JSON_1
}

IMAGE_ATTACHMENT_WITHOUT_METADATA_JSON_1: DojoFeedItemAttachmentJson = {
    'path': 'https://example.com/file1.jpg'
}

FEED_ITEM_JSON_1: DojoFeedItemJson = {
    '_id': 'id1',
    'time': '2023-01-02T03:04:05.678Z'
}


@pytest.fixture(name='feed_item_archiver')
def _feed_item_archiver(tmp_path: Path, requests_session_mock: MagicMock):
    return FeedItemArchiver(
        output_dir=str(tmp_path.joinpath('output')),
        requests_session=requests_session_mock
    )


class TestFeedItemArchiver:
    def test_should_write_item_json(self, feed_item_archiver: FeedItemArchiver):
        feed_item_archiver.archive_feed_items([
            DojoFeedItem.from_item_json(FEED_ITEM_JSON_1)
        ])
        item_json_path = feed_item_archiver.get_item_json_path_by_id(FEED_ITEM_JSON_1['_id'])
        assert item_json_path.exists()
        assert json.loads(item_json_path.read_text('utf-8')) == FEED_ITEM_JSON_1

    def test_should_strip_query_parameters(self, feed_item_archiver: FeedItemArchiver):
        attachment_json: DojoFeedItemAttachmentJson = {
            'path': 'https://example.com/file1.pdf?query=param'
        }
        feed_item = DojoFeedItem.from_item_json({
            **FEED_ITEM_JSON_1,
            'contents': {
                'attachments': [attachment_json]
            }
        })
        file_path = feed_item_archiver.get_item_attachment_path(
            feed_item=feed_item,
            attachment_json=attachment_json
        )
        assert file_path.name.endswith('file1.pdf')

    def test_should_write_pdf(
        self,
        feed_item_archiver: FeedItemArchiver,
        requests_response_mock: MagicMock
    ):
        requests_response_mock.content = PDF_BYTES_1
        feed_item = DojoFeedItem.from_item_json({
            **FEED_ITEM_JSON_1,
            'contents': {
                'attachments': [PDF_ATTACHMENT_JSON_1]
            }
        })
        feed_item_archiver.archive_feed_items([feed_item])
        attachment_path = feed_item_archiver.get_item_attachment_path(
            feed_item=feed_item,
            attachment_json=PDF_ATTACHMENT_JSON_1
        )
        assert attachment_path.exists()
        assert attachment_path.read_bytes() == PDF_BYTES_1

    def test_should_support_attachment_without_metadata_filename(
        self,
        feed_item_archiver: FeedItemArchiver
    ):
        feed_item = DojoFeedItem.from_item_json({
            **FEED_ITEM_JSON_1,
            'contents': {
                'attachments': [IMAGE_ATTACHMENT_WITHOUT_FILENAME_JSON_1]
            }
        })
        assert feed_item_archiver.get_item_attachment_path(
            feed_item=feed_item,
            attachment_json=IMAGE_ATTACHMENT_WITHOUT_FILENAME_JSON_1
        )

    def test_should_support_attachment_without_metadata(
        self,
        feed_item_archiver: FeedItemArchiver
    ):
        feed_item = DojoFeedItem.from_item_json({
            **FEED_ITEM_JSON_1,
            'contents': {
                'attachments': [IMAGE_ATTACHMENT_WITHOUT_METADATA_JSON_1]
            }
        })
        assert feed_item_archiver.get_item_attachment_path(
            feed_item=feed_item,
            attachment_json=IMAGE_ATTACHMENT_WITHOUT_METADATA_JSON_1
        )
