from mastodon import Mastodon


class BaseMastodonClient:
    _client: Mastodon

    def get_status(self, id) -> dict:
        return self._client.status(id)


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
