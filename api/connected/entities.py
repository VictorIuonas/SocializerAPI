from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class DevsConnection:
    timestamp: datetime
    connected: bool
    organizations: List[str]

    def to_dict(self):
        return asdict(self)
