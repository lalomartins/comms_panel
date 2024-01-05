from datetime import datetime
from typing import Callable
from mastodon import Mastodon

from comms_panel.backends.timeline import Timeline


class BaseMastodonClient:
    _client: Mastodon

    def get_status(self, id) -> dict:
        return self._client.status(id)

    def home_timeline(self, title: str = "Home", update_period=None) -> Timeline:
        return MastodonTimeline(
            self, self._client.timeline_home, title=title, update_period=update_period
        )

    def local_timeline(self, title: str = "Local", update_period=None) -> Timeline:
        return MastodonTimeline(
            self, self._client.timeline_local, title=title, update_period=update_period
        )


class RootClient(BaseMastodonClient):
    def __init__(self) -> None:
        self._client = Mastodon(client_id="var/clientcred.secret")

    def oauth_login(self, code) -> None:
        self._client.log_in(
            code=code, scopes=["read", "write", "follow"], to_file="var/usercred.secret"
        )

    def auth_request_url(self) -> str:
        return self._client.auth_request_url()


class UserClient(BaseMastodonClient):
    def __init__(self) -> None:
        self._client = Mastodon(access_token="var/usercred.secret")


class MastodonTimeline(Timeline):
    _client: BaseMastodonClient
    _method: Callable[[], list[dict]]

    def __init__(self, client, method, title: str = "", update_period=None) -> None:
        self._client = client
        self._method = method
        self.title = title
        self.update_period = update_period
        self.statuses = []

    def update(self):
        self.statuses = self._method()
        self.updated = datetime.now()
        if self.update_period is not None:
            self.next_update = self.updated + self.update_period
