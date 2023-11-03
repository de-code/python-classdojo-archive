import dataclasses
import os
from typing import Optional


class EnvVarNames:
    DOJO_EMAIL = "DOJO_EMAIL"
    DOJO_PASSWORD = "DOJO_PASSWORD"


def get_required_env_value(env_var_name: str) -> str:
    value = os.getenv(env_var_name)
    if not value:
        raise RuntimeError('Environment variable %r is required' % env_var_name)
    return value


@dataclasses.dataclass(frozen=True)
class DojoConfig:  # pylint: disable=too-many-instance-attributes
    email: str
    password: str = dataclasses.field(repr=False)
    timeout: float = 60
    login_url: str = "https://home.classdojo.com/api/session"
    feed_url: str = "https://home.classdojo.com/api/storyFeed?includePrivate=true"

    cookies_file: str = 'cookies.json'
    debug_response_dir: Optional[str] = '.responses'

    output_dir: str = 'output'
    # date_format: str = 'YYYY-MM-DD'
    # max_feeds: int = 30
    # concurrency: int = 15

    @staticmethod
    def from_env() -> 'DojoConfig':
        return DojoConfig(
            email=get_required_env_value(EnvVarNames.DOJO_EMAIL),
            password=get_required_env_value(EnvVarNames.DOJO_PASSWORD)
        )
