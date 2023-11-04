import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional, cast

import requests

from dojo_archive.config import DojoConfig
from dojo_archive.dojo_api_typing import DojoFeedResponseJson
from dojo_archive.model import DojoFeedItem


LOGGER = logging.getLogger(__name__)


class LoggedOutException(RuntimeError):
    pass


class DojoClient:
    def __init__(
        self,
        config: DojoConfig,
        session: requests.Session,
        min_timestamp: Optional[datetime] = None
    ):
        self.config = config
        self.session = session
        self.min_timestamp = min_timestamp
        self.session_start = datetime.now(timezone.utc)
        self.debug_response_prefix = self.session_start.strftime(r'%Y%m%d-%H%M%S-')
        self.debug_response_counter = 0
        if self.config.debug_response_dir:
            Path(self.config.debug_response_dir).mkdir(parents=True, exist_ok=True)

    def on_response(self, response: requests.Response) -> requests.Response:
        if self.config.debug_response_dir:
            index = self.debug_response_counter
            self.debug_response_counter += 1
            url = response.request.url
            assert url
            name = os.path.basename(url).split('?')[0]
            filename = f'{self.debug_response_prefix}{index}-{name}.json'
            Path(self.config.debug_response_dir).joinpath(
                filename
            ).write_text(
                json.dumps({
                    'request': {
                        'url': url
                    },
                    'response': response.json()
                }, indent=2),
                encoding='utf-8'
            )
        return response

    def login(self):
        response = self.on_response(self.session.post(self.config.login_url, json={
            "login": self.config.email,
            "password": self.config.password,
            "resumeAddClassFlow": False
        }))
        response.raise_for_status()

    def iter_feed_response_json(self) -> Iterable[DojoFeedResponseJson]:
        current_page_url = self.config.feed_url
        while True:
            response = self.on_response(self.session.get(current_page_url))
            response.raise_for_status()
            response_json: DojoFeedResponseJson = response.json()
            yield response_json
            links = response_json.get('_links')
            prev = links and links.get('prev')
            prev_href = prev and prev.get('href')
            if not prev_href:
                return
            current_page_url = cast(str, prev_href)

    def iter_feed_items(self) -> Iterable[DojoFeedItem]:
        for response_json in self.iter_feed_response_json():
            for item_json in response_json['_items']:
                feed_item = DojoFeedItem.from_item_json(item_json)
                LOGGER.debug('feed_item: %r', feed_item)
                if self.min_timestamp and feed_item.time < self.min_timestamp:
                    return
                yield feed_item
