from dataclasses import dataclass, field
from datetime import datetime, date, time
from email.policy import default
from platform import system
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_n, slot_not_available_error


@dataclass
class Reminder:
    EMAIL: ClassVar[str] = "email"
    SYSTEM: ClassVar[str] = "system"
    date_time: datetime = datetime
    type: str = EMAIL

    def __str__(self) -> str :
        return f"Reminder on {self.date_time} of type {self.type}"

@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder]
    id: str = field(default_factory=generate_unique_id())

    def add_reminder(self, date_time: datetime, type: str):
        add_reminder: Reminder = Reminder(date_time, type)
        self.reminders.append(add_reminder)

    def delete_reminder(self, reminder_index: int):
            if 0<= reminder_index < len(self.reminders):
                del self.reminders[reminder_index]
            else:
                reminder_not_found_error()

    def __str__(self):
        return (f"ID: {self.id} /n"
                f"Event title: {self.title} /n"
                f"Description: {self.description} /n"
                f"Time: {self.start_at} - {self.end_at}")


class Day:
    def __init__(self, date_: date):
        self.date_: date
        self.slots: dict[time, str | None] = {}

    def _init_slots(self):
        for hour in range(24):
            for minute in range(0, 60, 15):
                self.slots[time(hour, minute)] = None

    def add_event(self, event_id: str, start_at: time, end_at: time):
        pass

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id



