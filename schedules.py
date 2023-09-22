
from dataclasses import dataclass, field, fields
from typing import List, Optional


@dataclass
class FRCEvent:
    """Holds basic FRC event details"""
    code: str = ""
    loc: str = ""
    capacity: int = 36


@dataclass
class Schedule:
    """Represents a schedule of FRC events"""
    name: str = ""
    week1: Optional[List[FRCEvent]] = field(default_factory=list)
    week2: Optional[List[FRCEvent]] = field(default_factory=list)
    week3: Optional[List[FRCEvent]] = field(default_factory=list)
    week4: Optional[List[FRCEvent]] = field(default_factory=list)
    week5: Optional[List[FRCEvent]] = field(default_factory=list)
    week6: Optional[List[FRCEvent]] = field(default_factory=list)

    def getWeek(self, week: int) -> List[FRCEvent]:
        return getattr(self, "week" + str(week))

    def getEvent(self, week: int, idx: int) -> FRCEvent:
        """Returns an FRC event at a given position in a week of events. Weeks start at 1 and go to 6"""
        return self.getWeek(week)[idx]

    def getEventsPerWeek(self) -> List[int]:
        """Returns how many events are in each week of the schedule"""
        return [len(self.getWeek(w)) for w in range(1, 7)]

    def getAllEvents(self) -> List[FRCEvent]:
        returnList = []
        for w in range(1, 7):
            returnList += self.getWeek(w)

        return returnList
