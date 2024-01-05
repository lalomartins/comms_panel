from abc import abstractmethod
from datetime import datetime, timedelta


class Timeline:
    title: str
    updated: datetime
    next_update: datetime | None
    update_period: timedelta | None
    statuses: list[dict]

    # Override this and add the actual implementation *before* calling super
    def update(self) -> None:
        self.updated = datetime.now()
        if self.update_period is not None:
            self.next_update = self.updated + self.update_period

    def maybe_update(self) -> None:
        if self.next_update is not None and self.next_update <= datetime.now():
            self.update()
