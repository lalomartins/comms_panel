import wx, wx.html

from comms_panel.lib.html import cleanup_html


class StatusPanel(wx.Panel):
    status: dict

    def __init__(self, parent, status, width, *args, **kw):
        super().__init__(*args, parent, **kw)
        self.status = status
        self.base_size = wx.Size(width, 30)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.panel_sizer)
        self.SetAutoLayout(1)
        self.panel_sizer.Fit(self)
        self.head = wx.StaticText(self)
        self.body = wx.html.HtmlWindow(self, style=wx.html.HW_SCROLLBAR_AUTO, size=self.base_size)
        self.orig_head = wx.StaticText(self)
        self.orig_body = wx.html.HtmlWindow(self, style=wx.html.HW_SCROLLBAR_AUTO, size=self.base_size)
        self.panel_sizer.AddMany([self.head, self.body, self.orig_head, self.orig_body])
        self.update()

    def update(self) -> None:
        self.head.SetLabel(f"{self.status["created_at"]} by {self.status["account"]["display_name"]}")
        self.head.Wrap(self.base_size.width)
        orig = self.status.get("reblog", {})

        self.body.Show()
        if self.status["content"]:
            self.body.SetPage(cleanup_html(self.status["content"]))
            self.body.SetMinSize(wx.Size(self.base_size.width, self.body.VirtualSize.height + 10))
        elif orig:
            self.body.Hide()
        else:
            self.body.SetPage("<i>No content</i>")
            self.body.SetMinSize(wx.Size(self.base_size.width, 20))

        if orig:
            self.orig_head.SetLabel(f"Reblog of {orig["created_at"]} by {orig["account"]["display_name"]}")
            self.orig_body.SetPage(cleanup_html(orig["content"]))
            self.orig_head.Show()
            self.orig_body.SetMinSize(wx.Size(self.base_size.width, self.orig_body.VirtualSize.height + 10))
            self.orig_body.Show()
        else:
            self.orig_head.Hide()
            self.orig_body.Hide()
