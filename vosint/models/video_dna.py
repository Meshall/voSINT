from dataclasses import dataclass, field


@dataclass
class VideoDNA:
    video_hash: str
    frame_hashes: dict[str, str] = field(default_factory=dict)
    scene_hashes: list[str] = field(default_factory=list)
    ocr_terms: list[str] = field(default_factory=list)
    transcript_terms: list[str] = field(default_factory=list)
    logos_watermarks: list[str] = field(default_factory=list)
    best_pivots: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "video_hash": self.video_hash,
            "frame_hashes": self.frame_hashes,
            "scene_hashes": self.scene_hashes,
            "ocr_terms": self.ocr_terms,
            "transcript_terms": self.transcript_terms,
            "logos_watermarks": self.logos_watermarks,
            "best_pivots": self.best_pivots,
        }
