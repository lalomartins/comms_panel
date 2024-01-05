"""Main module."""

from asyncio import get_event_loop
from datetime import timedelta, datetime
import wx, wx.html
from wxasync import WxAsyncApp, StartCoroutine

from comms_panel.backends.mastodon.client import RootClient, UserClient
from comms_panel.widgets.timeline import TimelinePanel


class App(WxAsyncApp):
    def __init__(self):
        super().__init__(False)
        self.root_client = RootClient()
        self.user_client = UserClient()
        self.frame = wx.Frame(None, wx.ID_ANY, "Comms Panel")
        self.SetTopWindow(self.frame)
        self.frame.MinSize = wx.Size(800, 600)
        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.frame.SetSizer(self.panel_sizer)
        self.frame.SetAutoLayout(1)
        self.panel_sizer.Fit(self.frame)
        size = wx.Size(380, 600)
        self.panels = []
        offset = 0
        now = datetime.now()
        for factory in [
            self.user_client.home_timeline,
            self.user_client.local_timeline,
        ]:
            panel = TimelinePanel(
                self.frame, factory(update_period=timedelta(minutes=2)), size=size
            )
            panel.timeline.next_update = now + timedelta(seconds=offset)
            offset += 3
            self.panels.append(panel)
        self.panel_sizer.AddMany((panel, 1, wx.EXPAND) for panel in self.panels)

    async def run(self):
        self.frame.Show(True)
        loop = get_event_loop()
        for panel in self.panels:
            StartCoroutine(panel.auto_update(), panel)
        await self.MainLoop()
