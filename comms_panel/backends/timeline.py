from abc import abstractmethod
from datetime import datetime, timedelta


class Timeline:
    title: str
    updated: datetime
    next_update: datetime
    update_period: timedelta | None
    statuses: list[dict]

    @abstractmethod
    def update(self) -> None:
        pass

    def maybe_update(self) -> None:
        if self.next_update is not None and self.next_update <= datetime.now():
            self.update()
