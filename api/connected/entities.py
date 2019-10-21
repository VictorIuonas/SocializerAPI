from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class OrganizationEntity:
    name: str
    id: int
    external_id: int

    def __hash__(self):
        return self.id


@dataclass
class DevsConnection:
    timestamp: datetime
    connected: bool
    organizations: List[OrganizationEntity]

    def to_dict(self):
        return asdict(self)
