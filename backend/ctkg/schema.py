from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Node:
    id: str
    label: str
    properties: dict = field(default_factory=dict)

@dataclass
class Edge:
    source_id: str
    target_id: str
    type: str
    properties: dict = field(default_factory=dict)

@dataclass
class Study(Node):
    label: str = "Study"

@dataclass
class Condition(Node):
    label: str = "Condition"

@dataclass
class Drug(Node):
    label: str = "Drug"

@dataclass
class Outcome(Node):
    label: str = "Outcome"

@dataclass
class CTKGData:
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
