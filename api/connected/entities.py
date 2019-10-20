from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class Organization:
    external_id: int
    name: str
    id: int

    def __hash__(self):
        return self.external_id


@dataclass
class DevsConnection:
    timestamp: datetime
    connected: bool
    organizations: List[str]

    def to_dict(self):
        return asdict(self)