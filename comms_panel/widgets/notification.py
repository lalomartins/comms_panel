import wx, wx.html

from comms_panel.lib.html import cleanup_html


class NotificationPanel(wx.Panel):
    notification: dict

    def __init__(self, parent, status, width, *args, **kw):
        super().__init__(*args, parent, **kw)
        self.notification = status
        self.base_size = wx.Size(width, 30)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.panel_sizer)
        self.SetAutoLayout(1)
        self.panel_sizer.Fit(self)
        self.head = wx.StaticText(self)
        self.status_head = wx.StaticText(self)
        self.body = wx.html.HtmlWindow(self, style=wx.html.HW_SCROLLBAR_AUTO, size=self.base_size)
        self.panel_sizer.AddMany([self.head, self.status_head, self.body])
        self.update()

    def update(self) -> None:
        match self.notification["type"]:
            case "mention": # Someone mentioned you in their status
                self.head.SetLabel("Someone mentioned you in their status")
            case "status": # Someone you enabled notifications for has posted a status
                self.head.SetLabel("Someone you enabled notifications for has posted a status")
            case "reblog": # Someone boosted one of your statuses
                self.head.SetLabel(f"Boosted on {self.notification["created_at"]} by {self.notification["account"]["display_name"]}")
            case "follow": # Someone followed you
                self.head.SetLabel(f"Follow on {self.notification["created_at"]} from {self.notification["account"]["display_name"]}")
            case "follow_request": # Someone requested to follow you
                self.head.SetLabel(f"Follow request on {self.notification["created_at"]} from {self.notification["account"]["display_name"]}")
            case "favourite": # Someone favourited one of your statuses
                self.head.SetLabel(f"Favorite on {self.notification["created_at"]} from {self.notification["account"]["display_name"]}")
            case "poll": # A poll you have voted in or created has ended
                self.head.SetLabel("A poll you have voted in or created has ended")
            case "update": # A status you interacted with has been edited
                self.head.SetLabel("A status you interacted with has been edited")
            case _:
                self.head.SetLabel(f"Unknown notification: {self.notification["type"]}")
        self.head.Wrap(self.base_size.width)

        status = self.notification.get("status", {})
        if status:
            self.status_head.Show()
            self.body.Show()
            if status["content"]:
                self.status_head.SetLabel(f"{status["created_at"]} by {status["account"]["display_name"]}")
                self.status_head.Wrap(self.base_size.width)
                self.body.SetPage(cleanup_html(status["content"]))
                self.body.SetMinSize(wx.Size(self.base_size.width, self.body.VirtualSize.height + 10))
            else:
                self.body.SetPage("<i>No content</i>")
                self.body.SetMinSize(wx.Size(self.base_size.width, 20))
        else:
            self.status_head.Hide()
            self.body.Hide()
