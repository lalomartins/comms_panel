import asyncio
from datetime import datetime
from logging import debug
import wx, wx.lib.scrolledpanel, wx.html

from comms_panel.backends.timeline import Timeline
from comms_panel.lib.html import cleanup_html
from comms_panel.widgets.status import StatusPanel


class TimelinePanel(wx.lib.scrolledpanel.ScrolledPanel):
    timeline: Timeline

    def __init__(self, parent, timeline, **kw):
        super().__init__(parent, **kw)
        self._default_width = self.Size.width
        self.timeline = timeline
        self.panel_sizer = wx.FlexGridSizer(1)
        self.SetSizer(self.panel_sizer)
        self.EnableScrolling(False, True)
        self.panel_sizer.Add(wx.StaticText(self, label=timeline.title))
        self.SetupScrolling()

    def update(self):
        self.timeline.update()
        width = (self.Size.width or self._default_width) - 20
        self.panel_sizer.Clear(delete_windows=True)
        self.panel_sizer.Add(wx.StaticText(self, label=self.timeline.title))
        for status in self.timeline.items:
            self.panel_sizer.AddSpacer(20)
            self.panel_sizer.Add(StatusPanel(self, status, width))
        self.Layout()
        self.SetupScrolling()

    async def auto_update(self) -> None:
        while self.timeline.next_update is not None:
            await asyncio.sleep(
                (self.timeline.next_update - datetime.now()).total_seconds()
            )
            debug(f"Updating {self.timeline.title} timeline")
            self.update()
