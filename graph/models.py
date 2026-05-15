from dataclasses import dataclass, field

@dataclass
class DepthConfig:
    root: str
    depth: int


@dataclass
class ViewConfig:
    name: str
    include: list[str]
    exclude: list[str] = field(default_factory=list)
    groups: dict[str, list[str]] = field(default_factory=dict)
    depth_config: DepthConfig | None = None