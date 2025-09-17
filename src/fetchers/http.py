from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

def get_session():
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    timeout = (5, 15)
    session.request = _wrap_request_with_timeout(session.request, timeout)
    return session

def _wrap_request_with_timeout(request_func, timeout):
    def wrapper(method, url, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = timeout
        return request_func(method, url, **kwargs)
    return wrapper