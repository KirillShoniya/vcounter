from datetime import datetime
from urllib.parse import urlparse


def now_timestamp() -> int:
    return int(datetime.utcnow().timestamp())


def url_to_domain(url: str) -> str:
    if ':' not in url:
        url = f'https://{url}'

    return urlparse(url).netloc
