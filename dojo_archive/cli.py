from datetime import datetime, timezone
import logging
import sys
import json
from pathlib import Path

import dotenv

import requests
from dojo_archive.archiver import FeedItemArchiver

from dojo_archive.client import DojoClient, LoggedOutException
from dojo_archive.config import DojoConfig


LOGGER = logging.getLogger(__name__)


def run(config: DojoConfig):
    LOGGER.info('config: %r', config)
    state_file_path = Path(config.state_file)
    cookies_file_path = Path(config.cookies_file)
    min_timestamp = datetime(
        year=config.min_date.year,
        month=config.min_date.month,
        day=config.min_date.day,
        tzinfo=timezone.utc
    )
    if state_file_path.exists():
        min_timestamp = datetime.fromisoformat(
            json.loads(state_file_path.read_text('utf-8'))['min_timestamp']
        )
    with requests.Session() as session:
        archiver = FeedItemArchiver(
            output_dir=config.output_dir,
            requests_session=session
        )
        client = DojoClient(
            config=config,
            session=session,
            min_timestamp=min_timestamp
        )
        if cookies_file_path.exists():
            LOGGER.info('loading existing cookies')
            session.cookies.update(json.loads(
                cookies_file_path.read_text(encoding='utf-8')
            ))
        else:
            LOGGER.info('logging in')
            client.login()

        feed_item_iterable = client.iter_feed_items()
        for archived_feed_item in archiver.iter_archive_feed_items(
            feed_item_iterable
        ):
            min_timestamp = max(min_timestamp, archived_feed_item.time)

        LOGGER.info('cookies=%r', session.cookies.get_dict())
        cookies_file_path.write_text(
            json.dumps(session.cookies.get_dict()),
            encoding='utf-8'
        )
        state_file_path.write_text(
            json.dumps({'min_timestamp': min_timestamp.isoformat()}),
            encoding='utf-8'
        )


def main():
    dotenv.load_dotenv()
    config = DojoConfig.from_env()
    try:
        run(config)
    except LoggedOutException:
        print('ERROR: You appear to be logged out. Check cookie value.')
        sys.exit(1)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()
