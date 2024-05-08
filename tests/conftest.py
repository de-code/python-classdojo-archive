import logging
from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    logging.basicConfig(level='INFO')
    for name in ['tests', 'dojo_archive']:
        logging.getLogger(name).setLevel('DEBUG')


@pytest.fixture(name='requests_response_mock')
def _requests_response_mock() -> MagicMock:
    return MagicMock(name='requests_response_mock')


@pytest.fixture(name='requests_session_mock')
def _requests_session_mock(requests_response_mock: MagicMock) -> MagicMock:
    session = MagicMock(name='requests_session')
    session.request.return_value = requests_response_mock
    session.post.return_value = requests_response_mock
    session.get.return_value = requests_response_mock
    return session
