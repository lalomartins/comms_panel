from mastodon import Mastodon


class BaseMastodonClient:
    _client: Mastodon

    def get_status(self, id) -> dict:
        return self._client.status(id)


class RootClient(BaseMastodonClient):
    def __init__(self) -> None:
        self._client = Mastodon(client_id="var/clientcred.secret")
