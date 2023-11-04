import dataclasses
from datetime import date
import os
from typing import Optional


class EnvVarNames:
    DOJO_EMAIL = "DOJO_EMAIL"
    DOJO_PASSWORD = "DOJO_PASSWORD"
    DOJO_MIN_DATE = "DOJO_MIN_DATE"


def get_required_env_value(env_var_name: str) -> str:
    value = os.getenv(env_var_name)
    if not value:
        raise RuntimeError('Environment variable %r is required' % env_var_name)
    return value


@dataclasses.dataclass(frozen=True)
class DojoConfig:  # pylint: disable=too-many-instance-attributes
    email: str
    min_date: date
    password: str = dataclasses.field(repr=False)
    timeout: float = 60
    login_url: str = "https://home.classdojo.com/api/session"
    feed_url: str = "https://home.classdojo.com/api/storyFeed?includePrivate=true"

    cookies_file: str = 'cookies.json'
    state_file: str = 'state.json'
    debug_response_dir: Optional[str] = '.responses'

    output_dir: str = 'output'

    @staticmethod
    def from_env() -> 'DojoConfig':
        return DojoConfig(
            email=get_required_env_value(EnvVarNames.DOJO_EMAIL),
            password=get_required_env_value(EnvVarNames.DOJO_PASSWORD),
            min_date=date.fromisoformat(
                get_required_env_value(EnvVarNames.DOJO_MIN_DATE)
            )
        )
