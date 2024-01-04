from mastodon import Mastodon


class RootClient:
    def __init__(self, base_url: str) -> None:
        self._client = Mastodon(api_base_url=base_url)

    def get_status(self, id) -> dict:
        return self._client.status(id)
