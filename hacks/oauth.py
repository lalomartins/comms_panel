import sys, os

sys.path.append(os.getcwd())

from comms_panel.backends.mastodon.client import RootClient

client = RootClient()
print(f"Log in to {client.auth_request_url()}")
code = input("Auth code: ").strip()
client.oauth_login(code)
