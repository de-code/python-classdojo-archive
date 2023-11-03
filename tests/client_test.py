from unittest.mock import MagicMock

import pytest

from dojo_archive.client import DojoClient
from dojo_archive.config import DojoConfig
from dojo_archive.dojo_api_typing import DojoFeedItemJson, DojoFeedResponseJson
from dojo_archive.model import DojoFeedItem


DOJO_CONFIG_1 = DojoConfig(
    email='user@example.com',
    password='password1',
    debug_response_dir=None
)


FEED_ITEM_JSON_1: DojoFeedItemJson = {
    '_id': 'id1',
    'time': '2023-01-02T03:04:05.678Z'
}


@pytest.fixture(name='requests_session_mock')
def _requests_session_mock() -> MagicMock:
    return MagicMock(name='requests_session')


class TestDojoClient:
    def test_should_login(self, requests_session_mock: MagicMock):
        client = DojoClient(config=DOJO_CONFIG_1, session=requests_session_mock)
        client.login()
        requests_session_mock.post.assert_called_with(
            DOJO_CONFIG_1.login_url,
            json={
                'login': DOJO_CONFIG_1.email,
                'password': DOJO_CONFIG_1.password,
                'resumeAddClassFlow': False
            }
        )
        response_mock = requests_session_mock.post.return_value
        response_mock.raise_for_status.assert_called()

    def test_should_return_feed_items(self, requests_session_mock: MagicMock):
        client = DojoClient(config=DOJO_CONFIG_1, session=requests_session_mock)

        response_json: DojoFeedResponseJson = {
            '_items': [FEED_ITEM_JSON_1]
        }

        response_mock = requests_session_mock.get.return_value
        response_mock.json.return_value = response_json

        feed_items = list(client.iter_feed_items())
        assert feed_items == [DojoFeedItem.from_item_json(FEED_ITEM_JSON_1)]

        requests_session_mock.get.assert_called_with(
            DOJO_CONFIG_1.feed_url
        )
        response_mock.raise_for_status.assert_called()