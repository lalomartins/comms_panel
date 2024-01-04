import sys
from mastodon import Mastodon

Mastodon.create_app(
    "comms-panel", api_base_url=sys.argv[1], to_file="var/clientcred.secret"
)
