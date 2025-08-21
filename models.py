from dataclasses import dataclass, asdict
import json

@dataclass(frozen=True)
class CommuteResult:
    origin: str
    destination: str
    duration_minutes: float
    duration_text: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
