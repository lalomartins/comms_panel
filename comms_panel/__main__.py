import asyncio
import logging
from .app import App


async def main():
    app = App()
    await app.run()


logging.root.setLevel(logging.DEBUG)
asyncio.run(main())
