"""Main module."""

from datetime import timedelta
import wx, wx.html

from comms_panel.backends.mastodon.client import RootClient, UserClient
from comms_panel.widgets.timeline import TimelinePanel


class App(wx.App):
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
        size = wx.Size(400, 600)
        self.panels = [
            TimelinePanel(self.frame, factory(update_period=timedelta(minutes=2)))
            for factory in [
                self.user_client.home_timeline,
                self.user_client.local_timeline,
            ]
        ]
        self.panel_sizer.AddMany((panel, 1, wx.EXPAND) for panel in self.panels)

    def run(self):
        self.frame.Show(True)
        self.MainLoop()

    def load_posts(self):
        for panel in self.panels:
            panel.update()
