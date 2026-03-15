from dataclasses import dataclass, field
from pathlib import Path

from .frame_pivot import FramePivot
from .hit import Hit
from .video_dna import VideoDNA


@dataclass
class Case:
    case_id: str
    mode: str
    input_path: str
    case_dir: Path
    hits: list[Hit] = field(default_factory=list)
    pivots: list[FramePivot] = field(default_factory=list)
    video_dna: VideoDNA | None = None
    failures: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "case_id": self.case_id,
            "mode": self.mode,
            "input_path": self.input_path,
            "hits": [h.to_dict() for h in self.hits],
            "pivots": [p.to_dict() for p in self.pivots],
            "video_dna": self.video_dna.to_dict() if self.video_dna else None,
            "failures": self.failures,
        }
