from typing import List
from dataclasses import dataclass


@dataclass
class FixResult:
    fix_messages: List[str]
    repo_was_cherrypicked: bool
    is_chunk_fixing_required: bool
