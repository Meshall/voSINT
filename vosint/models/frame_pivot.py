from dataclasses import dataclass, field


@dataclass
class FramePivot:
    frame_id: str
    ocr_terms: list[str] = field(default_factory=list)
    transcript_terms: list[str] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "frame_id": self.frame_id,
            "ocr_terms": self.ocr_terms,
            "transcript_terms": self.transcript_terms,
            "queries": self.queries,
        }
