from cProfile import label
import wx, wx.lib.scrolledpanel, wx.html

from comms_panel.backends.timeline import Timeline
from comms_panel.lib.html import cleanup_html


class TimelinePanel(wx.lib.scrolledpanel.ScrolledPanel):
    timeline: Timeline

    def __init__(self, parent, timeline, **kw):
        super().__init__(parent, **kw)
        self._default_width = self.Size.width
        self.timeline = timeline
        self.title_pane = wx.StaticText(self, label=timeline.title)
        self.panel_sizer = wx.FlexGridSizer(1)
        self.SetSizer(self.panel_sizer)
        # self.SetAutoLayout(1)
        # self.panel_sizer.Fit(self)
        self.EnableScrolling(False, True)
        self.panel_sizer.Add(self.title_pane)
        self.SetupScrolling()

    def update(self):
        size = wx.Size((self.Size.width or self._default_width) - 20, 30)
        wx.SafeYield()
        self.panel_sizer.Clear()
        self.panel_sizer.Add(self.title_pane)
        self.timeline.update()
        for status in self.timeline.statuses:
            self.panel_sizer.AddSpacer(20)
            self.panel_sizer.Add(
                wx.StaticText(self, label=f"{status["created_at"]} by {status["account"]["display_name"]}")
            )
            html = wx.html.HtmlWindow(self, style=wx.html.HW_SCROLLBAR_AUTO, size=size)
            orig = status.get("reblog", {})
            if status["content"]:
                html.SetPage(cleanup_html(status["content"]))
            elif not orig:
                self.panel_sizer.Add(wx.StaticText(self, label="No content"))

            if orig:
                self.panel_sizer.Add(
                    wx.StaticText(self, label=f"Reblog of {orig["created_at"]} by {orig["account"]["display_name"]}")
                )
                html.SetPage(cleanup_html(orig["content"]))
            wx.SafeYield()
            html.SetMinSize(wx.Size(size.width, html.VirtualSize.height + 10))
            self.panel_sizer.Add(html)
