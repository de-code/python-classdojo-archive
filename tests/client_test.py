import dataclasses
from datetime import date
from unittest.mock import call, MagicMock

from dojo_archive.client import DojoClient
from dojo_archive.config import DojoConfig
from dojo_archive.dojo_api_typing import DojoFeedItemJson, DojoFeedResponseJson
from dojo_archive.model import DojoFeedItem


DOJO_CONFIG_1 = DojoConfig(
    email='user@example.com',
    password='password1',
    min_date=date.fromisoformat('2020-01-01'),
    debug_response_dir=None
)


FEED_ITEM_JSON_1: DojoFeedItemJson = {
    '_id': 'id1',
    'time': '2023-01-02T03:04:05.100Z'
}

FEED_ITEM_JSON_2: DojoFeedItemJson = {
    '_id': 'id2',
    'time': '2023-01-02T03:04:05.200Z'
}


PAGE_URL_2 = 'https://test/page_2'


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

    def test_should_process_pagination_links(self, requests_session_mock: MagicMock):
        client = DojoClient(config=DOJO_CONFIG_1, session=requests_session_mock)

        response_json_1: DojoFeedResponseJson = {
            '_items': [FEED_ITEM_JSON_1],
            '_links': {
                'prev': {
                    'href': PAGE_URL_2
                }
            }
        }
        response_json_2: DojoFeedResponseJson = {
            '_items': [FEED_ITEM_JSON_2]
        }

        response_mock = requests_session_mock.get.return_value
        response_mock.json.side_effect = [response_json_1, response_json_2]

        feed_items = list(client.iter_feed_items())
        assert feed_items == [
            DojoFeedItem.from_item_json(FEED_ITEM_JSON_1),
            DojoFeedItem.from_item_json(FEED_ITEM_JSON_2)
        ]

        requests_session_mock.get.assert_has_calls([
            call(DOJO_CONFIG_1.feed_url),
            call(PAGE_URL_2)
        ])

    def test_should_stop_with_feed_item_before_min_date(
        self,
        requests_session_mock: MagicMock
    ):
        client = DojoClient(
            config=dataclasses.replace(
                DOJO_CONFIG_1,
                min_date=date.fromisoformat('2021-01-01')
            ),
            session=requests_session_mock
        )

        item_after_min_date: DojoFeedItemJson = {
            **FEED_ITEM_JSON_1,
            'time': '2022-01-01T00:00:00+00:00'
        }
        item_before_min_date: DojoFeedItemJson = {
            **FEED_ITEM_JSON_2,
            'time': '2020-01-01T00:00:00+00:00'
        }
        response_json: DojoFeedResponseJson = {
            '_items': [item_after_min_date, item_before_min_date],
            '_links': {
                'prev': {
                    'href': PAGE_URL_2
                }
            }
        }

        response_mock = requests_session_mock.get.return_value
        response_mock.json.side_effect = [response_json]

        feed_items = list(client.iter_feed_items())
        assert feed_items == [DojoFeedItem.from_item_json(item_after_min_date)]

        requests_session_mock.get.assert_called_once()
