from cProfile import label
import wx, wx.html

from comms_panel.backends.timeline import Timeline


class TimelinePanel(wx.ScrolledWindow):
    timeline: Timeline

    def __init__(self, parent, timeline, **kw):
        super().__init__(parent, **kw)
        self.timeline = timeline
        self.title_pane = wx.StaticText(self, label=timeline.title)
        self.panel_sizer = wx.FlexGridSizer(1)
        self.SetSizer(self.panel_sizer)
        self.SetAutoLayout(1)
        self.panel_sizer.Fit(self)
        self.panel_sizer.Add(self.title_pane)

    def update(self):
        self.panel_sizer.Clear()
        self.panel_sizer.Add(self.title_pane)
        self.timeline.update()
        for status in self.timeline.statuses:
            self.panel_sizer.Add(
                wx.StaticText(self, label=f"{status["created_at"]} by {status["account"]["display_name"]}")
            )
            html = wx.html.HtmlWindow(self, style=wx.html.HW_SCROLLBAR_NEVER)
            html.SetPage(status["content"])
            # html.SetAutoLayout(1)
            # html.Fit()
            # html.Size = html.VirtualSize
            self.panel_sizer.Add(html)
