"""Main module."""

import wx, wx.html

from comms_panel.backends.mastodon.client import RootClient, UserClient


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
            wx.html.HtmlWindow(self.frame, size=size),
            wx.html.HtmlWindow(self.frame, size=size),
        ]
        self.panel_sizer.AddMany((panel, 1, wx.EXPAND) for panel in self.panels)

    def run(self):
        self.frame.Show(True)
        self.MainLoop()

    def load_posts(self, ids: list):
        for i, id in enumerate(ids):
            status = self.user_client.get_status(id)
            self.panels[i].SetPage(status["content"])
