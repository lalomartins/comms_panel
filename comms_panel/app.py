"""Main module."""

import wx


class App(wx.App):
    def __init__(self):
        super().__init__(False)
        self.frame = wx.Frame(None, wx.ID_ANY, "Hello World")

    def run(self):
        self.frame.Show(True)
        self.MainLoop()
