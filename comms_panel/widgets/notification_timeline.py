import wx
from comms_panel.widgets.notification import NotificationPanel

from comms_panel.widgets.timeline import TimelinePanel


class NotificationsTimelinePanel(TimelinePanel):
    def update(self):
        self.timeline.update()
        width = (self.Size.width or self._default_width) - 20
        self.panel_sizer.Clear(delete_windows=True)
        self.panel_sizer.Add(wx.StaticText(self, label=self.timeline.title))
        for notification in self.timeline.items:
            self.panel_sizer.AddSpacer(20)
            self.panel_sizer.Add(NotificationPanel(self, notification, width))
        self.Layout()
        self.SetupScrolling()
