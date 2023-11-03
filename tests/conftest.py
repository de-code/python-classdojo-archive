from unittest.mock import MagicMock

import pytest


@pytest.fixture(name='requests_response_mock')
def _requests_response_mock() -> MagicMock:
    return MagicMock(name='requests_response_mock')


@pytest.fixture(name='requests_session_mock')
def _requests_session_mock(requests_response_mock: MagicMock) -> MagicMock:
    session = MagicMock(name='requests_session')
    session.post.return_value = requests_response_mock
    session.get.return_value = requests_response_mock
    return session
