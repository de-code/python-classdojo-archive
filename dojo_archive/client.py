import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests

from dojo_archive.config import DojoConfig
from dojo_archive.dojo_api_typing import DojoFeedResponseJson
from dojo_archive.model import DojoFeedItem


class LoggedOutException(RuntimeError):
    pass


class DojoClient:
    def __init__(self, config: DojoConfig, session: requests.Session):
        self.config = config
        self.session = session
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

    def iter_feed_items(self) -> Iterable[DojoFeedItem]:
        response = self.on_response(self.session.get(self.config.feed_url))
        response.raise_for_status()
        response_json: DojoFeedResponseJson = response.json()
        return [
            DojoFeedItem.from_item_json(item_json)
            for item_json in response_json['_items']
        ]
